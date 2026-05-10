"use client";
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
