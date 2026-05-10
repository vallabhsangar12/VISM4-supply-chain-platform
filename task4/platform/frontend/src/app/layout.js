import './globals.css';
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
