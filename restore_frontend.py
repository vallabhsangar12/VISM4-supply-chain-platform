import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# Frontend Files
layout_js = """import './globals.css';
import Sidebar from '@/components/Sidebar';

export const metadata = {
  title: 'Supply Chain Intelligence Platform',
  description: 'Enterprise-grade supply chain monitoring and optimization',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-gray-100 text-gray-900 flex h-screen overflow-hidden">
        <Sidebar />
        <main className="flex-1 overflow-y-auto p-8 relative">
          {children}
        </main>
      </body>
    </html>
  );
}
"""

sidebar_js = """"use client";
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  LayoutDashboard, 
  AlertOctagon, 
  TrendingUp, 
  Zap, 
  BarChart3,
  Box,
  Truck
} from 'lucide-react';

const menuItems = [
  { name: 'Control Tower', icon: LayoutDashboard, path: '/' },
  { name: 'Exceptions', icon: AlertOctagon, path: '/alerts' },
  { name: 'Demand Forecast', icon: TrendingUp, path: '/forecast' },
  { name: 'Optimization', icon: Zap, path: '/optimization' },
  { name: 'What-If Analysis', icon: BarChart3, path: '/what-if' },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-72 bg-gray-950 text-white flex flex-col h-full shadow-2xl border-r border-gray-800 z-50">
      <div className="p-8 border-b border-gray-800 flex items-center space-x-3">
        <div className="p-2 bg-blue-600 rounded-lg"><Box size={24} className="text-white" /></div>
        <div>
          <h2 className="text-xl font-black tracking-tighter text-white">SC INTELLIGENCE</h2>
          <p className="text-[10px] font-bold text-blue-500 uppercase tracking-widest">Enterprise v1.0</p>
        </div>
      </div>
      
      <nav className="flex-1 p-6 space-y-2 mt-4">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.path;
          return (
            <Link 
              key={item.path} 
              href={item.path}
              className={`flex items-center space-x-4 px-4 py-3.5 rounded-xl transition-all duration-300 group ${
                isActive 
                  ? 'bg-blue-600 text-white shadow-lg shadow-blue-900/50 scale-105' 
                  : 'text-gray-400 hover:bg-gray-900 hover:text-white'
              }`}
            >
              <Icon size={20} className={`${isActive ? 'text-white' : 'text-gray-500 group-hover:text-blue-400'} transition-colors`} />
              <span className="font-bold text-sm tracking-wide">{item.name}</span>
            </Link>
          );
        })}
      </nav>

      <div className="p-8 bg-gray-900/50 m-4 rounded-2xl border border-gray-800">
        <div className="flex items-center space-x-2 mb-3">
          <Truck size={16} className="text-blue-400" />
          <h4 className="text-xs font-black text-gray-300 uppercase">System Health</h4>
        </div>
        <div className="w-full bg-gray-800 h-1.5 rounded-full overflow-hidden">
          <div className="bg-blue-500 h-full w-[94%]" />
        </div>
        <p className="text-[10px] mt-2 font-bold text-gray-500 tracking-wider">94% Operational Efficiency</p>
      </div>
    </aside>
  );
}
"""

# Write Frontend
write_file('frontend/src/app/layout.js', layout_js)
write_file('frontend/src/components/Sidebar.js', sidebar_js)
write_file('frontend/package.json', '{"name":"supply-chain-frontend","version":"1.0.0","scripts":{"dev":"next dev","build":"next build","start":"next start"},"dependencies":{"next":"14.0.0","react":"18.2.0","react-dom":"18.2.0","lucide-react":"0.284.0","recharts":"2.9.0","clsx":"2.0.0","tailwind-merge":"1.14.0"}}')
