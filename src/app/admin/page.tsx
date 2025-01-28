"use client"
import NavBar from "@/src/components/NavBar";
import ChatCards from "@/src/components/ChatCards";
import { useEffect, useState } from "react";
import axios from "axios";

interface Message{
    content: string;
    role: string;
    created_at: string;
}

interface ChatCardProps {
    _id: string;
    created_at: string;
    updated_at: string;
    messages: Message[];
}

export default function Admin() {
    const [chatCards, setChatCards] = useState<ChatCardProps[]>([]);
    useEffect(() => {
        const fetchChatCards = async () => {
            const response = await axios.get('http://localhost:8000/chats');
            console.log(response.data)
            setChatCards(response.data);
        };
        fetchChatCards();
    }, []);
    
    return (
        <div className="flex flex-col h-screen bg-yellow-100">
            <NavBar />
            <div className="grid grid-cols-3 gap-4 bg-yellow-100 p-4">
                {chatCards.map((chatcard, index) => {
                    return (
                        <ChatCards key={index} cardProps={chatcard} />
                    )
                })}
            </div>
        </div>
    )
}