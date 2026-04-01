import React, { useState, useEffect } from 'react';
import { 
  FileText, 
  Upload, 
  Settings, 
  BarChart3, 
  CheckCircle2, 
  Clock, 
  AlertCircle,
  Plus,
  RefreshCcw,
  ExternalLink,
  ChevronRight
} from 'lucide-react';

import { fetchDocuments } from '../services/api';
import type { UnifiedDocument } from '../types';

const DASHBOARD_GRADIENT = "bg-gradient-to-br from-slate-900 via-slate-950 to-black";

const Button = ({ children, className = "", variant = "primary" }: any) => {
  const base = "px-4 py-2 rounded-lg font-medium transition-all duration-200 flex items-center gap-2 text-sm";
  const variants: any = {
    primary: "bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-500/20",
    secondary: "bg-slate-800 hover:bg-slate-700 text-slate-100",
    outline: "border border-slate-700 hover:border-slate-600 text-slate-300"
  };
  return <button className={`${base} ${variants[variant]} ${className}`}>{children}</button>;
};

const Dashboard: React.FC = () => {
  const [docs, setDocs] = useState<UnifiedDocument[]>([]);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    setLoading(true);
    try {
      const data = await fetchDocuments();
      setDocs(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  if (loading) {
      return (
          <div className={`min-h-screen ${DASHBOARD_GRADIENT} flex items-center justify-center text-white`}>
              <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
          </div>
      );
  }

  const stats = {
    total: docs.length,
    pending: docs.filter(d => d.status === 'UPLOADED' || d.status === 'PARSED').length,
    ready: docs.filter(d => d.status === 'PRINT_READY').length
  };

  const getStatusBadge = (status: string) => {
    const colors: any = {
      UPLOADED: "bg-slate-500/10 text-slate-400 border-slate-500/20",
      PARSED: "bg-blue-500/10 text-blue-400 border-blue-500/20",
      CALCULATED: "bg-indigo-500/10 text-indigo-400 border-indigo-500/20",
      PRINT_READY: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
      EXPORTED: "bg-purple-500/10 text-purple-400 border-purple-500/20"
    };
    return (
      <span className={`px-2 py-0.5 rounded text-[10px] font-bold border uppercase tracking-wider ${colors[status]}`}>
        {status}
      </span>
    );
  };

  return (
    <div className={`min-h-screen ${DASHBOARD_GRADIENT} text-slate-200 font-sans selection:bg-blue-500/30`}>
      {/* Sidebar / Nav */}
      <nav className="fixed left-0 top-0 h-full w-20 border-r border-slate-800 flex flex-col items-center py-8 gap-8 bg-slate-950/50 backdrop-blur-xl">
        <div className="w-12 h-12 bg-blue-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-600/20">
          <FileText className="text-white" size={24} />
        </div>
        <div className="flex flex-col gap-6 mt-4">
          <div className="p-3 text-blue-400 bg-blue-400/10 rounded-lg cursor-pointer"><BarChart3 size={20} /></div>
          <div className="p-3 text-slate-500 hover:text-slate-300 rounded-lg cursor-pointer transition-colors"><Upload size={20} /></div>
          <div className="p-3 text-slate-500 hover:text-slate-300 rounded-lg cursor-pointer transition-colors"><Clock size={20} /></div>
          <div className="p-3 text-slate-500 hover:text-slate-300 rounded-lg cursor-pointer transition-colors"><Settings size={20} /></div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="pl-28 pr-12 py-10">
        {/* Header */}
        <div className="flex justify-between items-end mb-12">
          <div>
            <h1 className="text-5xl font-extrabold tracking-tighter text-white">
              Nexus <span className="text-blue-600">Bill</span>
            </h1>
            <p className="text-slate-500 mt-2 text-lg">Consolidated Billing & Project Workflow Management</p>
          </div>
          <div className="flex gap-4">
            <Button variant="outline"><RefreshCcw size={16} /> Sync</Button>
            <Button><Plus size={18} /> New Document</Button>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          {[
            { label: 'Total Projects', value: stats.total, icon: BarChart3, color: 'text-blue-400' },
            { label: 'Pending Processing', value: stats.pending, icon: Clock, color: 'text-amber-400' },
            { label: 'Print Ready', value: stats.ready, icon: CheckCircle2, color: 'text-emerald-400' }
          ].map((stat, i) => (
            <div key={i} className="bg-slate-900/50 border border-slate-800 p-6 rounded-2xl backdrop-blur-sm shadow-xl hover:border-slate-700 transition-all">
              <div className="flex justify-between items-start">
                <div>
                  <p className="text-slate-500 text-sm font-medium mb-1">{stat.label}</p>
                  <h3 className="text-3xl font-bold text-white">{stat.value}</h3>
                </div>
                <div className={`p-3 bg-slate-800 rounded-xl ${stat.color} shadow-inner`}>
                  <stat.icon size={20} />
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Document List */}
        <div className="bg-slate-900/40 border border-slate-800 rounded-2xl backdrop-blur-md overflow-hidden shadow-2xl">
          <div className="p-6 border-b border-slate-800 flex justify-between items-center bg-slate-900/50">
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              Recent Documents <span className="text-slate-600 text-sm font-normal">({docs.length})</span>
            </h2>
            <div className="text-blue-500 text-sm font-semibold flex items-center gap-1 cursor-pointer hover:underline">
              View All <ChevronRight size={14} />
            </div>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="bg-slate-950/30 text-slate-500 text-xs uppercase tracking-widest border-b border-slate-800">
                  <th className="px-6 py-4 font-semibold">Document Info</th>
                  <th className="px-6 py-4 font-semibold">Status</th>
                  <th className="px-6 py-4 font-semibold">Contractor</th>
                  <th className="px-6 py-4 font-semibold text-right">Total Amount</th>
                  <th className="px-6 py-4 font-semibold"></th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/50">
                {docs.map((doc) => (
                  <tr key={doc.id} className="hover:bg-white/5 transition-colors group">
                    <td className="px-6 py-5">
                      <div className="flex flex-col">
                        <span className="text-slate-100 font-bold group-hover:text-blue-400 transition-colors uppercase text-sm tracking-tight">
                          {doc.metadata.bill_no}
                        </span>
                        <span className="text-slate-500 text-xs mt-0.5 line-clamp-1">{doc.metadata.work_name}</span>
                      </div>
                    </td>
                    <td className="px-6 py-5">
                      {getStatusBadge(doc.status)}
                    </td>
                    <td className="px-6 py-5">
                      <span className="text-slate-300 text-sm">{doc.metadata.contractor_name}</span>
                    </td>
                    <td className="px-6 py-5 text-right text-xs text-slate-500">
                      {new Date(doc.metadata.last_modified).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-5 text-right">
                      <span className="text-white font-mono font-bold">
                        {doc.summary.total_amount > 0 ? `₹${doc.summary.total_amount.toLocaleString()}` : "—"}
                      </span>
                    </td>
                    <td className="px-6 py-5 text-right w-10">
                      <div className="p-2 text-slate-500 hover:text-white rounded-lg hover:bg-slate-800 cursor-pointer transition-all">
                        <ExternalLink size={16} />
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          
          {docs.length === 0 && (
            <div className="p-20 flex flex-col items-center justify-center text-slate-600 gap-4">
              <AlertCircle size={48} className="opacity-20" />
              <p className="text-lg">No documents found</p>
              <Button variant="outline" className="mt-2">Upload First Bill</Button>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
