import { useEffect, useState } from 'react';
import api from '../api';

const RequestList = ({ refreshTrigger }) => {
    const [requests, setRequests] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchRequests = async () => {
            try {
                const response = await api.get('/requests/');
                setRequests(response.data);
            } catch (error) {
                console.error("Failed to fetch requests", error);
            } finally {
                setLoading(false);
            }
        };

        fetchRequests();
    }, [refreshTrigger]);

    if (loading) return <div className="text-gray-500">Cargando solicitudes...</div>;

    if (requests.length === 0) {
        return <div className="text-gray-500">No hay solicitudes. ¡Crea una arriba!</div>;
    }

    return (
        <div className="space-y-4">
            {requests.map((req) => (
                <div key={req.id} className="p-4 bg-white border border-gray-200 rounded shadow-sm">
                    <div className="flex items-center justify-between">
                        <h4 className="text-lg font-bold text-gray-800">{req.title}</h4>
                        <span className={`px-2 py-1 text-xs font-semibold rounded ${req.status === 'approved' ? 'bg-green-100 text-green-800' :
                            req.status === 'rejected' ? 'bg-red-100 text-red-800' :
                                'bg-yellow-100 text-yellow-800'
                            }`}>
                            {req.status.toUpperCase()}
                        </span>
                    </div>
                    <p className="mt-1 text-gray-600">{req.description}</p>
                    <div className="mt-2 text-xs text-gray-500">
                        Solicitado por: {req.requester_name} el {new Date(req.created_at).toLocaleDateString()}
                    </div>
                </div>
            ))}
        </div>
    );
};

export default RequestList;
