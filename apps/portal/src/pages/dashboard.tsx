import React from 'react';

// Devopstrio AIOps Incident Predictor - SRE Command Center
// Stack: Next.js 14 + Tailwind CSS

const Dashboard = () => {
    return (
        <div className="min-h-screen bg-[#020617] text-white">
            {/* Command Header */}
            <header className="border-b border-indigo-500/20 bg-slate-900/50 backdrop-blur-xl sticky top-0 z-50">
                <div className="max-w-7xl mx-auto px-8 h-20 flex items-center justify-between">
                    <div className="flex items-center gap-4">
                        <div className="w-12 h-12 bg-indigo-600 rounded-xl flex items-center justify-center font-black shadow-lg shadow-indigo-600/20">AI</div>
                        <h1 className="text-xl font-bold tracking-tight">SRE Command Center <span className="text-slate-500 font-normal ml-2">Prophet-v2 Engine</span></h1>
                    </div>
                    <div className="flex gap-4 items-center">
                        <span className="text-xs font-bold text-emerald-400 bg-emerald-400/10 px-3 py-1.5 rounded-full flex items-center gap-2">
                            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                            PREDICTION MATRIX ONLINE
                        </span>
                    </div>
                </div>
            </header>

            <main className="max-w-7xl mx-auto px-8 py-10">
                {/* Top Metrics Row */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-10">
                    {[
                        { label: 'Predicted Failures (<2h)', value: '3', trend: '+1', color: 'rose' },
                        { label: 'Active Incidents', value: '1', trend: '-4', color: 'amber' },
                        { label: 'Alert Noise Reduction', value: '94.2%', trend: '+2.1%', color: 'emerald' },
                        { label: 'Global MTTR', value: '18m', trend: '-4m', color: 'blue' }
                    ].map((kpi, idx) => (
                        <div key={idx} className="bg-slate-900/60 p-6 rounded-[2rem] border border-white/5 hover:border-indigo-500/30 transition-all cursor-crosshair relative overflow-hidden">
                            <div className={`absolute top-0 right-0 w-32 h-32 bg-${kpi.color}-500/10 rounded-full blur-3xl -mr-16 -mt-16`}></div>
                            <span className="text-[10px] font-black uppercase tracking-widest text-slate-400 relative z-10">{kpi.label}</span>
                            <div className="flex items-end justify-between mt-3 relative z-10">
                                <span className="text-4xl font-black">{kpi.value}</span>
                                <span className={`text-xs font-bold px-2 py-1 rounded-lg bg-${kpi.color}-500/10 text-${kpi.color}-400`}>
                                    {kpi.trend}
                                </span>
                            </div>
                        </div>
                    ))}
                </div>

                {/* Main Prediction & Correlation Hub */}
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                    {/* Predictive Horizon Timeline */}
                    <div className="lg:col-span-8 bg-slate-900/60 p-8 rounded-[3rem] border border-white/5">
                        <h3 className="text-lg font-bold mb-6">Predictive Horizon Model (Next 4 Hours)</h3>
                        <div className="space-y-4">
                            {[
                                { asset: 'Payment-Gateway-Redis', risk: 'Capacity Exhaustion', prob: '96%', tti: '45m', action: 'Auto-Scaling Authorized' },
                                { asset: 'Inventory-DB-Primary', risk: 'IOPS Saturation', prob: '82%', tti: '1h 15m', action: 'Pending Human Approval' },
                                { asset: 'Frontend-AKS-Cluster-EU', risk: 'Latency Degradation', prob: '64%', tti: '2h 30m', action: 'Monitoring' }
                            ].map((row, idx) => (
                                <div key={idx} className="flex flex-col md:flex-row md:items-center justify-between p-6 bg-[#020617]/50 rounded-2xl border border-white/5">
                                    <div className="flex flex-col mb-4 md:mb-0">
                                        <span className="font-bold text-sm text-indigo-300">{row.asset}</span>
                                        <span className="text-xs text-slate-400 mt-1">{row.risk}</span>
                                    </div>
                                    <div className="flex items-center gap-6">
                                        <div className="flex flex-col items-end">
                                            <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Probability</span>
                                            <span className="text-sm font-black text-rose-400">{row.prob}</span>
                                        </div>
                                        <div className="flex flex-col items-end border-l border-white/10 pl-6">
                                            <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Impact In</span>
                                            <span className="text-sm font-black text-white">{row.tti}</span>
                                        </div>
                                        <div className="flex flex-col border-l border-white/10 pl-6 w-48">
                                            <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1">Agent Status</span>
                                            <button className="text-xs font-bold py-1.5 px-3 bg-indigo-600/20 text-indigo-400 rounded-lg hover:bg-indigo-600 hover:text-white transition-all text-left">
                                                {row.action}
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Auto-Remediation Leaderboard & Controls */}
                    <div className="lg:col-span-4 bg-gradient-to-br from-indigo-900/40 to-slate-900/60 p-8 rounded-[3rem] border border-white/5">
                        <div className="flex justify-between items-center mb-6">
                            <h3 className="font-black text-xl leading-tight">Remediation Engine</h3>
                            <div className="w-3 h-3 bg-indigo-400 rounded-full animate-pulse"></div>
                        </div>
                        <p className="text-xs text-indigo-200/70 mb-8 leading-relaxed">
                            Continuous compliance enforces strict execution gates. Permissive policies execute under 30s.
                        </p>
                        <div className="space-y-4">
                            {[
                                { name: 'Redis Cache Flush', count: 142, success: '100%' },
                                { name: 'HPA Scale Replica+2', count: 89, success: '98%' },
                                { name: 'Node Pools Rotate', count: 12, success: '100%' }
                            ].map((job, idx) => (
                                <div key={idx} className="flex justify-between items-center bg-[#020617]/50 p-4 rounded-xl border border-white/5">
                                    <div className="flex flex-col">
                                        <span className="text-xs font-bold text-white">{job.name}</span>
                                        <span className="text-[10px] text-slate-500">{job.count} execs (30d)</span>
                                    </div>
                                    <span className="text-xs font-black text-emerald-400 bg-emerald-400/10 px-2 py-1 rounded-md">{job.success}</span>
                                </div>
                            ))}
                        </div>
                        <button className="w-full mt-8 py-3 bg-white text-slate-900 font-black text-xs uppercase tracking-widest rounded-xl hover:bg-indigo-600 hover:text-white transition-all">
                            Configure Policies
                        </button>
                    </div>
                </div>
            </main>
        </div>
    );
};

export default Dashboard;
