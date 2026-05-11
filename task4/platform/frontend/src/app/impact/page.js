"use client";

import { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { DollarSign, TrendingUp, Package, Truck, Target, Clock, ArrowUpRight, ArrowDownRight } from 'lucide-react';

const API_URL = 'http://localhost:8000/api';

export default function ImpactPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchData = () => {
    fetch(`${API_URL}/impact`)
      .then(res => res.json())
      .then(d => { setData(d); setLoading(false); })
      .catch(err => { console.error(err); setLoading(false); });
  };
  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 10000);
    return () => clearInterval(interval);
  }, []);

  if (loading) return (
    <div className="flex items-center justify-center h-full">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>
  );

  if (!data) return (
    <div className="flex flex-col items-center justify-center h-full space-y-4">
      <DollarSign size={48} className="text-gray-400" />
      <h2 className="text-2xl font-bold text-gray-900">Impact Data Unavailable</h2>
    </div>
  );

  const savingsChart = [
    { name: 'Inventory', value: data.inventory_savings_annual, fill: '#2563eb' },
    { name: 'Transport', value: data.transport_savings_annual, fill: '#059669' },
  ];

  const roiData = [
    { name: 'Investment', value: data.implementation_cost, fill: '#ef4444' },
    { name: 'Annual Savings', value: data.annual_total_savings, fill: '#22c55e' },
  ];

  const COLORS = ['#2563eb', '#059669', '#f59e0b', '#8b5cf6'];

  return (
    <div className="space-y-8 pb-10">
      <div>
        <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight">Business Impact Analysis</h1>
        <p className="text-gray-500 mt-1 font-medium">Quantified savings, ROI projection, and service level improvements</p>
      </div>

      {/* ROI Hero Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-gradient-to-br from-blue-600 to-blue-700 p-6 rounded-2xl text-white shadow-lg shadow-blue-200">
          <div className="flex items-center space-x-2 mb-4">
            <DollarSign size={20} />
            <span className="text-xs font-bold uppercase tracking-widest opacity-80">Annual Total Savings</span>
          </div>
          <p className="text-4xl font-black">${(data.annual_total_savings / 1000).toFixed(0)}K</p>
          <p className="text-sm mt-2 opacity-80">Combined inventory + transport optimization</p>
        </div>
        <div className="bg-gradient-to-br from-emerald-600 to-emerald-700 p-6 rounded-2xl text-white shadow-lg shadow-emerald-200">
          <div className="flex items-center space-x-2 mb-4">
            <TrendingUp size={20} />
            <span className="text-xs font-bold uppercase tracking-widest opacity-80">Return on Investment</span>
          </div>
          <p className="text-4xl font-black">{data.roi_pct}%</p>
          <p className="text-sm mt-2 opacity-80">Payback period: {data.payback_months} months</p>
        </div>
        <div className="bg-gradient-to-br from-purple-600 to-purple-700 p-6 rounded-2xl text-white shadow-lg shadow-purple-200">
          <div className="flex items-center space-x-2 mb-4">
            <Target size={20} />
            <span className="text-xs font-bold uppercase tracking-widest opacity-80">Service Level Target</span>
          </div>
          <p className="text-4xl font-black">{data.service_level_target}%</p>
          <p className="text-sm mt-2 opacity-80">Current: {data.service_level_current}% (+{data.service_improvement_pct}% improvement)</p>
        </div>
      </div>

      {/* Detailed Metrics */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Inventory Optimization */}
        <div className="bg-white p-8 rounded-2xl border border-gray-200 shadow-sm">
          <h3 className="text-lg font-bold text-gray-900 mb-6 flex items-center">
            <Package className="mr-2 text-blue-600" size={20} /> Inventory Cost Optimization
          </h3>
          <div className="space-y-4">
            <MetricRow label="Monthly Holding Cost Savings" value={`$${data.inventory_savings_monthly.toLocaleString()}`} positive={true} />
            <MetricRow label="Annual Projected Savings" value={`$${data.inventory_savings_annual.toLocaleString()}`} positive={true} />
            <MetricRow label="Working Capital Reduction" value={`$${data.working_capital_reduction.toLocaleString()}`} positive={true} />
            <MetricRow label="Products Below Reorder Point" value={`${data.products_below_rop} / ${data.total_products}`} positive={false} />
          </div>
        </div>

        {/* Transportation Optimization */}
        <div className="bg-white p-8 rounded-2xl border border-gray-200 shadow-sm">
          <h3 className="text-lg font-bold text-gray-900 mb-6 flex items-center">
            <Truck className="mr-2 text-emerald-600" size={20} /> Transportation Optimization
          </h3>
          <div className="space-y-4">
            <MetricRow label="Monthly Route Savings" value={`$${data.transport_savings_monthly.toLocaleString()}`} positive={true} />
            <MetricRow label="Annual Route Savings" value={`$${data.transport_savings_annual.toLocaleString()}`} positive={true} />
            <MetricRow label="Routes Flagged for Optimization" value={`${data.optimizable_routes} / ${data.total_routes}`} positive={false} />
            <MetricRow label="Total Transport Cost (monthly)" value={`$${data.total_transport_cost.toLocaleString()}`} positive={null} />
          </div>
        </div>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white p-8 rounded-2xl border border-gray-200 shadow-sm">
          <h3 className="text-lg font-bold text-gray-900 mb-6">Annual Savings Breakdown</h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={savingsChart} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#f3f4f6" />
                <XAxis type="number" tickFormatter={(v) => `$${(v/1000).toFixed(0)}K`} />
                <YAxis type="category" dataKey="name" width={80} />
                <Tooltip formatter={(v) => `$${v.toLocaleString()}`} />
                <Bar dataKey="value" radius={[0, 8, 8, 0]}>
                  {savingsChart.map((entry, i) => <Cell key={i} fill={entry.fill} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white p-8 rounded-2xl border border-gray-200 shadow-sm">
          <h3 className="text-lg font-bold text-gray-900 mb-6">ROI Overview</h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={roiData} cx="50%" cy="50%" outerRadius={100} innerRadius={60} dataKey="value" label={({ name, value }) => `${name}: $${(value/1000).toFixed(0)}K`}>
                  {roiData.map((entry, i) => <Cell key={i} fill={entry.fill} />)}
                </Pie>
                <Tooltip formatter={(v) => `$${v.toLocaleString()}`} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Service Level & Stockout */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm">
          <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center">
            <Target className="mr-2 text-purple-600" size={20} /> Service Level Improvement
          </h3>
          <div className="flex items-end space-x-4">
            <div>
              <p className="text-xs font-bold text-gray-500 uppercase">Current</p>
              <p className="text-3xl font-black text-gray-900">{data.service_level_current}%</p>
            </div>
            <ArrowUpRight size={32} className="text-emerald-500 mb-1" />
            <div>
              <p className="text-xs font-bold text-gray-500 uppercase">Target</p>
              <p className="text-3xl font-black text-emerald-600">{data.service_level_target}%</p>
            </div>
          </div>
          <div className="mt-4 w-full bg-gray-200 h-3 rounded-full overflow-hidden">
            <div className="bg-gradient-to-r from-blue-500 to-emerald-500 h-full rounded-full" style={{ width: `${data.service_level_current}%` }} />
          </div>
        </div>
        <div className="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm">
          <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center">
            <Clock className="mr-2 text-amber-600" size={20} /> Stockout Reduction
          </h3>
          <div className="flex items-end space-x-4">
            <div>
              <p className="text-xs font-bold text-gray-500 uppercase">Current Avg/Day</p>
              <p className="text-3xl font-black text-red-600">{data.current_avg_stockouts}</p>
            </div>
            <ArrowDownRight size={32} className="text-emerald-500 mb-1" />
            <div>
              <p className="text-xs font-bold text-gray-500 uppercase">Projected Reduction</p>
              <p className="text-3xl font-black text-emerald-600">-{data.projected_stockout_reduction}</p>
            </div>
          </div>
          <p className="text-sm text-gray-500 mt-4">65% stockout reduction through proactive EOQ-based reordering and safety stock optimization</p>
        </div>
      </div>
    </div>
  );
}

function MetricRow({ label, value, positive }) {
  return (
    <div className="flex justify-between items-center py-2 border-b border-gray-100">
      <span className="text-sm text-gray-600 font-medium">{label}</span>
      <span className={`text-sm font-bold ${positive === true ? 'text-emerald-600' : positive === false ? 'text-amber-600' : 'text-gray-900'}`}>
        {value}
      </span>
    </div>
  );
}
