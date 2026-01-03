import React from 'react';

const ActivityLog = ({ logs }) => {
    if (!logs || logs.length === 0) {
        return <div className="text-xs text-gray-400 mt-2 italic">Sin actividad aún.</div>;
    }

    return (
        <div className="mt-3 border-t pt-2">
            <h5 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Registro de Actividad</h5>
            <div className="space-y-2">
                {logs.map((log, index) => (
                    <div key={index} className="flex items-start space-x-2 text-sm">
                        <div className={`mt-0.5 w-2 h-2 rounded-full ${log.action === 'approved' ? 'bg-green-500' :
                            log.action === 'rejected' ? 'bg-red-500' : 'bg-gray-400'
                            }`}></div>
                        <div className="flex-1">
                            <div className="flex justify-between">
                                <span className="font-medium text-gray-700">{log.approver_name}</span>
                                <span className="text-xs text-gray-400">{new Date(log.timestamp).toLocaleString()}</span>
                            </div>
                            <div className="text-gray-600">
                                <span className={
                                    log.action === 'approved' ? 'text-green-600 font-medium' :
                                        log.action === 'rejected' ? 'text-red-600 font-medium' : 'text-gray-500'
                                }>
                                    {log.action.toUpperCase()}
                                </span>
                                {log.comment && <span className="text-gray-500"> - "{log.comment}"</span>}
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ActivityLog;
