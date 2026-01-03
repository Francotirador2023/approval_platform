import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';
import { useAuth } from '../context/AuthContext';

const AdminPanel = () => {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const { user } = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        if (user && user.role !== 'admin') {
            navigate('/');
            return;
        }
        fetchUsers();
    }, [user, navigate]);

    const fetchUsers = async () => {
        try {
            setLoading(true);
            const response = await api.get('/users/');
            setUsers(response.data);
        } catch (error) {
            console.error("Failed to fetch users", error);
            alert("Failed to fetch users");
        } finally {
            setLoading(false);
        }
    };

    const handleRoleChange = async (userId, newRole) => {
        if (!confirm(`¿Estás seguro de que deseas cambiar el rol de este usuario a ${newRole}?`)) return;

        try {
            await api.put(`/users/${userId}/role`, { role: newRole });
            // Optimistic update or refetch
            setUsers(users.map(u => u.id === userId ? { ...u, role: newRole } : u));
        } catch (error) {
            console.error("Failed to update role", error);
            alert("Error al actualizar rol: " + (error.response?.data?.detail || error.message));
        }
    };

    return (
        <div className="min-h-screen bg-gray-50 font-sans text-gray-900">
            <nav className="bg-white shadow">
                <div className="px-4 mx-auto max-w-7xl sm:px-6 lg:px-8">
                    <div className="flex justify-between h-16">
                        <div className="flex items-center">
                            <h1 className="text-2xl font-bold text-gray-900">Panel de Administración</h1>
                        </div>
                        <div className="flex items-center">
                            <button
                                onClick={() => navigate('/dashboard')}
                                className="text-indigo-600 hover:text-indigo-900 font-medium"
                            >
                                &larr; Volver al Tablero
                            </button>
                        </div>
                    </div>
                </div>
            </nav>

            <main className="py-10 mx-auto max-w-7xl sm:px-6 lg:px-8">
                <div className="flex flex-col">
                    <div className="-my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
                        <div className="py-2 align-middle inline-block min-w-full sm:px-6 lg:px-8">
                            <div className="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg">
                                {loading ? (
                                    <div className="flex justify-center py-10">
                                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
                                    </div>
                                ) : (
                                    <table className="min-w-full divide-y divide-gray-200 bg-white">
                                        <thead className="bg-gray-50">
                                            <tr>
                                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                                    Info Usuario
                                                </th>
                                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                                    Rol Actual
                                                </th>
                                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                                    Acciones
                                                </th>
                                            </tr>
                                        </thead>
                                        <tbody className="bg-white divide-y divide-gray-200">
                                            {users.map((person) => (
                                                <tr key={person.id}>
                                                    <td className="px-6 py-4 whitespace-nowrap">
                                                        <div className="flex items-center">
                                                            <div>
                                                                <div className="text-sm font-medium text-gray-900">
                                                                    {person.full_name}
                                                                </div>
                                                                <div className="text-sm text-gray-500">
                                                                    {person.email}
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </td>
                                                    <td className="px-6 py-4 whitespace-nowrap">
                                                        <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${person.role === 'admin' ? 'bg-purple-100 text-purple-800' :
                                                            person.role === 'manager' ? 'bg-green-100 text-green-800' :
                                                                'bg-gray-100 text-gray-800'
                                                            }`}>
                                                            {person.role.toUpperCase()}
                                                        </span>
                                                    </td>
                                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                                        <select
                                                            value={person.role}
                                                            onChange={(e) => handleRoleChange(person.id, e.target.value)}
                                                            className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                                                            disabled={person.id === user?.id} // Prevent self-demotion lockout risk
                                                        >
                                                            <option value="employee">Empleado</option>
                                                            <option value="manager">Gerente</option>
                                                            <option value="admin">Admin</option>
                                                        </select>
                                                    </td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
};

export default AdminPanel;
