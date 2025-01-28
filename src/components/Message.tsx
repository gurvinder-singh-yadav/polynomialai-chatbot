"use client"

export default function Message({ role, children, type }: {
    role: string,
    children: React.ReactNode,
    type?: string  // Add optional type prop
}) {
    // if role is user show on the left, if role is assistant show on the right
    const isUser = role === 'user';
    const isLoading = type === 'loading';

    return (
        <div className={`flex w-full ${!isUser ? 'justify-start ml-4' : 'justify-end mr-4'} `}>
            <div className={`flex flex-col rounded-2xl p-4 max-w-[80%] ${!isUser ? 'bg-white' : 'bg-white'
                }`}>
                {isLoading ? (
                    <span className="loading-spinner">{children}</span>
                ) : (
                    <p className={`${!isUser ? 'text-black' : 'text-black'}`}>{children}</p>
                )}
            </div>
        </div>
    )
}