import json
import os
from typing import List, Dict
import google.generativeai as genai
from google.generativeai import embed_content
import pymongo
from pymongo import MongoClient
from pymongo.collection import Collection
from config import config
import hashlib
from time import time


class KnowledgeBaseManager:
    def __init__(
        self, knowledge_base_dir: str, embedding_model: str, mongo_uri: str
    ):
        self.knowledge_base_dir = knowledge_base_dir
        self.embedding_model = embedding_model
        self.mongo_uri = mongo_uri
        self.client = None
        self.db = None
        self.collection: Collection = None
        self.initialize_mongodb()
        self.files_processed = self.get_already_processed_files()
        self.load_knowledge() # Load during initialization

    def initialize_mongodb(self):
        """Initializes the MongoDB connection, creates a database and collection if not exists"""
        self.client = MongoClient(self.mongo_uri, username=config.MONGO_USERNAME, password=config.MONGO_PASSWORD)
        
        self.db = self.client.get_database("agent_db")
        self.collection = self.db.get_collection("knowledge_base")
        self.collection.create_index([("file_hash", pymongo.ASCENDING)], name="file_hash")

    def generate_chunk_hash(self, chunk: str) -> str:
        """Generates a hash of the given chunk"""
        return hashlib.sha256(chunk.encode()).hexdigest()

    def generate_file_hash(self, file_path: str) -> str:
        """Generate hash of a given file based on the file content"""
        with open(file_path, "rb") as f:
            content = f.read()
            return hashlib.sha256(content).hexdigest()

    def get_already_processed_files(self) -> set:
        """Get the hash value of all the files from the database"""
        processed_files_data = self.collection.distinct("file_hash")
        return set(processed_files_data)


    def load_knowledge(self):
        """Load and chunk knowledge from JSON files in the specified directory and stores to db"""
        for file in os.listdir(self.knowledge_base_dir):
            if file.endswith(".json"):
                file_path = os.path.join(self.knowledge_base_dir, file)
                try:
                    with open(file_path, "r") as f:
                        data = json.load(f)
                        file_hash = self.generate_file_hash(file_path)
                        self.process_json_data(data, file, file_hash)
                except json.JSONDecodeError:
                   print(f"Error: Skipping file {file} because it's not a valid JSON.")
                   continue

    def process_json_data(self, data: dict, file_name: str, file_hash: str):
        """Process data, chunk it, and store it in the DB"""
        if file_hash in self.files_processed:
            print(f"File '{file_name}' already processed, skipping")
            return

        if isinstance(data, dict) and "qa_pairs" in data:
            self._process_qa_pairs(data["qa_pairs"], file_name, file_hash)
        else:
            print(
                f"Warning: Expected 'qa_pairs' key in JSON data for '{file_name}'. Skipping"
            )
    
    def _process_qa_pairs(self, qa_pairs: List[Dict], file_name: str, file_hash: str):
       """ Process a list of QA pairs and chunk them"""
       chunk:List[str] = []
       entity_count = 0

       for qa_pair in qa_pairs:
         if isinstance(qa_pair,dict) and "question" in qa_pair and "answers" in qa_pair:
            chunk.append(json.dumps(qa_pair))
            entity_count += 1
         else:
            print(f"Warning: Invalid format in qa_pair, skipping {qa_pair}")
            continue

         if entity_count >= 10:
              self._store_chunk(chunk, file_name, file_hash)
              chunk = []
              entity_count = 0
       
       if chunk:
         self._store_chunk(chunk, file_name, file_hash)


    def _store_chunk(self, chunk: List[str], file_name: str, file_hash: str):
       """Store a chunk to the database after generating embedding"""
       chunk_text = "\n".join(chunk)
       chunk_hash = self.generate_chunk_hash(chunk_text)
       if self.check_chunk_exists(chunk_hash, file_hash):
         print(f"Skipping existing chunk: '{chunk_text[0:20]}...', file: '{file_name}', file_hash: {file_hash}")
         return

       self.store_embedding(chunk_text, file_name, chunk_hash, file_hash)

    def store_embedding(self, chunk: str, file_name: str, chunk_hash: str, file_hash: str):
        """Generate the embedding for a given chunk and stores the data to db."""
        try:
            response = embed_content(model=self.embedding_model, content=chunk)
            if response and 'embedding' in response:
                vector = response['embedding']
                document = {
                    "text": chunk,
                    "vector": vector,
                    "file_name": file_name,
                    "chunk_hash": chunk_hash,
                    "file_hash": file_hash,
                }
                self.collection.insert_one(document)
                print(
                    f"Successfully stored embedding for: '{chunk[0:20]}...', file: '{file_name}', file_hash: {file_hash}"
                )
            else:
                print(f"Error generating embedding for chunk: '{chunk[0:20]}...'")
        except Exception as e:
            print(f"Error embedding or storing chunk: '{chunk[0:20]}...': {e}")

    def check_chunk_exists(self, chunk_hash: str, file_hash: str):
        """Check if the given chunk hash and file hash exists in the db"""
        return bool(
            self.collection.find_one(
                {"chunk_hash": chunk_hash, "file_hash": file_hash}
            )
        )

    def search_db(self, query: str, top_k: int = 3) -> list:
        """Searches the vector database for similar content using cosine similarity."""
        response = embed_content(model=self.embedding_model, content=query)
        query_embedding = response['embedding']

        # Get all documents and calculate similarity locally
        all_docs = list(self.collection.find({}, {"_id": 0, "text": 1, "vector": 1}))
        
        # Calculate cosine similarity for each document
        for doc in all_docs:
            vec1 = query_embedding
            vec2 = doc['vector']
            # Compute dot product
            dot_product = sum(a * b for a, b in zip(vec1, vec2))
            # Compute magnitudes
            mag1 = sum(a * a for a in vec1) ** 0.5
            mag2 = sum(b * b for b in vec2) ** 0.5
            # Compute cosine similarity
            doc['score'] = dot_product / (mag1 * mag2) if mag1 * mag2 != 0 else 0

        # Sort by similarity score and get top_k results
        results = sorted(all_docs, key=lambda x: x['score'], reverse=True)[:top_k]
        return [{"text": doc["text"], "score": doc["score"]} for doc in results]

    def update_knowledge_base(self):
      """Checks the json file for the changes and updates the database accordingly."""
      print("Starting knowledge base update...")
      start = time()
      new_files_processed = set()
      for file in os.listdir(self.knowledge_base_dir):
        if file.endswith(".json"):
            file_path = os.path.join(self.knowledge_base_dir, file)
            file_hash = self.generate_file_hash(file_path)
            new_files_processed.add(file_hash)
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                print(
                    f"Error: Skipping file {file} because it's not a valid JSON."
                )
                continue
            self.process_json_data(data, file, file_hash)
      files_to_remove = self.files_processed.difference(new_files_processed)
      if files_to_remove:
        self.delete_obsolete_files(list(files_to_remove))
      self.files_processed = new_files_processed
      end = time()
      print(f"Knowledge base update complete, time taken: {end - start}")

    def delete_obsolete_files(self, files_hash_to_remove: List[str]):
        """Deletes the data corresponding to the given file hashes"""
        result = self.collection.delete_many({"file_hash": {"$in": files_hash_to_remove}})
        print(f"Deleted {result.deleted_count} records for obsolete files")


class Agent:
    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or "gemini-1.5-flash"
        self.messages = []
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(model_name=self.model_name)
        self.knowledge_manager = KnowledgeBaseManager(
            knowledge_base_dir="./knowledge-base",
            embedding_model="models/embedding-001",
            mongo_uri=config.MONGO_URI,
        )

    def add_message(self, message: str):
        self.messages.append({"role": "user", "parts": [{"text": message}]})

    def get_response(self, message: str):
        self.add_message(message)
        context_search = self.knowledge_manager.search_db(query=message)
        context = "\n\n".join(
            [f"Context: {item['text']}" for item in context_search]
        )  # Format the retrieved contexts
        prompt = f"""
            You are a helpful assistant and your response should be based on the information given in the context.
             If the answer can't be found in the context, say "I am sorry, I don't have the context to answer that question. ".
             Do not generate any response that does not belong to the context.
             Context: {context}
             User Question: {message}
             Response : text only
        """
        self.messages.append({"role": "user", "parts": [{"text": prompt}]})
        response = self.model.generate_content(self.messages)
        self.messages.append({"role": "model", "parts": [{"text": response.text}]})
        return response.text

    def clear_messages(self):
        self.messages = []

    def update_knowledge(self):
        """Updates the knowledge base."""
        self.knowledge_manager.update_knowledge_base()

