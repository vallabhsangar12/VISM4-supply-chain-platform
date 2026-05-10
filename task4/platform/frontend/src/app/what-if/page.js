"use client";
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
