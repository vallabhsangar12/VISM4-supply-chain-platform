"use client";
import { useState, useEffect } from 'react';
import { AlertCircle, AlertTriangle, CheckCircle } from 'lucide-react';

const API_URL = 'http://localhost:8000/api';

export default function AlertsPage() {
  const [alerts, setAlerts] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [resolvingId, setResolvingId] = useState(null);

  const fetchData = async () => {
    try {
      const [res1, res2] = await Promise.all([fetch(`${API_URL}/alerts`), fetch(`${API_URL}/alerts/summary`)]);
      const alertsData = await res1.json();
      const summaryData = await res2.json();
      setAlerts(Array.isArray(alertsData) ? alertsData : []);
      setSummary(summaryData && !summaryData.error ? summaryData : null);
    } catch (err) { console.error(err); } finally { setLoading(false); }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  const handleResolve = async (id) => {
    setResolvingId(id);
    try {
      const res = await fetch(`${API_URL}/alerts/${id}/resolve`, { method: 'PUT' });
      if (res.ok) await fetchData();
    } catch (err) { console.error(err); } finally { setResolvingId(null); }
  };

  if (loading) return <div className="flex items-center justify-center h-full"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div></div>;

  return (
    <div className="space-y-8 pb-10">
      <div>
        <h1 className="text-3xl font-extrabold text-red-700 tracking-tight">Exception Alerts</h1>
        <p className="text-gray-600 mt-1 font-medium">Monitor and resolve supply chain anomalies</p>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 text-center"><h4 className="text-xs font-bold text-gray-500 uppercase tracking-wider">Total Alerts</h4><p className="text-4xl font-extrabold mt-3 text-gray-900">{summary?.total}</p></div>
        <div className="bg-red-50 p-6 rounded-xl shadow-sm border border-red-200 text-center text-red-900"><h4 className="text-xs font-bold text-red-600 uppercase tracking-wider">High Severity</h4><p className="text-4xl font-extrabold mt-3">{summary?.high}</p></div>
        <div className="bg-orange-50 p-6 rounded-xl shadow-sm border border-orange-200 text-center text-orange-900"><h4 className="text-xs font-bold text-orange-600 uppercase tracking-wider">Medium Severity</h4><p className="text-4xl font-extrabold mt-3">{summary?.medium}</p></div>
        <div className="bg-blue-50 p-6 rounded-xl shadow-sm border border-blue-200 text-center text-blue-900"><h4 className="text-xs font-bold text-blue-600 uppercase tracking-wider">Unresolved</h4><p className="text-4xl font-extrabold mt-3">{summary?.unresolved}</p></div>
      </div>
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <div className="p-5 border-b border-gray-200 bg-gray-50"><h3 className="text-lg font-bold text-gray-900">Recent Incidents</h3></div>
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-100"><tr><th className="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase">Date</th><th className="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase">Severity</th><th className="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase">Issue</th><th className="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase">Status</th></tr></thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {alerts.map((a) => (
              <tr key={a.id} className="hover:bg-gray-50 transition-colors">
                <td className="px-6 py-4 text-sm text-gray-600 font-medium">{a.date}</td>
                <td className="px-6 py-4"><span className={`px-2.5 py-1 text-xs font-bold rounded-full border ${a.severity === 'HIGH' ? 'bg-red-100 text-red-800 border-red-300' : 'bg-orange-100 text-orange-800 border-orange-300'}`}>{a.severity}</span></td>
                <td className="px-6 py-4 text-sm font-bold text-gray-900">{a.message}</td>
                <td className="px-6 py-4">{a.resolved ? <span className="flex items-center text-sm font-bold text-green-700"><CheckCircle size={16} className="mr-1.5" /> Resolved</span> : <button onClick={() => handleResolve(a.id)} disabled={resolvingId === a.id} className="text-blue-700 border border-blue-600 px-3 py-1 rounded-md text-sm font-bold hover:bg-blue-600 hover:text-white transition-colors">{resolvingId === a.id ? '...' : 'Resolve Issue'}</button>}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
