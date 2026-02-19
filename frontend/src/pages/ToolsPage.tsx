import React, { useEffect, useState } from 'react';
import api from '../services/api';

const ToolsPage: React.FC = () => {
    const [models, setModels] = useState<any[]>([]);

    useEffect(() => {
        fetchModels();
    }, []);

    const fetchModels = async () => {
        try {
            const response = await api.get('/models/');
            if (response.data && response.data.models) {
                setModels(response.data.models);
            }
        } catch (error) {
            console.error("Failed to fetch models", error);
        }
    };

    return (
        <div className="p-6 text-white">
            <h1 className="text-2xl font-bold mb-4">Agent Tools & Models</h1>

            <section className="mb-8">
                <h2 className="text-xl font-semibold mb-3">Installed Ollama Models</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {models.length === 0 ? (
                        <p className="text-gray-500">No models found or Ollama is offline.</p>
                    ) : (
                        models.map((model: any) => (
                            <div key={model.name} className="p-4 border border-gray-800 rounded-lg bg-black shadow-sm">
                                <div className="flex justify-between items-center mb-2">
                                    <h3 className="font-semibold truncate" title={model.name}>{model.name}</h3>
                                    <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">Installed</span>
                                </div>
                                <p className="text-xs text-gray-500">Modified: {new Date(model.modified_at).toLocaleDateString()}</p>
                                <p className="text-xs text-gray-500">Size: {(model.size / 1024 / 1024 / 1024).toFixed(2)} GB</p>
                            </div>
                        ))
                    )}
                </div>
            </section>

            <section>
                <h2 className="text-xl font-semibold mb-3">Active Tools</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {['Web Search', 'Calculator', 'Note Taker', 'Reminder', 'File Reader', 'Website Reader'].map(tool => (
                        <div key={tool} className="p-4 border border-gray-800 rounded-lg bg-black shadow-sm opacity-75">
                            <div className="flex justify-between items-center mb-2">
                                <h3 className="font-semibold">{tool}</h3>
                                <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">Active</span>
                            </div>
                            <p className="text-sm text-gray-500">Enabled for all conversations.</p>
                        </div>
                    ))}
                </div>
            </section>
        </div>
    );
};

export default ToolsPage;
