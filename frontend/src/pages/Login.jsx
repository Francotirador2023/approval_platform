import { useState } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const { login } = useAuth();
    const navigate = useNavigate();
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await login(email, password);
            navigate('/');
        } catch (err) {
            setError('Correo o contraseña inválidos');
        }
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-slate-50 relative overflow-hidden">
            {/* Background Decoration */}
            <div className="absolute top-0 left-0 w-full h-full bg-white">
                <div className="absolute top-0 left-0 w-full h-96 bg-gradient-to-br from-indigo-600 to-violet-600 skew-y-6 transform origin-top-left -translate-y-20"></div>
                <div className="absolute bottom-0 right-0 w-96 h-96 bg-indigo-50 rounded-full blur-3xl opacity-50 -translate-x-20 translate-y-20"></div>
            </div>

            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="w-full max-w-md p-8 bg-white/90 backdrop-blur-lg rounded-2xl shadow-xl border border-white/20 relative z-10"
            >
                <div className="text-center mb-8">
                    <motion.h1
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: 0.2, duration: 0.4 }}
                        className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-violet-600"
                    >
                        Plataforma de Aprobación
                    </motion.h1>
                    <motion.p
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.3 }}
                        className="text-slate-500 mt-2 text-sm"
                    >
                        Gestiona tus solicitudes de forma eficiente
                    </motion.p>
                </div>

                <h2 className="text-xl font-semibold text-center text-slate-800 mb-6">Inicia sesión</h2>

                {error && (
                    <div className="p-3 mb-6 text-sm text-red-600 bg-red-50 border border-red-100 rounded-lg flex items-center">
                        <svg className="w-4 h-4 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                        </svg>
                        {error}
                    </div>
                )}

                <form className="space-y-5" onSubmit={handleSubmit}>
                    <div>
                        <label htmlFor="email" className="block text-sm font-medium text-slate-700 mb-1">
                            Correo electrónico
                        </label>
                        <input
                            id="email"
                            name="email"
                            type="email"
                            required
                            className="w-full px-4 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition-all duration-200"
                            placeholder="tu@correo.com"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                    </div>
                    <div>
                        <label htmlFor="password" className="block text-sm font-medium text-slate-700 mb-1">
                            Contraseña
                        </label>
                        <input
                            id="password"
                            name="password"
                            type="password"
                            required
                            className="w-full px-4 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition-all duration-200"
                            placeholder="••••••••"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                    </div>
                    <div>
                        <motion.button
                            whileHover={{ scale: 1.02, boxShadow: "0 10px 25px -5px rgba(79, 70, 229, 0.4)" }}
                            whileTap={{ scale: 0.98 }}
                            type="submit"
                            className="w-full px-4 py-3 font-semibold text-white bg-gradient-to-r from-indigo-600 to-violet-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 shadow-lg shadow-indigo-500/30 transition-all duration-200"
                        >
                            Iniciar sesión
                        </motion.button>
                    </div>
                </form>

                <div className="mt-6 text-center text-xs text-slate-400">
                    &copy; {new Date().getFullYear()} Approval Platform. All rights reserved.
                </div>
            </motion.div>
        </div>
    );
};

export default Login;
