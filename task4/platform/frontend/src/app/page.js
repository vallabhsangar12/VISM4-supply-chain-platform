"use client";

import { useState, useEffect } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { Package, TrendingUp, AlertTriangle, Clock, DollarSign, Warehouse } from 'lucide-react';

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
        const trendData = await trendRes.json();
        setTrends(Array.isArray(trendData) ? trendData : []);
      } catch (err) { console.error(err); }
      finally { setLoading(false); }
    };
    fetchData();
    const intervalId = setInterval(fetchData, 10000);
    return () => clearInterval(intervalId);
  }, []);

  if (loading) return (
    <div className="flex items-center justify-center h-full">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>
  );

  if (summary?.error) return (
    <div className="flex flex-col items-center justify-center h-full space-y-4">
      <AlertTriangle size={48} className="text-amber-500" />
      <h2 className="text-2xl font-bold text-gray-900">No Data Available</h2>
      <p className="text-gray-500">Run seed_data.py to populate the database.</p>
    </div>
  );

  const kpis = summary?.kpi_cards || {};

  return (
    <div className="space-y-8 pb-10">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-gray-950 tracking-tight">Supply Chain Control Tower</h1>
          <p className="text-gray-500 mt-1 font-medium">Global Operations Monitor — Real-time Status</p>
        </div>
        <div className="text-right">
          <p className="text-xs font-bold text-gray-400 uppercase tracking-widest">Last Sync</p>
          <p className="text-sm font-bold text-gray-900">{summary?.latest_date}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <KpiCard title="Fulfillment Rate" value={`${kpis.avg_fulfillment_rate || 0}%`} icon={Package} color="blue" />
        <KpiCard title="Stockout Events (30d)" value={kpis.total_stockouts_30d || 0} icon={AlertTriangle} color="red" />
        <KpiCard title="Avg Delivery Days" value={`${kpis.avg_delivery_days || 0}d`} icon={Clock} color="emerald" />
        <KpiCard title="Order Volume (30d)" value={(kpis.total_orders_30d || 0).toLocaleString()} icon={TrendingUp} color="indigo" />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <MiniCard title="Inventory Value" value={`$${((kpis.latest_inventory_value || 0) / 1000000).toFixed(2)}M`} icon={DollarSign} />
        <MiniCard title="Warehouse Utilization" value={`${kpis.latest_warehouse_util || 0}%`} icon={Warehouse} />
        <MiniCard title="Avg Shipping Cost" value={`$${(kpis.avg_daily_shipping_cost || 0).toLocaleString()}/day`} icon={DollarSign} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-200">
          <h3 className="text-lg font-bold text-gray-900 mb-6 flex items-center">
            <TrendingUp className="mr-2 text-blue-600" size={20} /> Inventory Value Trend
          </h3>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={trends}>
                <defs>
                  <linearGradient id="colorInv" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#2563eb" stopOpacity={0.15}/>
                    <stop offset="95%" stopColor="#2563eb" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f3f4f6" />
                <XAxis dataKey="date" hide />
                <YAxis hide />
                <Tooltip
                  contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 10px 25px -5px rgb(0 0 0 / 0.1)' }}
                  formatter={(v) => [`$${v.toLocaleString()}`, 'Inventory Value']}
                />
                <Area type="monotone" dataKey="inventory_value" stroke="#2563eb" strokeWidth={2.5} fillOpacity={1} fill="url(#colorInv)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-200">
          <h3 className="text-lg font-bold text-gray-900 mb-6 flex items-center">
            <TrendingUp className="mr-2 text-emerald-600" size={20} /> Fulfillment Performance
          </h3>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={trends.slice(-14)}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f3f4f6" />
                <XAxis dataKey="date" hide />
                <YAxis hide domain={[80, 100]} />
                <Tooltip formatter={(v) => [`${v}%`, 'Fulfillment Rate']} />
                <Bar dataKey="fulfillment_rate" fill="#059669" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}

function KpiCard({ title, value, icon: Icon, color }) {
  const colorMap = {
    blue: 'bg-blue-50 text-blue-700 border-blue-100',
    red: 'bg-red-50 text-red-700 border-red-100',
    emerald: 'bg-emerald-50 text-emerald-700 border-emerald-100',
    indigo: 'bg-indigo-50 text-indigo-700 border-indigo-100'
  };
  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-200 flex flex-col justify-between hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start">
        <div className={`p-3 rounded-xl border ${colorMap[color]}`}><Icon size={22} /></div>
      </div>
      <div className="mt-5">
        <p className="text-xs font-bold text-gray-500 uppercase tracking-wider">{title}</p>
        <p className="text-3xl font-black text-gray-950 mt-1 tracking-tighter">{value}</p>
      </div>
    </div>
  );
}

function MiniCard({ title, value, icon: Icon }) {
  return (
    <div className="bg-white p-4 rounded-xl border border-gray-200 flex items-center space-x-3 shadow-sm">
      <div className="p-2 rounded-lg bg-gray-100"><Icon size={18} className="text-gray-600" /></div>
      <div>
        <p className="text-[11px] font-bold text-gray-400 uppercase tracking-wider">{title}</p>
        <p className="text-lg font-black text-gray-900">{value}</p>
      </div>
    </div>
  );
}
