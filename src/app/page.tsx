"use client"

import ChatInput from '@/components/ChatInput'
import Message from '@/components/Message'
import NavBar from '@/components/NavBar'
import axios from 'axios'
import { useEffect, useState } from 'react'
import { atom, useRecoilValue } from 'recoil'
export interface ChatMessage {
  content: string;
  role: string;
  created_at: string;
  type: string;
}

export const messagesState = atom<ChatMessage[]>({
  key: 'messagesState',
  default: [],
});

export default function Home() {
  const messages = useRecoilValue(messagesState);
  const [userId, setUserId] = useState<string>("");
  useEffect(() => {
    const createUser = async () => {
      try {
        const response = await axios.post('http://localhost:8000/users');
        console.log('User created:', response.data);
        setUserId(response.data.id);
      } catch (error) {
        console.error('Error creating user:', error);
        if (axios.isAxiosError(error)) {
          console.error('Response:', error.response?.data);
        }
      }
    };
    createUser();
  }, []);
  return (
    <div className="flex h-screen flex-col bg-yellow-100">
      <NavBar />
      <div className="flex-1 overflow-y-auto">
        <div className="w-full flex flex-col items-center">
          {/* Update Message mapping to use useRecoilValue in the Message component */}
          {/* {messages.map((message, index) => (
              <Message key={index} role={message.role}>
                {message.content}
              </Message>
            ))} */}
          {messages.map((message, index) => (
            <Message
              key={index}
              role={message.role}
              type={message.type}
            >
              {message.content}
            </Message>
          ))}
        </div>
      </div>
      <ChatInput userId={userId} />
    </div>

  )
}
