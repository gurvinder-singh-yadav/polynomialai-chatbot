## chat bot application with active knowledge base



# Knowledge-Based Conversational AI System

This document outlines the architecture and features of a knowledge-based conversational AI system. The system utilizes a combination of technologies for efficient knowledge management, query handling, and user interaction.

## Demonstration Video

Here is a demonstration video of the conversational AI system in action:
```html
<div align="center">
<iframe width="560" height="315" src="https://www.youtube.com/embed/3Mzf3pFW0qQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>
```

## Knowledge Base Integration:

**Pre-loading:**
*   The system is pre-loaded with a structured knowledge base stored as JSON files within a local directory named `knowledge-base`.
*   These JSON files contain question-answer (Q&A) pairs, which are the fundamental units of knowledge for the system.
*   **Data Format:** Each JSON file contains a list of `qa_pairs` where each `qa_pair` has a "question" and "answers" field.
    ```json
       {
            "qa_pairs": [
                {
                    "question": "the 1999 film '10 things i hate about you' is based on which shakespeare play",
                    "answers": ["taming of the shrew"]
                },
                {
                   "question": "who began as a broadway actor, made his hollywood debut in 1935, and had lead roles in the grapes of wrath, the ox-bow incident, mister roberts and 12 angry men",
                   "answers": ["henry fonda"]
                }
            ]
        }

    ```

*   **Chunking:** Upon loading, the Q&A data is chunked to optimize the system's performance and resource utilization, particularly due to limited credits in the Google Gemini Studio. The chunking strategy ensures each chunk contains at least 10 Q&A entities (pairs).

*   **Embedding:** Embeddings are generated for each chunk using the Google Gemini `model-004` embedding model.
*   **Storage:** The generated chunk embeddings, along with the original text are stored in MongoDB as a vector store. This facilitates efficient similarity-based retrieval of relevant context for user queries.

*   **Periodic Updates:** The knowledge base is designed to accommodate periodic updates. New files added to the `knowledge-base` folder will be processed, chunked, and added to the database, also if any changes are made to the existing files it also updates the database based on the new content in the file and removes any obsolete data from the database which are no longer present in the `knowledge-base` folder.

## Dynamic Query Handling:

*   **LLM Utilization:** The system uses Google's Gemini 1.5 Flash model for processing user queries and generating responses. This model is selected for its balance between speed and performance for conversational AI tasks.
*   **Contextual Processing:**
    *   User queries are first processed by the embedding model (`model-004`) to generate embeddings.
    *   These embeddings are used to perform similarity searches in the MongoDB vector store.
    *   The most relevant context chunks are then retrieved and included in the prompt passed to Gemini 1.5 Flash to generate the response.
*   **Prompt Engineering:** The prompt sent to the LLM include the retrieved context and the user query to ensure the response is grounded in the available knowledge base.

## Flask Application Features:

**Frontend:**
*   **Technology:** The frontend is built using Next.js. This allows for efficient server-side rendering and a modern user experience.
*   **Features:** The frontend provides a simple user interface with:
    *   A text input box where users can enter their queries.
    *   A display area to show the system’s responses.
*   **API Endpoint:**
    *   **Technology:** The API backend is built using FastAPI. This choice enables asynchronous operation and is particularly suited for handling large language model tasks.
    *   **Endpoint:** A `/agent` GET endpoint that accepts user queries via a query parameter `msg`.

*   **Admin Features:**
    * **Technology:**  The admin section is integrated directly into the Next.js frontend and communicates with the FastAPI backend.
    *   **Knowledge Base Updates:**
        *   Provides functionality to initiate an update of the knowledge base.
        *   It can detect added, deleted or modified knowledge base content and update the MongoDB vector store accordingly.
    *   **Conversation Logging:**
        *   Displays all the conversation logs stored in the mongo db database.
        *  Accessible via the `/admin` endpoint.
        *  Allows filtering conversations by user id, which is unique for every conversation.

## Interaction Logging:
*   **Storage:** All user queries and the system's corresponding responses are stored in MongoDB.
*   **Logging Details:**
    *   Each user interaction is logged with a unique user ID which is generated at the start of each conversation.
    *   Both the user's question and the LLM's response are logged in the database.

## Fallback Mechanism:

*   **Context Absence:** If the Gemini 1.5 Flash model cannot generate an answer based on the retrieved context, it provides a polite fallback response.
*   **Fallback Response:** The fallback response states that the system does not have sufficient context to provide an answer, ensuring transparency and a good user experience.
*   **No Generated Content:** The LLM is restricted to only answer based on the given context, and it cannot provide any output if it does not have sufficient context from the knowledge base.

## Technology Comparison:

*   **Template LLM:** The template suggests using OpenAI’s GPT models, while this implementation uses Google's Gemini 1.5 Flash for the conversational model and `model-004` for embedding. This was chosen to take advantage of Google's latest generative AI offerings.
*   **Template Frontend (Optional):** The template mentions using a simple web interface via Flask, but the system uses Next.js for better performance, server-side rendering, and a more robust frontend architecture.
* **Template Backend:** The template mentions using Flask for the API but, this implementation uses FastAPI. The choice was done to better align with the asynchronous operations of LLMs, and to provide efficient API handling.

This markdown provides a detailed description of the system. This setup ensures you have an efficient, knowledge-based conversational bot that is capable of answering user questions based on the pre-loaded knowledge base, and also logging all the conversation and providing an admin panel to see all the conversations and update the knowledge base as well.

```bash
docker-compose up -d
npm i
pip install -r requirements.txt
npm run dev
```
