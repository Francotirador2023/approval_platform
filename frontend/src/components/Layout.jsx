import { useState } from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import NotificationBell from './NotificationBell';

const Layout = () => {
    const [sidebarOpen, setSidebarOpen] = useState(false);

    return (
        <div className="flex min-h-screen bg-slate-50">
            <Sidebar isOpen={sidebarOpen} setIsOpen={setSidebarOpen} />

            <div className="flex-1 flex flex-col min-w-0 transition-all duration-300">
                {/* Mobile Header */}
                <header className="lg:hidden flex items-center justify-between h-16 px-4 bg-white border-b border-slate-200 shadow-sm sticky top-0 z-10">
                    <button
                        onClick={() => setSidebarOpen(true)}
                        className="p-2 text-slate-500 rounded-md hover:bg-slate-100 focus:outline-none"
                    >
                        <span className="sr-only">Open sidebar</span>
                        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                        </svg>
                    </button>
                    <span className="font-bold text-slate-900">ApprovalFlow</span>
                    <NotificationBell />
                </header>

                {/* Desktop Header area if needed, or just spacers */}
                {/* For now we keep notifications in sidebar or floating, but let's put Bell in a top bar for desktop too for convenience */}
                <div className="hidden lg:flex items-center justify-end h-16 px-8 bg-white/80 backdrop-blur border-b border-slate-200 sticky top-0 z-10">
                    <NotificationBell />
                </div>

                <main className="flex-1 p-4 sm:p-6 lg:p-8 overflow-y-auto">
                    <div className="max-w-7xl mx-auto">
                        <Outlet />
                    </div>
                </main>
            </div>
        </div>
    );
};

export default Layout;
