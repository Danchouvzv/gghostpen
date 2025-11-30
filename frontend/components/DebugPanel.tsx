import React, { useState, useEffect } from 'react';
import { GenerateRequest, GenerateResponse, Author } from '../types';
import { Terminal, Code2, Database, Activity, Cpu, ChevronDown, List } from 'lucide-react';

interface DebugPanelProps {
  request: GenerateRequest | null;
  response: GenerateResponse | null;
  author: Author | null;
}

const DebugPanel: React.FC<DebugPanelProps> = ({ request, response, author }) => {
  const [activeTab, setActiveTab] = useState<'request' | 'response' | 'profile'>('response');
  const [logs, setLogs] = useState<string[]>([]);

  // Simulate logs
  useEffect(() => {
    if (response) {
        setLogs([
            `[10:42:01] Success: Output generated in ${response.debug.processing_time_ms}ms`,
            `[10:42:01] Token Usage: ${response.debug.prompt_tokens} tokens`,
            `[10:42:00] Inference: Model ghostpen-v1.4 active`,
            `[10:42:00] Vector DB: Retrieved context for ${author?.name}`,
            `[10:41:59] Pipeline: Request received`
        ]);
    } else {
        setLogs([]);
    }
  }, [response, author]);

  const renderJson = (data: any) => {
    if (!data) return <span className="text-slate-500 italic">// No data stream...</span>;
    return JSON.stringify(data, null, 2);
  };

  return (
    <div className="bg-black border-2 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] flex flex-col h-full font-mono text-xs overflow-hidden">
      
      {/* Inspector Header */}
      <div className="h-10 bg-black border-b-2 border-white/20 flex items-center px-4 justify-between">
          <span className="font-bold text-[#ccff00] uppercase tracking-widest flex items-center gap-2">
            <Activity size={14} /> SYSTEM_MONITOR
          </span>
          <div className="flex gap-1.5">
            <div className="w-2.5 h-2.5 bg-red-500 border border-black"></div>
            <div className="w-2.5 h-2.5 bg-yellow-500 border border-black"></div>
            <div className="w-2.5 h-2.5 bg-green-500 border border-black"></div>
          </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b-2 border-white/20 bg-black">
        {[
            { id: 'request', icon: Code2, label: 'REQ' },
            { id: 'response', icon: Terminal, label: 'RES' },
            { id: 'profile', icon: Database, label: 'DB' },
        ].map(tab => (
            <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex-1 py-3 flex items-center justify-center gap-2 transition-all ${
                    activeTab === tab.id 
                    ? 'bg-white text-black font-black' 
                    : 'bg-black text-slate-500 hover:text-[#ccff00] hover:bg-white/10'
                }`}
            >
                <tab.icon size={14} />
                <span className="font-bold hidden xl:inline">{tab.label}</span>
            </button>
        ))}
      </div>

      {/* Code Content */}
      <div className="flex-1 overflow-auto custom-scrollbar-dark p-4 bg-[#0a0a0a] relative group border-b-2 border-white/20">
         {activeTab === 'request' && (
             <div className="animate-fade-in text-blue-400">
                 <div className="text-slate-600 mb-2 border-b border-slate-800 pb-1">// PAYLOAD_TO_LLM</div>
                 <pre className="whitespace-pre-wrap break-all leading-relaxed">{renderJson(request)}</pre>
             </div>
         )}
         {activeTab === 'response' && (
             <div className="animate-fade-in text-[#ccff00]">
                 <div className="text-slate-600 mb-2 border-b border-slate-800 pb-1">// PIPELINE_OUTPUT</div>
                 <pre className="whitespace-pre-wrap break-all leading-relaxed">{renderJson(response)}</pre>
             </div>
         )}
         {activeTab === 'profile' && (
             <div className="animate-fade-in text-pink-400">
                 <div className="text-slate-600 mb-2 border-b border-slate-800 pb-1">// AUTHOR_VECTORS</div>
                 <pre className="whitespace-pre-wrap break-all leading-relaxed">{renderJson(author ? { ...author, samplePosts: '[Array]' } : null)}</pre>
             </div>
         )}
      </div>

      {/* System Log / Console */}
      <div className="bg-black h-1/3 flex flex-col">
          <div className="px-4 py-2 bg-white/5 border-b border-white/10 text-[10px] font-bold text-slate-400 uppercase flex items-center gap-2">
            <List size={12} /> Events
          </div>
          <div className="p-3 flex-1 overflow-auto custom-scrollbar-dark space-y-2">
              {logs.length > 0 ? logs.map((log, i) => (
                  <div key={i} className="font-mono text-[10px] text-slate-300 border-l-2 border-[#ccff00] pl-2 hover:bg-white/5">
                      {log}
                  </div>
              )) : (
                  <div className="text-slate-600 text-[10px] italic pt-4 text-center">... WAITING_FOR_INPUT ...</div>
              )}
          </div>
      </div>

    </div>
  );
};

export default DebugPanel;