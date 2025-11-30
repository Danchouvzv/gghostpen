import React, { useState } from 'react';
import { GenerateResponse, SocialNetwork, AppStatus, Author } from '../types';
import { Copy, Check, BarChart3, Heart, MessageCircle, Share2, MoreHorizontal, Send, ThumbsUp, Repeat, Bookmark, Smartphone, Monitor, Globe, Sparkles, RefreshCcw } from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';

interface ResultPanelProps {
  status: AppStatus;
  response: GenerateResponse | null;
  network: SocialNetwork;
  error: string | null;
  author: Author | null;
}

const ResultPanel: React.FC<ResultPanelProps> = ({ status, response, network, error, author }) => {
  const { t } = useLanguage();
  const [copied, setCopied] = useState(false);
  const [viewMode, setViewMode] = useState<'mobile' | 'desktop'>('mobile');

  const handleCopy = () => {
    if (response?.generated_post) {
      navigator.clipboard.writeText(response.generated_post);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const renderContent = () => {
    const text = response?.generated_post || "";
    // Используем данные выбранного автора или дефолтные значения
    const userImg = author?.avatar || "https://picsum.photos/id/64/50/50";
    const userName = author?.name || "Author";
    const userProfession = author?.profession || author?.role || "";
    
    // Internal content remains mostly realistic but with sharper borders
    switch (network) {
        case 'linkedin':
            return (
                <div className="bg-white border-2 border-slate-200 font-sans text-sm">
                    <div className="p-3 border-b border-slate-100 flex gap-2 items-start">
                         <img src={userImg} className="w-10 h-10" alt="" />
                         <div className="flex-1">
                            <div className="font-bold text-slate-900 flex justify-between">
                                <span>{userName}</span>
                                <MoreHorizontal size={16} className="text-slate-400" />
                            </div>
                            <div className="text-xs text-slate-500">{userProfession || t.result.author} • 12{t.result.hoursAgo} • <Globe size={10} className="inline"/></div>
                         </div>
                    </div>
                    <div className="p-3 text-slate-900 whitespace-pre-wrap leading-relaxed">
                        {text}
                    </div>
                    <div className="p-2 border-t border-slate-100 flex justify-between text-slate-500">
                        <div className="flex flex-col items-center gap-1 px-2 py-1"><ThumbsUp size={16} /><span className="text-xs">{t.result.like}</span></div>
                        <div className="flex flex-col items-center gap-1 px-2 py-1"><MessageCircle size={16} /><span className="text-xs">{t.result.comment}</span></div>
                        <div className="flex flex-col items-center gap-1 px-2 py-1"><Repeat size={16} /><span className="text-xs">{t.result.repost}</span></div>
                        <div className="flex flex-col items-center gap-1 px-2 py-1"><Send size={16} /><span className="text-xs">{t.result.send}</span></div>
                    </div>
                </div>
            );
        case 'instagram':
             return (
                 <div className="bg-white border-2 border-slate-200 font-sans text-sm pb-4">
                     <div className="p-3 flex items-center justify-between">
                         <div className="flex items-center gap-2">
                            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-yellow-400 to-purple-600 p-[2px]">
                                <img src={userImg} className="w-full h-full rounded-full border border-white" alt="" />
                            </div>
                            <span className="font-bold text-xs">{userName.toLowerCase().replace(' ', '_')}</span>
                         </div>
                         <MoreHorizontal size={16} />
                     </div>
                     <div className="aspect-square bg-slate-100 border-y border-slate-200">
                        <img src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&q=80&w=600" className="w-full h-full object-cover grayscale hover:grayscale-0 transition-all duration-500" alt="" />
                     </div>
                     <div className="p-3 pb-0 flex justify-between mb-2">
                        <div className="flex gap-4">
                            <Heart size={22} className="text-slate-900" />
                            <MessageCircle size={22} className="text-slate-900" />
                            <Send size={22} className="text-slate-900" />
                        </div>
                        <Bookmark size={22} className="text-slate-900" />
                     </div>
                     <div className="px-3 text-xs">
                        <p><span className="font-bold mr-1">{userName.toLowerCase().replace(' ', '_')}</span>{text}</p>
                     </div>
                 </div>
             );
        default:
            return (
                <div className="bg-white border-2 border-slate-200 p-4 text-sm text-slate-800 whitespace-pre-wrap leading-relaxed">
                    {text}
                </div>
            )
    }
  }

  return (
    <div className="bg-white border-2 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] h-full flex flex-col relative overflow-hidden">
        
        {/* Stage Header */}
        <div className="h-16 bg-white border-b-2 border-black px-4 flex justify-between items-center z-20">
            <div className="flex items-center gap-2 text-black">
                <span className="text-lg font-black uppercase tracking-tighter">{t.result.stage}</span>
            </div>
            
            <div className="flex gap-2">
                <button 
                    onClick={() => setViewMode('mobile')}
                    className={`p-2 border-2 transition-all ${
                        viewMode === 'mobile' 
                        ? 'bg-black text-white border-black shadow-[2px_2px_0px_0px_#ccff00]' 
                        : 'bg-white text-black border-black hover:bg-slate-50'
                    }`}
                >
                    <Smartphone size={18} />
                </button>
                <button 
                    onClick={() => setViewMode('desktop')}
                    className={`p-2 border-2 transition-all ${
                        viewMode === 'desktop' 
                        ? 'bg-black text-white border-black shadow-[2px_2px_0px_0px_#ccff00]' 
                        : 'bg-white text-black border-black hover:bg-slate-50'
                    }`}
                >
                    <Monitor size={18} />
                </button>
            </div>
        </div>

        {/* Stage Content Area */}
        <div className="flex-1 overflow-y-auto custom-scrollbar relative flex items-center justify-center p-8 bg-slate-50">
            
            {/* Background Grid */}
            <div className="absolute inset-0 z-0 opacity-10" 
                 style={{ backgroundImage: 'linear-gradient(#000 1px, transparent 1px), linear-gradient(90deg, #000 1px, transparent 1px)', backgroundSize: '40px 40px' }}>
            </div>

            {status === AppStatus.SUCCESS && response ? (
                <div className={`relative z-10 transition-all duration-500 ease-out ${viewMode === 'mobile' ? 'w-[375px]' : 'w-full max-w-2xl'}`}>
                     
                     {/* Toolbar above Preview */}
                     <div className="flex justify-end mb-4 gap-2 animate-fade-in">
                        <button 
                            onClick={handleCopy}
                            className="bg-[#ccff00] border-2 border-black text-black text-xs font-bold uppercase tracking-wide px-4 py-2 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] transition-all flex items-center gap-2"
                        >
                            {copied ? <Check size={14} /> : <Copy size={14} />}
                            {copied ? t.result.copied.toUpperCase() : t.result.copy.toUpperCase() + ' TEXT'}
                        </button>
                     </div>

                     {/* The Post Content */}
                     <div className="animate-slide-up border-2 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] bg-white overflow-hidden">
                        {renderContent()}
                     </div>

                </div>
            ) : status === AppStatus.LOADING ? (
                <div className="flex flex-col items-center justify-center z-10">
                    <div className="w-16 h-16 border-4 border-black border-t-[#ccff00] animate-spin mb-6"></div>
                    <h3 className="text-xl font-black text-black uppercase tracking-tighter">{t.common.loading}</h3>
                    <div className="font-mono text-xs text-slate-500 mt-2 bg-white border border-black px-2 py-1">
                        PROCESS_ID: {Math.floor(Math.random() * 9999)}
                    </div>
                </div>
            ) : (
                // Empty State
                <div className="text-center max-w-sm z-10">
                    <div className="w-24 h-24 bg-white border-2 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] flex items-center justify-center mx-auto mb-6">
                        <Sparkles size={40} className="text-black" />
                    </div>
                    <h3 className="text-2xl font-black text-black uppercase tracking-tighter mb-2">{t.result.stage} {t.common.loading}</h3>
                    <p className="text-sm text-slate-600 font-medium">
                        {t.playground.selectAuthor} {t.playground.selectPlatform} {t.playground.enterTopic}
                    </p>
                </div>
            )}
        </div>
    </div>
  );
};

export default ResultPanel;