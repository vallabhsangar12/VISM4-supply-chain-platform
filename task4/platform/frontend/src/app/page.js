"use client";
import { useState, useEffect } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { Package, TrendingUp, AlertTriangle, Clock } from 'lucide-react';

const API_URL = 'http://localhost:8000/api';

export default function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [trends, setTrends] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [sumRes, trendRes] = await Promise.all([
          fetch(`${API_URL}/dashboard/summary`),
          fetch(`${API_URL}/dashboard/trends`)
        ]);
        setSummary(await sumRes.json());
        setTrends(await trendRes.json());
      } catch (err) { console.error(err); } finally { setLoading(false); }
    };
    fetchData();
  }, []);

  if (loading) return <div className="flex items-center justify-center h-full"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div></div>;

  const kpis = summary?.kpi_cards;

  return (
    <div className="space-y-8 pb-10">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-gray-950 tracking-tight">Supply Chain Control Tower</h1>
          <p className="text-gray-600 mt-1 font-medium italic">Global Operations Monitor — Real-time Status</p>
        </div>
        <div className="text-right"><p className="text-xs font-bold text-gray-400 uppercase tracking-widest">Last Sync</p><p className="text-sm font-bold text-gray-900">{summary?.latest_date}</p></div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <KpiCard title="Fulfillment Rate" value={`${kpis?.avg_fulfillment_rate}%`} icon={Package} color="blue" trend="+2.4% vs LY" />
        <KpiCard title="Stockout Events" value={kpis?.total_stockouts_30d} icon={AlertTriangle} color="red" trend="-12% vs LY" />
        <KpiCard title="Avg Delivery" value={`${kpis?.avg_delivery_days}d`} icon={Clock} color="emerald" trend="-0.5d vs LY" />
        <KpiCard title="30D Order Vol" value={kpis?.total_orders_30d?.toLocaleString()} icon={TrendingUp} color="indigo" trend="+8% vs LY" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-200">
          <h3 className="text-lg font-bold text-gray-900 mb-6 flex items-center"><TrendingUp className="mr-2 text-blue-600" size={20} /> Inventory Value Trend</h3>
          <div className="h-80"><ResponsiveContainer width="100%" height="100%"><AreaChart data={trends}><defs><linearGradient id="colorInv" x1="0" y1="0" x2="0" y2="1"><stop offset="5%" stopColor="#2563eb" stopOpacity={0.1}/><stop offset="95%" stopColor="#2563eb" stopOpacity={0}/></linearGradient></defs><CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f3f4f6" /><XAxis dataKey="date" hide /><YAxis hide /><Tooltip contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)' }} /><Area type="monotone" dataKey="inventory_value" stroke="#2563eb" strokeWidth={3} fillOpacity={1} fill="url(#colorInv)" /></AreaChart></ResponsiveContainer></div>
        </div>
        <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-200">
          <h3 className="text-lg font-bold text-gray-900 mb-6 flex items-center"><TrendingUp className="mr-2 text-emerald-600" size={20} /> Fulfillment Performance</h3>
          <div className="h-80"><ResponsiveContainer width="100%" height="100%"><BarChart data={trends.slice(-14)}><CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f3f4f6" /><XAxis dataKey="date" hide /><YAxis hide /><Tooltip /><Bar dataKey="fulfillment_rate" fill="#059669" radius={[4, 4, 0, 0]} /></BarChart></ResponsiveContainer></div>
        </div>
      </div>
    </div>
  );
}

function KpiCard({ title, value, icon: Icon, color, trend }) {
  const colorMap = { blue: 'bg-blue-50 text-blue-700 border-blue-100', red: 'bg-red-50 text-red-700 border-red-100', emerald: 'bg-emerald-50 text-emerald-700 border-emerald-100', indigo: 'bg-indigo-50 text-indigo-700 border-indigo-100' };
  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-200 flex flex-col justify-between group hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start">
        <div className={`p-3 rounded-xl border ${colorMap[color]}`}><Icon size={22} /></div>
        <span className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">{trend}</span>
      </div>
      <div className="mt-6">
        <p className="text-xs font-bold text-gray-500 uppercase tracking-wider">{title}</p>
        <p className="text-3xl font-black text-gray-950 mt-1 tracking-tighter">{value}</p>
      </div>
    </div>
  );
}
