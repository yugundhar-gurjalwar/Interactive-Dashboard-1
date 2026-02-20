import React from 'react';
import { HashRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Layout from './components/Layout';
import DashboardHome from './pages/DashboardHome';
import ChatInterface from './components/ChatInterface';
import MemoryPage from './pages/MemoryPage';
import ToolsPage from './pages/ToolsPage';
import SettingsPage from './pages/SettingsPage';

const App = () => {
  return (
    <HashRouter>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Navigate to="/dashboard" />} />
            <Route path="dashboard" element={<DashboardHome />} />
            <Route path="chat" element={<ChatInterface />} />
            <Route path="memory" element={<MemoryPage />} />
            <Route path="tools" element={<ToolsPage />} />
            <Route path="settings" element={<SettingsPage />} />
          </Route>
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </AuthProvider>
    </HashRouter>
  );
};

export default App;
