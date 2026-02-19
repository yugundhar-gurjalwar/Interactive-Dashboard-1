import React, { useState, useEffect, useRef } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Send, PlusCircle, MessageSquare, Trash2 } from 'lucide-react';
import api from '../services/api';

interface Message {
    role: 'user' | 'assistant';
    content: string;
}

interface Conversation {
    id: number;
    title: string;
}

const ChatInterface: React.FC = () => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [conversations, setConversations] = useState<Conversation[]>([]);
    const [currentConversationId, setCurrentConversationId] = useState<number | null>(null);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    useEffect(() => {
        fetchConversations();
    }, []);

    const fetchConversations = async () => {
        try {
            const response = await api.get('/conversations/');
            setConversations(response.data);
        } catch (error) {
            console.error("Failed to fetch conversations", error);
        }
    };

    const loadConversation = async (id: number) => {
        try {
            setCurrentConversationId(id);
            const response = await api.get(`/conversations/${id}`);
            if (response.data.messages) {
                setMessages(response.data.messages.map((m: any) => ({ role: m.role, content: m.content })));
            } else {
                setMessages([]);
            }
        } catch (error) {
            console.error("Failed to load conversation", error);
        }
    };

    const deleteConversation = async (e: React.MouseEvent, id: number) => {
        e.stopPropagation();
        try {
            await api.delete(`/conversations/${id}`);
            setConversations(prev => prev.filter(c => c.id !== id));
            if (currentConversationId === id) {
                startNewChat();
            }
        } catch (error) {
            console.error("Failed to delete conversation", error);
        }
    };

    const startNewChat = () => {
        setCurrentConversationId(null);
        setMessages([]);
    };

    const [models, setModels] = useState<string[]>([]);
    const [selectedModel, setSelectedModel] = useState<string>('llama3');

    useEffect(() => {
        fetchModels();
    }, []);

    const fetchModels = async () => {
        try {
            const response = await api.get('/models/');
            if (response.data && response.data.models) {
                const modelNames = response.data.models.map((m: any) => m.name);
                setModels(modelNames);
                if (modelNames.includes('llama3')) {
                    setSelectedModel('llama3');
                } else if (modelNames.length > 0) {
                    setSelectedModel(modelNames[0]);
                }
            }
        } catch (error) {
            console.error("Failed to fetch models", error);
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || isLoading) return;

        const userMessage: Message = { role: 'user', content: input };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/chat/completions`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({
                    messages: [...messages, userMessage],
                    stream: true,
                    conversation_id: currentConversationId,
                    model: selectedModel
                })
            });

            if (response.status === 401) {
                localStorage.removeItem('token');
                window.location.reload();
                return;
            }
            if (!response.ok) throw new Error('Network response was not ok');
            if (!response.body) throw new Error('No body');

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let assistantMessage = { role: 'assistant', content: '' };

            setMessages(prev => [...prev, assistantMessage as Message]);

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value);
                assistantMessage.content += chunk;

                setMessages(prev => {
                    const newMessages = [...prev];
                    newMessages[newMessages.length - 1] = { ...assistantMessage as Message };
                    return newMessages;
                });
            }

            // Refresh conversations list if new chat
            if (!currentConversationId) {
                fetchConversations();
            }
        } catch (error) {
            console.error('Error:', error);
            console.error('Error:', error);
            const errorMessage = error instanceof Error ? error.message : 'Failed to fetch response';
            setMessages(prev => [...prev, { role: 'assistant', content: `Error: ${errorMessage}. Make sure Ollama is running.` }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex h-[calc(100vh-4rem)]">
            {/* Sidebar for Conversations */}
            <div className="w-64 bg-black border-r border-gray-800 p-4 flex flex-col text-white">
                <Button onClick={startNewChat} className="mb-4 w-full flex items-center justify-center gap-2" variant="outline">
                    <PlusCircle size={16} /> New Chat
                </Button>
                <div className="flex-1 overflow-y-auto space-y-2">
                    {conversations.map(conv => (
                        <div
                            key={conv.id}
                            onClick={() => loadConversation(conv.id)}
                            className={`group p-3 text-sm rounded cursor-pointer hover:bg-gray-800 flex justify-between items-center ${currentConversationId === conv.id ? 'bg-gray-800 font-medium' : ''}`}
                        >
                            <span className="truncate flex-1">{conv.title}</span>
                            <Trash2
                                size={14}
                                className="opacity-0 group-hover:opacity-100 text-gray-500 hover:text-red-500"
                                onClick={(e) => deleteConversation(e, conv.id)}
                            />
                        </div>
                    ))}
                </div>
            </div>

            {/* Chat Area */}
            <div className="flex-1 flex flex-col max-w-4xl mx-auto w-full p-4">
                <div className="flex justify-between items-center mb-2 px-2">
                    <span className="text-sm font-medium text-gray-500">Model:</span>
                    <select
                        value={selectedModel}
                        onChange={(e) => setSelectedModel(e.target.value)}
                        className="bg-black text-white border border-gray-800 rounded px-2 py-1 text-sm outline-none focus:ring-1 focus:ring-blue-500"
                    >
                        {models.map(m => (
                            <option key={m} value={m}>{m}</option>
                        ))}
                    </select>
                </div>
                <div className="flex-1 overflow-y-auto space-y-4 mb-4 p-4 border rounded-lg bg-black text-white dark:border-gray-700 shadow-sm custom-scrollbar">
                    {messages.length === 0 && (
                        <div className="text-center text-gray-500 mt-10">
                            <MessageSquare size={48} className="mx-auto mb-4 opacity-20" />
                            <p>Start a new conversation with the AI.</p>
                        </div>
                    )}
                    {messages.map((msg, idx) => (
                        <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                            <div className={`max-w-[80%] rounded-lg p-3 ${msg.role === 'user'
                                ? 'bg-blue-600 text-white'
                                : 'bg-gray-800 text-white border border-gray-700'
                                }`}>
                                {msg.content}
                            </div>
                        </div>
                    ))}
                    <div ref={messagesEndRef} />
                </div>

                <form onSubmit={handleSubmit} className="flex gap-2">
                    <Input
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Type your message..."
                        className="flex-1"
                        disabled={isLoading}
                    />
                    <Button type="submit" disabled={isLoading || !input.trim()}>
                        <Send className="w-4 h-4" />
                    </Button>
                </form>
            </div>
        </div>
    );
};

export default ChatInterface;
