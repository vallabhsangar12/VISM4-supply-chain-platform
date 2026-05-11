"use client";
import { useState, useEffect } from 'react';
import { Package, Map, Zap } from 'lucide-react';

const API_URL = 'http://localhost:8000/api';

export default function OptimizationPage() {
  const [recs, setRecs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [actionId, setActionId] = useState(null);

  const fetchData = () => fetch(`${API_URL}/recommendations`).then(res => res.json()).then(d => { setRecs(Array.isArray(d) ? d : []); setLoading(false); }).catch(e => { console.error(e); setLoading(false); });
  useEffect(() => { 
    fetchData(); 
    const interval = setInterval(fetchData, 10000);
    return () => clearInterval(interval);
  }, []);

  const handleAction = async (type, id, qty) => {
    setActionId(id || 'route');
    const url = type === 'ORDER' ? `${API_URL}/recommendations/order` : `${API_URL}/recommendations/optimize-route`;
    const body = type === 'ORDER' ? JSON.stringify({ product_id: id, order_qty: qty }) : null;
    await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body });
    await fetchData();
    setActionId(null);
  };

  if (loading) return <div className="flex justify-center h-full"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div></div>;

  return (
    <div className="space-y-8 pb-10">
      <h1 className="text-3xl font-extrabold text-emerald-700">Optimization Engine</h1>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="bg-white p-6 rounded-2xl border border-gray-200">
          <h3 className="text-lg font-bold mb-4 flex items-center text-blue-700"><Package className="mr-2" /> Pending Reorders</h3>
          {recs.filter(r => r.type === 'REORDER').map((r, i) => (
            <div key={i} className="p-4 mb-4 bg-gray-50 rounded-xl border flex justify-between items-center">
              <div><p className="font-bold">{r.name}</p><p className="text-sm text-gray-500">{r.message}</p></div>
              <button onClick={() => handleAction('ORDER', r.product_id, r.order_qty)} disabled={actionId === r.product_id} className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-bold">{actionId === r.product_id ? '...' : 'Approve'}</button>
            </div>
          ))}
        </div>
        <div className="bg-white p-6 rounded-2xl border border-gray-200">
          <h3 className="text-lg font-bold mb-4 flex items-center text-emerald-700"><Map className="mr-2" /> Logistics Optimization</h3>
          {recs.filter(r => r.type === 'ROUTE').map((r, i) => (
            <div key={i} className="p-4 bg-emerald-50 rounded-xl border border-emerald-200">
              <p className="font-bold text-emerald-900 mb-2">{r.message}</p>
              <button onClick={() => handleAction('ROUTE')} disabled={actionId === 'route'} className="w-full bg-emerald-600 text-white py-2 rounded-lg font-bold">{actionId === 'route' ? '...' : 'Consolidate Routes'}</button>
            </div>
          ))}
        </div>
        <div className="bg-white p-6 rounded-2xl border border-gray-200">
          <h3 className="text-lg font-bold mb-4 flex items-center text-purple-700"><Zap className="mr-2" /> Supplier Optimization</h3>
          {recs.filter(r => r.type === 'SUPPLIER').map((r, i) => (
            <div key={i} className="p-4 bg-purple-50 rounded-xl border border-purple-200">
              <p className="font-bold text-purple-900 mb-2">{r.message}</p>
              <div className="w-full bg-purple-600 text-white py-2 rounded-lg font-bold text-center opacity-80 cursor-not-allowed">Auto-Selected</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
