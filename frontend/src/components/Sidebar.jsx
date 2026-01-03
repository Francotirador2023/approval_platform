import { NavLink } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useAuth } from '../context/AuthContext';

// Icons (Using simple SVGs or Heroicons equivalent)
const HomeIcon = ({ className }) => (
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className={className}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
    </svg>
);

const UserGroupIcon = ({ className }) => (
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className={className}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M18 18.72a9.094 9.094 0 003.741-.479 3 3 0 00-4.682-2.72m.94 3.198l.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0112 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 016 18.719m12 0a5.971 5.971 0 00-.941-3.197m0 0A5.995 5.995 0 0012 12.75a5.995 5.995 0 00-5.058 5.472m0 0a9.09 9.09 0 00-3.26.693 2.75 2.75 0 01-3.566 3.566 3 3 0 003.566-3.566z" />
        <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 5.25a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z" />
    </svg>
);

const LogoutIcon = ({ className }) => (
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className={className}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75" />
    </svg>
);

const Sidebar = ({ isOpen, setIsOpen }) => {
    const { user, logout } = useAuth();

    return (
        <>
            {/* Mobile backdrop */}
            <div
                className={`fixed inset-0 z-20 bg-gray-900/50 transition-opacity lg:hidden ${isOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'
                    }`}
                onClick={() => setIsOpen(false)}
            />

            {/* Sidebar component */}
            <div
                className={`fixed inset-y-0 left-0 z-30 w-64 bg-slate-900 text-white transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-auto ${isOpen ? 'translate-x-0' : '-translate-x-full'
                    }`}
            >
                <div className="flex flex-col h-full">
                    {/* Logo */}
                    <div className="flex items-center justify-center h-16 px-4 bg-slate-950 shadow-sm overflow-hidden">
                        <motion.span
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ duration: 0.5, type: "spring" }}
                            className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-cyan-400"
                        >
                            ApprovalFlow
                        </motion.span>
                    </div>

                    {/* Navigation */}
                    <nav className="flex-1 px-4 py-6 space-y-1">
                        <NavLink
                            to="/"
                            className={({ isActive }) =>
                                `flex items-center px-4 py-3 text-sm font-medium rounded-xl transition-all duration-200 ${isActive
                                    ? 'bg-indigo-600/10 text-indigo-400 shadow-sm ring-1 ring-inset ring-indigo-500/20'
                                    : 'text-slate-400 hover:bg-slate-800 hover:text-white'
                                }`
                            }
                        >
                            <HomeIcon className="w-5 h-5 mr-3" />
                            Dashboard
                            {/* Active Indicator */}
                            {({ isActive }) => isActive && (
                                <motion.div
                                    layoutId="activeTab"
                                    className="absolute left-0 w-1 h-8 bg-indigo-500 rounded-r-full"
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    transition={{ duration: 0.3 }}
                                />
                            )}
                        </NavLink>

                        {user?.role === 'admin' && (
                            <NavLink
                                to="/admin"
                                className={({ isActive }) =>
                                    `relative flex items-center px-4 py-3 text-sm font-medium rounded-xl transition-all duration-200 ${isActive
                                        ? 'bg-indigo-600/10 text-indigo-400 shadow-sm ring-1 ring-inset ring-indigo-500/20'
                                        : 'text-slate-400 hover:bg-slate-800 hover:text-white'
                                    }`
                                }
                            >
                                <UserGroupIcon className="w-5 h-5 mr-3" />
                                Admin Panel
                                {({ isActive }) => isActive && (
                                    <motion.div
                                        layoutId="activeTab"
                                        className="absolute left-0 w-1 h-8 bg-indigo-500 rounded-r-full"
                                        initial={{ opacity: 0 }}
                                        animate={{ opacity: 1 }}
                                        transition={{ duration: 0.3 }}
                                    />
                                )}
                            </NavLink>
                        )}
                    </nav>

                    {/* User Profile & Logout */}
                    <div className="p-4 bg-slate-950/50 border-t border-slate-800">
                        <div className="flex items-center gap-3 mb-4">
                            <div className="flex items-center justify-center w-8 h-8 rounded-full bg-indigo-500 text-white font-bold text-xs">
                                {user?.full_name?.charAt(0) || 'U'}
                            </div>
                            <div className="overflow-hidden">
                                <p className="text-sm font-medium text-white truncate">{user?.full_name}</p>
                                <p className="text-xs text-slate-500 truncate capitalize">{user?.role}</p>
                            </div>
                        </div>
                        <button
                            onClick={logout}
                            className="flex items-center justify-center w-full px-4 py-2 text-sm text-slate-400 transition-colors rounded-lg hover:bg-slate-800 hover:text-rose-400"
                        >
                            <LogoutIcon className="w-4 h-4 mr-2" />
                            Cerrar Sesión
                        </button>
                    </div>
                </div>
            </div>
        </>
    );
};

export default Sidebar;
