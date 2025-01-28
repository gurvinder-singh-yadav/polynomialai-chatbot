"use client"
import { Dialog, DialogPanel, DialogTitle, Transition, TransitionChild } from '@headlessui/react';
import { Fragment, useState } from 'react';

interface Message {
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
export default function ChatCards({ cardProps }: { cardProps: ChatCardProps }) {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <>
            <div className="flex flex-col bg-white p-4 rounded-lg shadow-md cursor-pointer" onClick={() => setIsOpen(true)}>
                {/* <h1 className="text-2xl font-medium leading-6 text-gray-900">{cardProps._id}</h1> */}
                <h3>{new Date(cardProps.created_at).toLocaleString('en-US', {
                    dateStyle: 'medium',
                    timeStyle: 'short'
                })}</h3>
                <p>{cardProps.messages[0]?.content}...</p>
            </div>

            <Transition appear show={isOpen} as={Fragment}>
                <Dialog as="div" className="relative z-10" onClose={() => setIsOpen(false)}>
                    <TransitionChild
                        as={Fragment}
                        enter="ease-out duration-300"
                        enterFrom="opacity-0"
                        enterTo="opacity-100"
                        leave="ease-in duration-200"
                        leaveFrom="opacity-100"
                        leaveTo="opacity-0"
                    >
                        <div className="fixed inset-0 bg-black bg-opacity-25" />
                    </TransitionChild>

                    <div className="fixed inset-0 overflow-y-auto">
                        <div className="flex min-h-full items-center justify-center p-4">
                            <TransitionChild
                                as={Fragment}
                                enter="ease-out duration-300"
                                enterFrom="opacity-0 scale-95"
                                enterTo="opacity-100 scale-100"
                                leave="ease-in duration-200"
                                leaveFrom="opacity-100 scale-100"
                                leaveTo="opacity-0 scale-95"
                            >
                                <DialogPanel className="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
                                    <DialogTitle as="h3" className="text-lg font-medium leading-6 text-gray-900">
                                        Chat Messages
                                    </DialogTitle>
                                    <div className="mt-4 max-h-96 overflow-y-auto">
                                        <ul className="space-y-2">
                                            {cardProps.messages.map((message, index) => (
                                                <li
                                                    key={index}
                                                    className={`p-2 rounded ${message.role === 'assistant' || message.role === 'model'
                                                            ? 'bg-green-200'
                                                            : 'bg-gray-50'
                                                        }`}
                                                >
                                                    {message.content}
                                                </li>
                                            ))}
                                        </ul>
                                    </div>
                                </DialogPanel>
                            </TransitionChild>
                        </div>
                    </div>
                </Dialog>
            </Transition>
        </>
    );
}