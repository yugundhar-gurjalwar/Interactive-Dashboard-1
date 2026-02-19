import React from 'react';
import { Activity, MessageSquare, Database, Sparkles } from 'lucide-react';

const DashboardHome = () => {
    return (
        <div className="p-8 h-full overflow-y-auto">
            <div className="max-w-7xl mx-auto space-y-8">
                {/* Header Section */}
                <div className="flex items-end justify-between">
                    <div>
                        <h1 className="text-4xl font-bold tracking-tight bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
                            Dashboard
                        </h1>
                        <p className="text-gray-400 mt-2 text-lg">
                            Welcome back. Your AI assistant is ready.
                        </p>
                    </div>
                    <div className="px-4 py-2 bg-blue-500/10 border border-blue-500/20 rounded-full text-blue-400 text-sm font-medium flex items-center gap-2">
                        <span className="relative flex h-2 w-2">
                            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                            <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-500"></span>
                        </span>
                        System Online
                    </div>
                </div>

                {/* Stats Grid */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="p-6 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-xl hover:bg-white/10 transition-colors group">
                        <div className="flex items-center justify-between mb-4">
                            <h3 className="font-medium text-gray-200">Recent Chats</h3>
                            <div className="p-2 bg-purple-500/20 rounded-lg text-purple-400 group-hover:bg-purple-500/30 transition-colors">
                                <MessageSquare size={20} />
                            </div>
                        </div>
                        <div className="space-y-1">
                            <span className="text-3xl font-bold text-white">0</span>
                            <p className="text-sm text-gray-400">Conversations today</p>
                        </div>
                    </div>

                    <div className="p-6 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-xl hover:bg-white/10 transition-colors group">
                        <div className="flex items-center justify-between mb-4">
                            <h3 className="font-medium text-gray-200">Memory Bank</h3>
                            <div className="p-2 bg-emerald-500/20 rounded-lg text-emerald-400 group-hover:bg-emerald-500/30 transition-colors">
                                <Database size={20} />
                            </div>
                        </div>
                        <div className="space-y-1">
                            <span className="text-3xl font-bold text-white">Active</span>
                            <p className="text-sm text-gray-400">Vector store connected</p>
                        </div>
                    </div>

                    <div className="p-6 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-xl hover:bg-white/10 transition-colors group">
                        <div className="flex items-center justify-between mb-4">
                            <h3 className="font-medium text-gray-200">System Health</h3>
                            <div className="p-2 bg-blue-500/20 rounded-lg text-blue-400 group-hover:bg-blue-500/30 transition-colors">
                                <Activity size={20} />
                            </div>
                        </div>
                        <div className="space-y-1">
                            <span className="text-3xl font-bold text-white">100%</span>
                            <p className="text-sm text-gray-400">Operational</p>
                        </div>
                    </div>
                </div>

                {/* Main Content Area - Just a placeholder for now */}
                <div className="rounded-3xl border border-white/10 bg-white/5 backdrop-blur-md p-8 min-h-[400px] flex flex-col items-center justify-center text-center space-y-4">
                    <div className="p-4 bg-white/5 rounded-full">
                        <Sparkles size={48} className="text-gray-500" />
                    </div>
                    <h2 className="text-xl font-medium text-white">Ready for your next task</h2>
                    <p className="text-gray-400 max-w-md">
                        Navigate to the Chat tab to start a new conversation, or manage your AI's knowledge in the Memory section.
                    </p>
                    <button className="px-6 py-2 bg-white text-black font-semibold rounded-full hover:bg-gray-200 transition-colors">
                        Start Chatting
                    </button>
                </div>
            </div>
        </div>
    );
};

export default DashboardHome;
