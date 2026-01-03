import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../api';
import RequestForm from '../components/RequestForm';
import ActivityLog from '../components/ActivityLog';
import NotificationBell from '../components/NotificationBell';

const Dashboard = () => {
    const { user } = useAuth();
    const navigate = useNavigate();
    const [requests, setRequests] = useState([]);
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState('pending');
    const [statusFilter, setStatusFilter] = useState('all'); // 'all', 'approved', 'rejected'
    const [refreshTrigger, setRefreshTrigger] = useState(0);

    const handleRequestCreated = () => {
        setRefreshTrigger(prev => prev + 1);
        fetchRequests();
    };

    const fetchRequests = async () => {
        try {
            setLoading(true);
            // Fetch all requests to allow client-side filtering by date
            const response = await api.get('/requests/');
            setRequests(response.data);
        } catch (error) {
            console.error("Failed to fetch requests", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchRequests();
    }, [refreshTrigger]);

    // Reset status filter when changing tabs
    useEffect(() => {
        setStatusFilter('all');
    }, [activeTab]);

    const handleStatusUpdate = async (id, status, comment = "") => {
        try {
            await api.put(`/requests/${id}/status`, { status, comment });
            fetchRequests();
        } catch (error) {
            console.error("Failed to update status", error);
            alert("Error al actualizar estado: " + (error.response?.data?.detail || error.message));
        }
    };

    const tabs = [
        { id: 'pending', name: 'Pendientes' },
        { id: 'recent', name: 'Recientes (48h)' },
        { id: 'history', name: 'Historial' },
    ];

    const getFilteredRequests = () => {
        const now = new Date();
        const fortyEightHoursAgo = new Date(now.getTime() - 48 * 60 * 60 * 1000);

        return requests.filter(req => {
            const reqDate = new Date(req.created_at);
            let matchesTab = false;

            if (activeTab === 'pending') {
                matchesTab = req.status === 'pending';
            } else if (activeTab === 'recent') {
                // Approved or Rejected within last 48 hours
                matchesTab = req.status !== 'pending' && reqDate >= fortyEightHoursAgo;
            } else if (activeTab === 'history') {
                // Approved or Rejected older than 48 hours
                matchesTab = req.status !== 'pending' && reqDate < fortyEightHoursAgo;
            }

            if (!matchesTab) return false;

            // Secondary status filter (only for recent/history)
            if (activeTab !== 'pending') {
                if (statusFilter === 'approved' && req.status !== 'approved') return false;
                if (statusFilter === 'rejected' && req.status !== 'rejected') return false;
            }

            return true;
        });
    };

    const filteredRequests = getFilteredRequests();


    return (
        <div className="space-y-6 animate-fade-in-up">
            {/* Page Header */}
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                <div>
                    <h1 className="text-2xl font-bold text-slate-800 tracking-tight">Dashboard</h1>
                    <p className="text-slate-500">Bienvenido de nuevo, {user?.full_name}</p>
                </div>
                <div className="flex items-center gap-3">
                    <button
                        onClick={async () => {
                            const btn = document.getElementById('sync-btn');
                            try {
                                btn.disabled = true;
                                btn.innerHTML = '<span class="animate-spin inline-block mr-2">↻</span> Sincronizando...';
                                await api.post('/sync-emails');
                                handleRequestCreated(); // Refresh list
                            } catch (error) {
                                console.error(error);
                                alert('Error al sincronizar correos');
                            } finally {
                                btn.disabled = false;
                                btn.innerHTML = 'Sincronizar Correos';
                            }
                        }}
                        id="sync-btn"
                        className="inline-flex items-center px-4 py-2 bg-white border border-slate-300 rounded-lg text-sm font-medium text-slate-700 hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 shadow-sm transition-all"
                    >
                        Sincronizar Correos
                    </button>
                    <button
                        onClick={() => navigate('/admin')}
                        className={`inline-flex items-center px-4 py-2 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all ${user?.role !== 'admin' ? 'hidden' : ''}`}
                    >
                        Panel Admin
                    </button>
                </div>
            </div>

            {/* Content Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Left Column: Create Form */}
                <div className="lg:col-span-1">
                    <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 sticky top-6">
                        <div className="flex items-center space-x-3 mb-6">
                            <div className="p-2 bg-indigo-50 rounded-lg">
                                <svg className="w-6 h-6 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                                </svg>
                            </div>
                            <h2 className="text-lg font-bold text-slate-900">Nueva Solicitud</h2>
                        </div>
                        <RequestForm onRequestCreated={handleRequestCreated} />
                    </div>
                </div>

                {/* Right Column: List */}
                <div className="lg:col-span-2 space-y-6">
                    <div className="flex flex-col space-y-3">
                        {/* Main Tabs */}
                        <div className="flex p-1 space-x-1 bg-white/50 backdrop-blur rounded-xl border border-slate-200 w-fit">
                            {tabs.map((tab) => (
                                <button
                                    key={tab.id}
                                    onClick={() => setActiveTab(tab.id)}
                                    className={`px-4 py-2 text-sm font-medium rounded-lg transition-all duration-200 ${activeTab === tab.id
                                        ? 'bg-white text-indigo-600 shadow-sm ring-1 ring-slate-200'
                                        : 'text-slate-500 hover:text-slate-700 hover:bg-white/50'
                                        }`}
                                >
                                    {tab.name}
                                </button>
                            ))}
                        </div>

                        {/* Sub-filters for Recent/History */}
                        {activeTab !== 'pending' && (
                            <div className="flex items-center space-x-2 animate-fade-in">
                                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider mr-2">Filtrar por:</span>
                                {[
                                    { id: 'all', label: 'Todos' },
                                    { id: 'approved', label: 'Aprobados', color: 'text-emerald-600 bg-emerald-50 border-emerald-100' },
                                    { id: 'rejected', label: 'Rechazados', color: 'text-rose-600 bg-rose-50 border-rose-100' }
                                ].map(filter => (
                                    <button
                                        key={filter.id}
                                        onClick={() => setStatusFilter(filter.id)}
                                        className={`px-3 py-1 text-xs font-medium rounded-full border transition-all ${statusFilter === filter.id
                                            ? (filter.color || 'bg-slate-100 text-slate-700 border-slate-200 shadow-sm')
                                            : 'bg-transparent text-slate-500 border-transparent hover:bg-white'
                                            }`}
                                    >
                                        {filter.label}
                                    </button>
                                ))}
                            </div>
                        )}
                    </div>

                    {/* Request List */}
                    <div className="space-y-4">
                        {loading ? (
                            <div className="flex flex-col items-center justify-center p-12 text-slate-400">
                                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600 mb-4"></div>
                                <p>Cargando solicitudes...</p>
                            </div>
                        ) : filteredRequests.length === 0 ? (
                            <div className="text-center py-16 bg-white rounded-2xl border border-dashed border-slate-300">
                                <div className="bg-slate-50 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                                    <svg className="w-8 h-8 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                                    </svg>
                                </div>
                                <h3 className="text-slate-900 font-medium">No hay solicitudes en esta sección</h3>
                                <p className="text-slate-500 text-sm mt-1">
                                    {activeTab === 'pending' ? '¡Estás al día! No hay pendientes.' :
                                        activeTab === 'recent' ? 'No hay actividad reciente (48h).' :
                                            'No hay historial antiguo.'}
                                </p>
                            </div>
                        ) : (
                            filteredRequests.map((req) => (
                                <div key={req.id} className="bg-white rounded-xl p-5 border border-slate-200 shadow-sm hover:shadow-md transition-all duration-200">
                                    <div className="flex justify-between items-start mb-3">
                                        <div>
                                            <h3 className="text-lg font-bold text-slate-900">{req.title}</h3>
                                            <div className="text-xs text-slate-500 mt-1 flex items-center gap-2">
                                                <span>De: {req.requester_name}</span>
                                                <span className="w-1 h-1 rounded-full bg-slate-300"></span>
                                                <span>{new Date(req.created_at).toLocaleDateString()}</span>
                                            </div>
                                        </div>
                                        <span className={`px-3 py-1 rounded-full text-xs font-bold tracking-wide border ${req.status === 'approved'
                                            ? 'bg-emerald-50 text-emerald-700 border-emerald-100'
                                            : req.status === 'rejected'
                                                ? 'bg-rose-50 text-rose-700 border-rose-100'
                                                : 'bg-amber-50 text-amber-700 border-amber-100'
                                            }`}>
                                            {req.status === 'approved' ? 'APROBADO' : req.status === 'rejected' ? 'RECHAZADO' : 'PENDIENTE'}
                                        </span>
                                    </div>

                                    <div className="bg-slate-50 rounded-lg p-3 text-slate-700 text-sm leading-relaxed border border-slate-100/50">
                                        {req.description}
                                    </div>

                                    {(req.logs && req.logs.length > 0) && (
                                        <div className="mt-4 pt-4 border-t border-slate-100">
                                            <ActivityLog logs={req.logs} />
                                        </div>
                                    )}

                                    {/* Actions */}
                                    {(user?.role === 'manager' || user?.role === 'admin') && req.status === 'pending' && (
                                        <div className="mt-4 flex gap-3 justify-end pt-3 border-t border-dashed border-slate-200">
                                            <button
                                                onClick={() => handleStatusUpdate(req.id, 'rejected', 'Rechazado desde panel')}
                                                className="px-4 py-2 text-sm font-medium text-rose-600 bg-rose-50 hover:bg-rose-100 rounded-lg transition-colors focus:ring-2 focus:ring-rose-500/20"
                                            >
                                                Rechazar
                                            </button>
                                            <button
                                                onClick={() => handleStatusUpdate(req.id, 'approved', 'Aprobado desde panel')}
                                                className="px-4 py-2 text-sm font-medium text-white bg-emerald-600 hover:bg-emerald-700 rounded-lg shadow-sm shadow-emerald-200 transition-all hover:-translate-y-0.5"
                                            >
                                                Aprobar Solicitud
                                            </button>
                                        </div>
                                    )}
                                </div>
                            ))
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
