import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# Forecast Page
forecast_js = """"use client";
import { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { TrendingUp, Calendar } from 'lucide-react';

const API_URL = 'http://localhost:8000/api';

export default function ForecastPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_URL}/forecast`).then(res => res.json()).then(d => { setData(d); setLoading(false); });
  }, []);

  if (loading) return <div className="flex items-center justify-center h-full"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div></div>;

  const chartData = [...data.historical, ...data.forecast.map(f => ({ ...f, orders: f.predicted_orders }))];

  return (
    <div className="space-y-8 pb-10">
      <div>
        <h1 className="text-3xl font-extrabold text-blue-700 tracking-tight">Demand Forecast</h1>
        <p className="text-gray-600 mt-1 font-medium">30-day predictive analytics with statistical confidence intervals</p>
      </div>
      <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-200">
        <div className="h-[500px]">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f3f4f6" />
              <XAxis dataKey="date" hide />
              <YAxis stroke="#94a3b8" fontSize={12} />
              <Tooltip />
              <Line type="monotone" dataKey="orders" stroke="#2563eb" strokeWidth={3} dot={false} />
              <Line type="monotone" dataKey="upper_bound" stroke="#93c5fd" strokeDasharray="5 5" dot={false} />
              <Line type="monotone" dataKey="lower_bound" stroke="#93c5fd" strokeDasharray="5 5" dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
"""

# Optimization Page
opt_js = """"use client";
import { useState, useEffect } from 'react';
import { Package, Map, Zap } from 'lucide-react';

const API_URL = 'http://localhost:8000/api';

export default function OptimizationPage() {
  const [recs, setRecs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [actionId, setActionId] = useState(null);

  const fetchData = () => fetch(`${API_URL}/recommendations`).then(res => res.json()).then(d => { setRecs(d); setLoading(false); });
  useEffect(() => { fetchData(); }, []);

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
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
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
      </div>
    </div>
  );
}
"""

# What-If Page
whatif_js = """"use client";
import { useState } from 'react';
import { BarChart3, ShieldCheck, ShieldAlert } from 'lucide-react';

const API_URL = 'http://localhost:8000/api';

export default function WhatIfPage() {
  const [demand, setDemand] = useState(0);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const simulate = async () => {
    setLoading(true);
    const res = await fetch(`${API_URL}/whatif`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ demand_change_pct: demand }) });
    setResults(await res.json());
    setLoading(false);
  };

  return (
    <div className="space-y-8 pb-10">
      <h1 className="text-3xl font-extrabold text-purple-700 tracking-tight">What-If Simulation</h1>
      <div className="bg-white p-8 rounded-2xl border border-gray-200">
        <label className="block text-sm font-bold text-gray-700 mb-4">Simulate Demand Change: {demand}%</label>
        <input type="range" min="-50" max="100" value={demand} onChange={(e) => setDemand(parseInt(e.target.value))} className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-purple-600" />
        <button onClick={simulate} disabled={loading} className="mt-6 w-full bg-purple-600 text-white py-3 rounded-xl font-bold shadow-lg shadow-purple-200">{loading ? 'Simulating...' : 'Run Simulation'}</button>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {results.map((r, i) => (
          <div key={i} className={`p-6 rounded-2xl border ${r.stock_adequate ? 'bg-white border-gray-200' : 'bg-red-50 border-red-200'}`}>
            <div className="flex justify-between items-center mb-4">
              <h4 className="font-bold">{r.product_id}</h4>
              {r.stock_adequate ? <ShieldCheck className="text-emerald-500" /> : <ShieldAlert className="text-red-500" />}
            </div>
            <p className="text-sm font-medium text-gray-600">Cost Impact: <span className={r.cost_change_pct > 0 ? 'text-red-600' : 'text-emerald-600'}>{r.cost_change_pct}%</span></p>
            <p className="text-xs mt-2 text-gray-400">Resilient: {r.stock_adequate ? 'YES' : 'NO'}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
"""

write_file('frontend/src/app/forecast/page.js', forecast_js)
write_file('frontend/src/app/optimization/page.js', opt_js)
write_file('frontend/src/app/what-if/page.js', whatif_js)
