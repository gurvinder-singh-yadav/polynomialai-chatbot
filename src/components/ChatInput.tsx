"use client"

import axios from 'axios';
import { useState } from 'react';
import { useRecoilState } from 'recoil';
import { messagesState } from '../app/page';

interface ChatInputProps {
    userId: string;
}

export default function ChatInput({ userId }: ChatInputProps) {
    const [message, setMessage] = useState('')
    const [messages, setMessages] = useRecoilState(messagesState);
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async () => {
        if (!message.trim()) return;

        // Immediately update messages with user's message and loading state
        const userMessage = {
            content: message,
            role: "user",
            type: "text",
            created_at: new Date().toISOString()
        };
        const loadingMessage = {
            content: "⏳",
            role: "model",
            type: "loading",
            created_at: new Date().toISOString()
        };

        setMessages([...messages, userMessage, loadingMessage]);
        setMessage(''); // Clear input immediately
        setIsLoading(true);

        try {
            const modelResponse = await axios.post(`http://localhost:8000/agent`, {
                content: message,
                role: "user",
                created_at: userMessage.created_at
            });

            // Replace loading message with actual response
            setMessages(prevMessages => [
                ...prevMessages.slice(0, -1), // Remove loading message
                {
                    content: modelResponse.data.content,
                    role: "model",
                    type: "text",
                    created_at: modelResponse.data.created_at
                }
            ]);

            // Update backend
            await axios.put(`http://localhost:8000/users/${userId}`, {
                messages: [
                    {
                        created_at: userMessage.created_at,
                        content: message,
                        role: "user"
                    },
                    {
                        created_at: modelResponse.data.created_at,
                        content: modelResponse.data.content,
                        role: "model"
                    }
                ]
            }, {
                headers: {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            });
        } catch (error) {
            // Remove loading message and show error
            setMessages(prevMessages => [
                ...prevMessages.slice(0, -1),
                {
                    content: "Error generating response. Please try again.",
                    role: "model",
                    type: "text",
                    created_at: new Date().toISOString()
                }
            ]);
            console.error('Error sending message:', error);
        } finally {
            setIsLoading(false);
        }
    }

    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter') {
            handleSubmit();
        }
    }

    return (
        <div className="flex justify-center items-center w-full mb-4">
            <input
                type="text"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyDown={handleKeyDown}
                className="w-[60%] text-center p-4 text-xl rounded-full border-2 border-black-200"
                placeholder="Type your message here..."
                disabled={isLoading}
            />
            <button
                onClick={handleSubmit}
                className={`${isLoading ? 'bg-gray-500' : 'bg-blue-500'} text-white p-4 rounded-full`}
                disabled={isLoading}
            >
                {isLoading ? 'Sending...' : 'Send'}
            </button>
        </div>
    )
}