import React from 'react';
import { Cpu, Layers, Zap, Database, Sparkles, Brain, Fingerprint, Code2, Palette, Globe, Heart, Terminal, Cpu as Processor } from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';

const AboutPage = () => {
  const { t } = useLanguage();
  return (
    <div className="animate-fade-in pb-20 bg-white min-h-screen font-sans text-slate-900 overflow-x-hidden">
      
      {/* --- GLOBAL BACKGROUND --- */}
      <div className="fixed inset-0 z-0 pointer-events-none bg-[linear-gradient(rgba(0,0,0,0.05)_1px,transparent_1px),linear-gradient(90deg,rgba(0,0,0,0.05)_1px,transparent_1px)] bg-[size:40px_40px]"></div>

      {/* --- HERO: The Vision --- */}
      <div className="relative pt-40 pb-20 px-6 border-b-4 border-black bg-[#ccff00]">
        
        <div className="max-w-6xl mx-auto relative z-20">
          <div className="inline-flex items-center gap-2 px-3 py-1 bg-black text-white text-xs font-mono font-bold uppercase mb-8 border-2 border-transparent">
            <Terminal size={12} className="text-[#ccff00]" />
            <span>{t.about.systemManifesto}</span>
          </div>
          
          <h1 className="text-6xl md:text-8xl lg:text-9xl font-black mb-8 tracking-tighter leading-[0.85] uppercase text-black">
            {t.about.weBuilt} <br />
            <span className="text-white text-stroke-black">{t.about.digitalMirror}</span>
          </h1>
          
          <div className="max-w-2xl bg-white border-4 border-black p-6 md:p-8 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]">
            <p className="text-lg md:text-xl text-black font-bold leading-tight">
              {t.about.digitalMirrorDesc}
            </p>
          </div>
        </div>
      </div>

      {/* --- THE STORY: Why we built this --- */}
      <div className="max-w-5xl mx-auto px-6 py-32 relative z-30">
        <div className="flex flex-col md:flex-row gap-12 items-start">
            
            {/* Left: Decoration */}
            <div className="hidden md:block w-24 pt-4">
                <div className="w-full h-4 bg-black mb-2"></div>
                <div className="w-3/4 h-4 bg-black mb-2"></div>
                <div className="w-1/2 h-4 bg-black"></div>
            </div>

            {/* Content */}
            <div className="flex-1">
                <h2 className="text-4xl md:text-6xl font-black text-black mb-8 uppercase tracking-tighter">
                    {t.about.blankPageProblem}
                </h2>
                
                <div className="bg-white border-4 border-black p-8 md:p-12 shadow-[12px_12px_0px_0px_rgba(0,0,0,1)] hover:translate-x-1 hover:translate-y-1 hover:shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] transition-all">
                    <p className="text-lg md:text-xl font-medium leading-relaxed mb-6">
                        {t.about.blankPageDesc1}
                    </p>
                    <p className="text-lg md:text-xl font-medium leading-relaxed mb-6">
                        {t.about.blankPageDesc2}
                    </p>
                    <p className="text-lg md:text-xl font-black leading-relaxed">
                        {t.about.blankPageDesc3}
                    </p>
                </div>
            </div>
        </div>
      </div>

      {/* --- HOW IT WORKS: The Ghost Engine --- */}
      <div className="border-y-4 border-black bg-black text-white py-32">
        <div className="max-w-7xl mx-auto px-6">
            <div className="mb-20 flex flex-col md:flex-row items-end justify-between gap-6">
                <div>
                    <h2 className="text-5xl md:text-7xl font-black uppercase tracking-tighter text-[#ccff00] mb-2">{t.about.theEngine}</h2>
                    <p className="font-mono text-slate-400">{t.about.pipelineVisualization}</p>
                </div>
                <div className="hidden md:flex gap-2">
                    {[1,2,3,4].map(i => <div key={i} className="w-4 h-12 bg-white/20 skew-x-12"></div>)}
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                
                {/* Step 1 */}
                <div className="group border-2 border-white/20 bg-white/5 p-8 hover:bg-[#ccff00] hover:border-[#ccff00] hover:text-black transition-colors duration-300">
                    <div className="font-mono text-xs font-bold mb-4 opacity-50 group-hover:opacity-100">01_INPUT_ANALYSIS</div>
                    <div className="mb-6 group-hover:scale-110 transition-transform origin-left">
                        <Fingerprint size={48} />
                    </div>
                    <h3 className="text-2xl font-black mb-4 uppercase">{t.about.deconstruct}</h3>
                    <p className="text-sm font-mono leading-relaxed opacity-80 group-hover:opacity-100 group-hover:font-bold">
                        {t.about.deconstructDesc}
                    </p>
                </div>

                {/* Step 2 */}
                <div className="group border-2 border-white/20 bg-white/5 p-8 hover:bg-[#ccff00] hover:border-[#ccff00] hover:text-black transition-colors duration-300">
                    <div className="font-mono text-xs font-bold mb-4 opacity-50 group-hover:opacity-100">02_LLM_INJECTION</div>
                    <div className="mb-6 group-hover:scale-110 transition-transform origin-left">
                        <Brain size={48} />
                    </div>
                    <h3 className="text-2xl font-black mb-4 uppercase">{t.about.synthesize}</h3>
                    <p className="text-sm font-mono leading-relaxed opacity-80 group-hover:opacity-100 group-hover:font-bold">
                        {t.about.synthesizeDesc}
                    </p>
                </div>

                {/* Step 3 */}
                <div className="group border-2 border-white/20 bg-white/5 p-8 hover:bg-[#ccff00] hover:border-[#ccff00] hover:text-black transition-colors duration-300">
                    <div className="font-mono text-xs font-bold mb-4 opacity-50 group-hover:opacity-100">03_PLATFORM_ADAPT</div>
                    <div className="mb-6 group-hover:scale-110 transition-transform origin-left">
                        <Globe size={48} />
                    </div>
                    <h3 className="text-2xl font-black mb-4 uppercase">{t.about.adapt}</h3>
                    <p className="text-sm font-mono leading-relaxed opacity-80 group-hover:opacity-100 group-hover:font-bold">
                        {t.about.adaptDesc}
                    </p>
                </div>

            </div>
        </div>
      </div>

      {/* --- TECH STACK: The Building Blocks --- */}
      <div className="max-w-7xl mx-auto px-6 py-32">
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-16 gap-6">
            <div>
                <h2 className="text-5xl md:text-7xl font-black uppercase tracking-tighter text-black">{t.about.underTheHood}</h2>
            </div>
            <div className="flex items-center gap-2 font-mono text-xs font-bold bg-black text-white px-3 py-1">
                <Zap size={12} className="text-[#ccff00]" />
                {t.about.fastStack}
            </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            
            <div className="bg-white border-4 border-black p-6 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] hover:-translate-y-1 hover:shadow-[12px_12px_0px_0px_rgba(0,0,0,1)] transition-all">
                <div className="mb-4 bg-black w-10 h-10 flex items-center justify-center text-white"><Code2 size={20} /></div>
                <h4 className="font-black text-xl mb-2 uppercase">{t.about.react19}</h4>
                <p className="text-xs font-mono text-slate-500">{t.about.react19Desc}</p>
            </div>

            <div className="bg-white border-4 border-black p-6 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] hover:-translate-y-1 hover:shadow-[12px_12px_0px_0px_rgba(0,0,0,1)] transition-all">
                <div className="mb-4 bg-black w-10 h-10 flex items-center justify-center text-white"><Palette size={20} /></div>
                <h4 className="font-black text-xl mb-2 uppercase">{t.about.tailwind}</h4>
                <p className="text-xs font-mono text-slate-500">{t.about.tailwindDesc}</p>
            </div>

            <div className="bg-white border-4 border-black p-6 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] hover:-translate-y-1 hover:shadow-[12px_12px_0px_0px_rgba(0,0,0,1)] transition-all">
                <div className="mb-4 bg-black w-10 h-10 flex items-center justify-center text-white"><Terminal size={20} /></div>
                <h4 className="font-black text-xl mb-2 uppercase">{t.about.vite}</h4>
                <p className="text-xs font-mono text-slate-500">{t.about.viteDesc}</p>
            </div>

            <div className="bg-white border-4 border-black p-6 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] hover:-translate-y-1 hover:shadow-[12px_12px_0px_0px_rgba(0,0,0,1)] transition-all">
                <div className="mb-4 bg-black w-10 h-10 flex items-center justify-center text-white"><Processor size={20} /></div>
                <h4 className="font-black text-xl mb-2 uppercase">{t.about.genAI}</h4>
                <p className="text-xs font-mono text-slate-500">{t.about.genAIDesc}</p>
            </div>

        </div>
      </div>

      {/* --- FOOTER / CREDIT --- */}
      <div className="border-t-4 border-black py-12 text-center bg-white">
        <p className="flex items-center justify-center gap-2 font-black uppercase text-sm tracking-widest">
            {t.about.madeWith} <Heart size={16} className="text-black fill-black" /> {t.about.forHackathon}
        </p>
      </div>

    </div>
  );
};

export default AboutPage;