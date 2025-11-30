import React, { useState } from 'react';
import { Author, SocialNetwork } from '../types';
import { SOCIAL_NETWORKS, MOCK_TOPICS } from '../constants';
import { User, CheckCircle2, Sparkles, AlertCircle, Dices, ChevronDown, ChevronRight, Sliders, Play, Loader2 } from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';

interface ControlPanelProps {
  authors: Author[];
  authorsLoading: boolean;
  selectedAuthor: Author | null;
  setSelectedAuthor: (author: Author | null) => void;
  selectedNetwork: SocialNetwork;
  setSelectedNetwork: (network: SocialNetwork) => void;
  topic: string;
  setTopic: (topic: string) => void;
  onGenerate: () => void;
  isGenerating: boolean;
}

const ControlPanel: React.FC<ControlPanelProps> = ({
  authors,
  authorsLoading,
  selectedAuthor,
  setSelectedAuthor,
  selectedNetwork,
  setSelectedNetwork,
  topic,
  setTopic,
  onGenerate,
  isGenerating,
}) => {
  const { t } = useLanguage();
  const [showProSettings, setShowProSettings] = useState(false);
  const [tone, setTone] = useState<'professional' | 'casual' | 'witty'>('professional');
  const [lengthVal, setLengthVal] = useState(50);
  
  const isValid = selectedAuthor && topic.length >= 5;

  const handleInspireMe = () => {
    const random = MOCK_TOPICS[Math.floor(Math.random() * MOCK_TOPICS.length)];
    setTopic(random);
  };

  return (
    <div className="bg-white border-2 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] flex flex-col h-full overflow-hidden">
      
      {/* Header */}
      <div className="p-4 border-b-2 border-black bg-white flex justify-between items-center">
        <div className="flex items-center gap-2 text-black">
           <Sliders size={20} className="text-black" />
           <h2 className="font-black text-lg uppercase tracking-tighter">Controls</h2>
        </div>
        <div className="flex gap-1">
            <div className="w-3 h-3 bg-black rounded-full"></div>
            <div className="w-3 h-3 bg-black/20 rounded-full"></div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto custom-scrollbar p-5 space-y-8 bg-white">
        
        {/* Author Selection */}
        <div className="space-y-4">
          <label className="text-xs font-black text-black uppercase tracking-wider flex justify-between items-center border-b-2 border-black pb-1">
            {t.control.persona}
            {selectedAuthor && <span className="text-black text-[10px] bg-[#ccff00] px-2 py-0.5 border border-black font-bold">{t.control.active}</span>}
          </label>
          <div className="space-y-3">
            {authorsLoading ? (
              <div className="flex items-center justify-center p-4 border-2 border-black bg-white">
                <Loader2 className="w-5 h-5 animate-spin text-black" />
                <span className="ml-2 text-xs font-bold text-black">{t.control.loading}</span>
              </div>
            ) : authors.length === 0 ? (
              <div className="p-4 border-2 border-black bg-white text-center">
                <span className="text-xs font-bold text-black">{t.control.notLoaded}</span>
              </div>
            ) : (
              authors.map((author) => (
                <button
                  key={author.id}
                  onClick={() => setSelectedAuthor(author)}
                  className={`w-full group relative flex items-center gap-3 p-3 border-2 transition-all duration-200 text-left ${
                    selectedAuthor?.id === author.id
                      ? 'border-black bg-[#ccff00] shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] -translate-y-1'
                      : 'border-black bg-white hover:bg-slate-50 hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:-translate-y-0.5'
                  } ${!author.is_demo ? 'ring-2 ring-blue-500' : ''}`}
                >
                  <div className="relative">
                     <img src={author.avatar} alt={author.name} className="w-10 h-10 rounded-none border-2 border-black object-cover" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <div className="font-bold text-sm truncate text-black uppercase">
                        {author.name}
                      </div>
                      {!author.is_demo && (
                        <span className="text-[8px] bg-blue-500 text-white px-1.5 py-0.5 border border-black font-black uppercase">
                          МОЙ
                        </span>
                      )}
                    </div>
                    <div className="text-[10px] text-slate-600 font-mono truncate">
                      {author.profession || author.role}
                    </div>
                  </div>
                </button>
              ))
            )}
          </div>
        </div>

        {/* Social Network Selection */}
        <div className="space-y-4">
          <label className="text-xs font-black text-black uppercase tracking-wider border-b-2 border-black pb-1 block">
            {t.control.platform}
            {selectedNetwork && <span className="ml-2 text-black text-[10px] bg-[#ccff00] px-2 py-0.5 border border-black font-bold">{t.control.active}</span>}
          </label>
          <div className="flex gap-3">
            {SOCIAL_NETWORKS.map((net) => {
              const Icon = net.icon;
              const isSelected = selectedNetwork === net.id;
              return (
                <button
                  key={net.id}
                  onClick={() => setSelectedNetwork(net.id)}
                  title={net.name}
                  className={`flex-1 flex items-center justify-center p-3 border-2 transition-all duration-200 ${
                    isSelected
                      ? 'border-black bg-black text-[#ccff00] shadow-[4px_4px_0px_0px_rgba(0,0,0,0.5)] -translate-y-1'
                      : 'border-black bg-white text-black hover:bg-slate-100 hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]'
                  }`}
                >
                  <Icon size={20} />
                </button>
              );
            })}
          </div>
        </div>

        {/* Topic Input */}
        <div className="space-y-4">
          <div className="flex justify-between items-center border-b-2 border-black pb-1">
             <label className="text-xs font-black text-black uppercase tracking-wider">{t.control.topic}</label>
             <button 
               onClick={handleInspireMe}
               className="text-[10px] font-bold flex items-center gap-1 text-black bg-[#ccff00] border border-black px-2 py-0.5 hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] transition-all"
             >
                <Dices size={12} /> Inspire Me
             </button>
          </div>
          <div className="relative">
              <textarea
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                placeholder={t.playground.enterTopic}
                rows={4}
                className="w-full p-4 border-2 border-black bg-slate-50 focus:bg-white focus:shadow-[4px_4px_0px_0px_#ccff00] outline-none resize-none transition-all text-sm text-black placeholder:text-slate-400 font-medium"
              />
          </div>
        </div>

        {/* Pro Settings (Collapsible) */}
        <div className="border-2 border-black bg-white">
            <button 
                onClick={() => setShowProSettings(!showProSettings)}
                className="w-full flex items-center justify-between p-3 bg-slate-100 hover:bg-slate-200 text-xs font-black text-black uppercase tracking-wider transition-colors"
            >
                <span>Pro Settings</span>
                {showProSettings ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
            </button>
            
            {showProSettings && (
                <div className="p-4 bg-white border-t-2 border-black space-y-5 animate-slide-up">
                    {/* Tone Chips */}
                    <div className="space-y-2">
                        <label className="text-[10px] font-black text-black uppercase">Tone</label>
                        <div className="flex flex-wrap gap-2">
                            {['professional', 'casual', 'witty'].map((t) => (
                                <button 
                                    key={t}
                                    onClick={() => setTone(t as any)}
                                    className={`px-3 py-1.5 text-[10px] font-bold border-2 transition-all uppercase ${
                                        tone === t 
                                        ? 'bg-black text-white border-black' 
                                        : 'bg-white text-black border-black hover:bg-slate-100'
                                    }`}
                                >
                                    {t}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Length Slider */}
                    <div className="space-y-2">
                        <div className="flex justify-between text-[10px] font-black text-black uppercase">
                            <span>Length</span>
                            <span>{lengthVal > 75 ? 'Long' : lengthVal < 25 ? 'Short' : 'Medium'}</span>
                        </div>
                        <input 
                            type="range" 
                            min="0" 
                            max="100" 
                            value={lengthVal}
                            onChange={(e) => setLengthVal(parseInt(e.target.value))}
                            className="w-full h-2 bg-slate-200 border-2 border-black rounded-none appearance-none cursor-pointer accent-black"
                        />
                    </div>
                </div>
            )}
        </div>

      </div>

      {/* Footer Action */}
      <div className="p-5 border-t-2 border-black bg-slate-50">
        <button
          onClick={onGenerate}
          disabled={!isValid || isGenerating}
          className={`w-full py-4 px-4 font-black text-sm uppercase tracking-wider flex items-center justify-center gap-2 border-2 transition-all duration-200 ${
            isValid && !isGenerating
              ? 'bg-black text-[#ccff00] border-black shadow-[6px_6px_0px_0px_#ccff00] hover:translate-x-1 hover:translate-y-1 hover:shadow-none'
              : 'bg-slate-200 text-slate-400 border-slate-300 cursor-not-allowed'
          }`}
        >
          {isGenerating ? (
              <span className="flex items-center gap-2">
                <span className="w-4 h-4 border-2 border-slate-500 border-t-[#ccff00] rounded-full animate-spin"></span>
                Processing...
              </span>
          ) : (
              <>
              {isGenerating ? t.playground.generating : t.playground.generate} <Play size={16} fill="#ccff00" />
              </>
          )}
        </button>
      </div>
    </div>
  );
};

export default ControlPanel;