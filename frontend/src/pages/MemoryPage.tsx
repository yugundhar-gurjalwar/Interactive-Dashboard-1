import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Trash2, Plus, Search } from 'lucide-react';

interface Memory {
    id: number;
    text: string;
    created_at: string;
}

const MemoryPage: React.FC = () => {
    const [memories, setMemories] = useState<Memory[]>([]);
    const [newMemory, setNewMemory] = useState('');
    const [searchQuery, setSearchQuery] = useState('');
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        fetchMemories();
    }, []);

    const fetchMemories = async () => {
        try {
            setLoading(true);
            const response = await api.get('/memory/');
            setMemories(response.data);
        } catch (error) {
            console.error("Failed to fetch memories", error);
        } finally {
            setLoading(false);
        }
    };

    const handleAddMemory = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!newMemory.trim()) return;

        try {
            const response = await api.post('/memory/', { text: newMemory });
            setMemories([response.data, ...memories]);
            setNewMemory('');
        } catch (error) {
            console.error("Failed to add memory", error);
        }
    };

    const handleDeleteMemory = async (id: number) => {
        if (!window.confirm("Are you sure you want to delete this memory?")) return;
        try {
            await api.delete(`/memory/${id}`);
            setMemories(memories.filter(m => m.id !== id));
        } catch (error) {
            console.error("Failed to delete memory", error);
        }
    };

    const handleSearch = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!searchQuery.trim()) {
            fetchMemories();
            return;
        }
        try {
            setLoading(true);
            const response = await api.post('/memory/search', { query: searchQuery });
            // Search returns a different format (from vector store), adapting basic display
            // Ideally backend search should allow returning full objects or we adapt here.
            // Vector search returns dicts with 'text', 'metadata', 'id'.
            // Our local state expects Memory interface.
            const searchResults = response.data.map((item: any) => ({
                id: item.id, // ID might be string from vector store, but we use int in SQL. Vector store ID is str(int).
                text: item.text,
                created_at: item.metadata?.created_at || new Date().toISOString()
            }));
            setMemories(searchResults);
        } catch (error) {
            console.error("Failed to search memories", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-6 max-w-4xl mx-auto text-white">
            <h1 className="text-2xl font-bold mb-6">Memory Management</h1>

            {/* Add Memory */}
            <div className="mb-8 p-4 bg-black border border-gray-800 rounded-lg shadow">
                <h2 className="text-lg font-semibold mb-2">Add New Memory</h2>
                <form onSubmit={handleAddMemory} className="flex gap-2">
                    <Input
                        value={newMemory}
                        onChange={(e) => setNewMemory(e.target.value)}
                        placeholder="What should I remember?"
                        className="flex-1"
                    />
                    <Button type="submit">
                        <Plus className="w-4 h-4 mr-2" /> Add
                    </Button>
                </form>
            </div>

            {/* Search */}
            <div className="mb-6 flex gap-2">
                <Input
                    value={searchQuery}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => setSearchQuery(e.target.value)}
                    placeholder="Search memories..."
                    className="flex-1"
                />
                <Button variant="outline" onClick={handleSearch}>
                    <Search className="w-4 h-4 mr-2" /> Search
                </Button>
            </div>

            {/* List */}
            <div className="space-y-2">
                {loading ? (
                    <p>Loading...</p>
                ) : memories.length === 0 ? (
                    <p className="text-gray-500">No memories found.</p>
                ) : (
                    memories.map(memory => (
                        <div key={memory.id} className="p-4 bg-black border border-gray-800 rounded-lg shadow flex justify-between items-start">
                            <div>
                                <p className="whitespace-pre-wrap">{memory.text}</p>
                                <span className="text-xs text-gray-400">{new Date(memory.created_at).toLocaleString()}</span>
                            </div>
                            <Button variant="ghost" size="icon" onClick={() => handleDeleteMemory(memory.id)} className="text-red-500 hover:text-red-700 hover:bg-red-50">
                                <Trash2 className="w-4 h-4" />
                            </Button>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
};

export default MemoryPage;
