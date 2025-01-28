"use client"
import Link from 'next/link'
import { usePathname } from 'next/navigation'

export default function NavBar() {
    const pathname = usePathname()
    return (
        <div className="flex justify-center items-center w-full bg-yellow-100 p-4 border-b border-gray-200">
            <div className="flex justify-center items-center space-x-4">
                <Link href="/" className={pathname === '/' ? 'bg-slate-200 p-2 rounded-full' : ''}>
                    <h1 className="text-2xl font-bold">Chat with me</h1>
                </Link>
                <Link href="/admin" className={pathname === '/admin' ? 'bg-slate-200 p-2 rounded-full' : ''}>
                    <h1 className="text-2xl font-bold">View Chat History</h1>
                </Link>
            </div>
            
        </div>
    )
}