import React from 'react';
import { useAuth } from '../context/AuthContext';
import { Home, MessageSquare, Settings, Brain, Wrench } from 'lucide-react';
import { cn } from '../lib/utils';
import { Link, useLocation } from 'react-router-dom';

const navItems = [
    { name: 'Dashboard', icon: Home, path: '/dashboard' },
    { name: 'Chat', icon: MessageSquare, path: '/chat' },
    { name: 'Memory', icon: Brain, path: '/memory' },
    { name: 'Tools', icon: Wrench, path: '/tools' },
    { name: 'Settings', icon: Settings, path: '/settings' },
];

const Sidebar = () => {
    const location = useLocation();

    return (
        <div className="flex flex-col h-screen w-64 bg-gray-900 text-white border-r border-gray-800">
            <div className="p-6 border-b border-gray-800">
                <h1 className="text-xl font-bold flex items-center gap-2">
                    <span className="text-blue-500">Pocket</span>Paw
                </h1>
            </div>

            <nav className="flex-1 p-4 space-y-2">
                {navItems.map((item) => (
                    <Link
                        key={item.path}
                        to={item.path}
                        className={cn(
                            "flex items-center gap-3 px-4 py-3 rounded-lg transition-colors",
                            location.pathname === item.path
                                ? "bg-blue-600 text-white"
                                : "text-gray-400 hover:bg-gray-800 hover:text-white"
                        )}
                    >
                        <item.icon size={20} />
                        <span>{item.name}</span>
                    </Link>
                ))}
            </nav>

        </div>
    );
};

export default Sidebar;
