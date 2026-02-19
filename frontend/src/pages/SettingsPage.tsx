import React from 'react';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';

const SettingsPage: React.FC = () => {
    return (
        <div className="p-6 max-w-2xl text-white">
            <h1 className="text-2xl font-bold mb-6">Settings</h1>

            <div className="space-y-6">
                <div className="p-4 bg-black border border-gray-800 rounded-lg shadow">
                    <h2 className="text-lg font-semibold mb-4">General Settings</h2>
                    <div className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium mb-1">Display Name</label>
                            <Input placeholder="Guest User" disabled />
                        </div>
                        <div>
                            <label className="block text-sm font-medium mb-1">Email</label>
                            <Input placeholder="guest@example.com" disabled />
                        </div>
                    </div>
                </div>

                <div className="p-4 bg-black border border-gray-800 rounded-lg shadow">
                    <h2 className="text-lg font-semibold mb-4">Appearance</h2>
                    <div className="flex items-center justify-between">
                        <span>Dark Mode</span>
                        <Button variant="outline" disabled>Auto (System)</Button>
                    </div>
                </div>

                <div className="p-4 bg-black border border-gray-800 rounded-lg shadow border-l-4 border-l-red-500">
                    <h2 className="text-lg font-semibold mb-2 text-red-500">Danger Zone</h2>
                    <p className="text-sm text-gray-400 mb-4">Irreversible actions.</p>
                    <Button variant="destructive">Delete Account</Button>
                </div>
            </div>
        </div>
    );
};

export default SettingsPage;
