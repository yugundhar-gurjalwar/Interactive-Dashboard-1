import React from 'react';
import Sidebar from './Sidebar';
import { Outlet } from 'react-router-dom';

const Layout = () => {
    return (
        <div className="flex h-screen w-screen overflow-hidden bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-gray-900 via-[#0a0a0a] to-black text-white">
            <Sidebar />
            <main className="flex-1 overflow-hidden h-full relative">
                {/* Background Grid Pattern */}
                <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 pointer-events-none mix-blend-soft-light"></div>
                <div className="absolute inset-0 bg-grid-white/[0.02] -z-10" />

                <Outlet />
            </main>
        </div>
    );
};

export default Layout;
