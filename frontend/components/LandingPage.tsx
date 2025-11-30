import React from 'react';
import { ArrowRight, Bot, PenTool, Globe2, MoveRight, Terminal, Fingerprint, Code, Zap } from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';

interface LandingPageProps {
  onStart: () => void;
}

const LandingPage: React.FC<LandingPageProps> = ({ onStart }) => {
  const { t } = useLanguage();
  const companies = [
    'LINEAR', 'VERCEL', 'NOTION', 'RAYCAST', 'FIGMA', 'ARC', 'RAMP', 'MERCURY'
  ];

  return (
    <div className="relative min-h-screen flex flex-col font-sans overflow-x-hidden bg-white text-slate-900">
      
      {/* --- GLOBAL NOISE & GRID --- */}
      <div className="fixed inset-0 z-0 pointer-events-none">
          {/* Noise Overlay */}
          <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 mix-blend-overlay"></div>
          {/* Subtle Grid */}
          <div className="absolute inset-0 bg-[linear-gradient(rgba(0,0,0,0.05)_1px,transparent_1px),linear-gradient(90deg,rgba(0,0,0,0.05)_1px,transparent_1px)] bg-[size:40px_40px]"></div>
      </div>

      {/* --- HERO SECTION --- */}
      <div className="relative pt-32 pb-20 lg:pt-40 lg:pb-32 px-6 overflow-hidden">
        
        <div className="max-w-[1200px] mx-auto relative z-10 text-center flex flex-col items-center">
          
          {/* Badge */}
          <div className="animate-slide-up inline-flex items-center gap-2 px-4 py-1.5 bg-[#ccff00] text-black border-2 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] text-xs font-black uppercase tracking-widest mb-10 hover:-translate-y-0.5 transition-transform cursor-pointer">
             <span className="w-2 h-2 bg-black"></span>
             {t.landing.badge}
          </div>

          {/* Headline - Brutalist */}
          <h1 className="animate-slide-up text-6xl md:text-8xl lg:text-9xl font-black tracking-tighter leading-[0.9] text-black mb-8 uppercase">
            {t.landing.headline.split(' ').slice(0, 2).join(' ')} <br />
            <span className="bg-[#ccff00] px-4 italic">{t.landing.headline.split(' ').slice(2).join(' ')}</span>
          </h1>

          <p className="animate-slide-up text-xl md:text-2xl text-slate-600 max-w-2xl mx-auto mb-12 font-bold tracking-tight" style={{ animationDelay: '0.1s' }}>
             {t.landing.tagline} <br/>
             <span className="text-black bg-slate-200 px-1">{t.landing.tagline2.split('.')[0]}.</span> {t.landing.tagline2.split('.').slice(1).join('.').trim()}
          </p>

          {/* CTA Buttons - Neo Brutalist */}
          <div className="animate-slide-up flex flex-col sm:flex-row gap-6 items-center" style={{ animationDelay: '0.2s' }}>
             <button 
               onClick={onStart}
               className="group relative px-8 py-4 bg-black text-white text-lg font-bold border-2 border-black transition-all hover:-translate-y-1 hover:shadow-[6px_6px_0px_0px_#ccff00] active:translate-y-0 active:shadow-none"
             >
                <div className="relative z-10 flex items-center gap-2 uppercase tracking-wide">
                   {t.landing.startCreating} <MoveRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </div>
             </button>

             <button className="px-8 py-4 bg-white text-black border-2 border-black text-lg font-bold hover:bg-slate-50 transition-all hover:-translate-y-1 hover:shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] active:translate-y-0 active:shadow-none flex items-center gap-2 uppercase tracking-wide">
                {t.landing.watchDemo}
             </button>
          </div>

          {/* Flat Interface Mockup (Replaces 3D) */}
          <div className="mt-24 w-full max-w-4xl mx-auto animate-slide-up" style={{ animationDelay: '0.3s' }}>
             <div className="bg-white border-4 border-black rounded-xl shadow-[12px_12px_0px_0px_rgba(0,0,0,1)] overflow-hidden">
                {/* Window Header */}
                <div className="bg-black p-3 flex items-center gap-3 border-b-4 border-black">
                   <div className="flex gap-2">
                      <div className="w-4 h-4 rounded-full bg-[#ff5f56] border-2 border-black"></div>
                      <div className="w-4 h-4 rounded-full bg-[#ffbd2e] border-2 border-black"></div>
                      <div className="w-4 h-4 rounded-full bg-[#27c93f] border-2 border-black"></div>
                   </div>
                   <div className="bg-slate-800 text-slate-400 px-4 py-1 rounded font-mono text-xs flex-1 text-center font-bold">
                      ghostpen_engine.exe
                   </div>
                   <div className="w-16"></div>
                </div>

                {/* Interface Body */}
                <div className="bg-slate-50 p-6 md:p-10 grid md:grid-cols-2 gap-8 text-left">
                   
                   {/* Col 1: Input */}
                   <div className="space-y-4">
                      <div className="font-black uppercase tracking-wider text-xs text-slate-400 mb-2">{t.landing.sourceInput}</div>
                      <div className="bg-white border-2 border-black p-4 rounded shadow-[4px_4px_0px_0px_rgba(0,0,0,0.1)] font-mono text-xs md:text-sm leading-relaxed text-slate-500">
                         <span className="text-purple-600 font-bold">@alex_rivera</span>: "Scaling teams is hard. Focus on culture."
                         <br/><br/>
                         <span className="text-green-600">// Analyzing vectors...</span>
                         <br/>
                         [FORMALITY: 0.8]
                         <br/>
                         [BREVITY: HIGH]
                      </div>
                   </div>

                   {/* Col 2: Output */}
                   <div className="space-y-4 relative">
                      <div className="absolute -left-4 top-1/2 -translate-y-1/2 hidden md:block">
                         <div className="bg-black text-white p-2 rounded-full border-2 border-black z-10">
                            <ArrowRight size={16} />
                         </div>
                      </div>
                      <div className="font-black uppercase tracking-wider text-xs text-brand-600 mb-2">{t.landing.generatedOutput}</div>
                      <div className="bg-[#ccff00] border-2 border-black p-4 rounded shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] font-sans font-bold text-sm md:text-base text-black relative">
                         "Building a team isn't just about headcount. It's about heart count. Culture scales when processes break. 🚀 #Leadership"
                         <div className="absolute -bottom-3 -right-3 bg-black text-white text-[10px] font-mono px-2 py-1 border-2 border-white">
                            {t.landing.match}: 99%
                         </div>
                      </div>
                   </div>

                </div>
             </div>
          </div>

        </div>
      </div>

      {/* --- INFINITE MARQUEE --- */}
      <div className="py-12 border-y-4 border-black bg-[#ccff00] overflow-hidden relative">
         <div className="flex animate-marquee whitespace-nowrap gap-20 items-center">
            {[...companies, ...companies, ...companies].map((name, i) => (
                <div key={i} className="flex items-center gap-20">
                    <span className="text-4xl font-black text-black uppercase tracking-tighter cursor-default italic">
                        {name}
                    </span>
                    <span className="text-4xl font-black text-black opacity-20">///</span>
                </div>
            ))}
         </div>
      </div>

      {/* --- BENTO GRID --- */}
      <div className="py-32 px-4 bg-white">
        <div className="max-w-[1200px] mx-auto">
            <h2 className="text-5xl md:text-7xl font-black text-center mb-20 tracking-tighter uppercase text-black">
                {t.landing.ghostEngine.split(' ').slice(0, 1).join(' ')} <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-pink-600 decoration-4 underline decoration-black">{t.landing.ghostEngine.split(' ').slice(1, 2).join(' ')}</span> {t.landing.ghostEngine.split(' ').slice(2).join(' ')}
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-6 gap-6">
                
                {/* 1. Large Feature - Analytics */}
                <div className="md:col-span-4 bg-white rounded-none border-4 border-black p-8 md:p-12 relative overflow-hidden group hover:shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] transition-all">
                    <div className="relative z-10 h-full flex flex-col">
                        <div className="w-16 h-16 bg-black text-white flex items-center justify-center mb-8 border-2 border-black shadow-[4px_4px_0px_0px_#ccff00]">
                            <Bot size={32} />
                        </div>
                        <h3 className="text-3xl font-black mb-4 uppercase tracking-tight">{t.landing.styleVectorization}</h3>
                        <p className="text-slate-600 text-lg mb-8 font-medium max-w-md border-l-4 border-[#ccff00] pl-4">
                            {t.landing.styleVectorizationDesc}
                        </p>
                        
                        <div className="mt-auto bg-slate-100 border-2 border-black p-6 font-mono text-xs text-black">
                             <div className="flex justify-between border-b-2 border-black pb-4 mb-4 font-bold">
                                <span>{t.landing.analysisMode}</span>
                                <span className="bg-green-500 text-white px-2">{t.landing.active}</span>
                             </div>
                             <div className="space-y-4">
                                <div className="space-y-1">
                                    <div className="flex justify-between font-bold"><span>{t.landing.toneFormal}</span><span>82%</span></div>
                                    <div className="w-full h-4 border-2 border-black p-0.5"><div className="h-full w-[82%] bg-black"></div></div>
                                </div>
                                <div className="space-y-1">
                                    <div className="flex justify-between font-bold"><span>{t.landing.witIndex}</span><span>45%</span></div>
                                    <div className="w-full h-4 border-2 border-black p-0.5"><div className="h-full w-[45%] bg-[#ccff00]"></div></div>
                                </div>
                             </div>
                        </div>
                    </div>
                </div>

                {/* 2. Tone Slider */}
                <div className="md:col-span-2 bg-[#ccff00] border-4 border-black p-8 flex flex-col justify-between group hover:shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] transition-all">
                    <div>
                        <div className="flex justify-between items-start mb-6">
                            <PenTool size={40} className="text-black" />
                            <div className="bg-white border-2 border-black px-2 py-1 text-[10px] font-black uppercase">{t.landing.control}</div>
                        </div>
                        <h3 className="text-3xl font-black text-black leading-none mb-2 uppercase">{t.landing.toneSlider}</h3>
                        <p className="text-black font-bold text-sm">{t.landing.toneSliderDesc}</p>
                    </div>
                    <div className="w-full h-8 bg-white border-2 border-black relative flex items-center px-2 mt-8">
                        <div className="w-6 h-6 bg-black border-2 border-white absolute left-[60%]"></div>
                    </div>
                </div>

                {/* 3. Multi-Platform */}
                <div className="md:col-span-3 bg-black text-white border-4 border-black p-10 flex flex-col relative group hover:translate-x-1 hover:translate-y-1 hover:shadow-none shadow-[8px_8px_0px_0px_#ccff00] transition-all">
                    <div className="absolute top-4 right-4 opacity-20">
                        <Globe2 size={80} />
                    </div>
                    <div className="relative z-10 mt-auto">
                        <h3 className="text-3xl font-black mb-2 uppercase">{t.landing.omnichannel}</h3>
                        <p className="text-gray-400 font-mono text-sm border-l-2 border-[#ccff00] pl-3">{t.landing.omnichannelDesc}</p>
                    </div>
                </div>

                 {/* 4. Code */}
                 <div className="md:col-span-3 bg-white border-4 border-black p-10 flex flex-col relative group hover:shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] transition-all">
                    <div className="absolute top-4 right-4 text-slate-200">
                        <Code size={80} />
                    </div>
                    <div className="font-mono text-xs space-y-2 text-slate-600 relative z-10">
                        <div className="text-green-600 font-bold">{t.landing.apiReady}</div>
                        <div className="bg-slate-100 p-2 border-2 border-slate-200">POST /v1/generate</div>
                    </div>
                    <h3 className="text-3xl font-black mt-6 uppercase">{t.landing.devFirst}</h3>
                </div>

            </div>
        </div>
      </div>

      {/* --- FOOTER CTA --- */}
      <div className="py-32 px-6 text-center bg-black text-white border-t-4 border-black">
         <h2 className="text-5xl md:text-8xl font-black mb-12 tracking-tighter uppercase">
            {t.landing.dontBeBoring.split(' ').slice(0, 2).join(' ')} <span className="text-[#ccff00] decoration-4 underline underline-offset-8 decoration-white">{t.landing.dontBeBoring.split(' ').slice(2).join(' ')}</span>
         </h2>
         <button 
           onClick={onStart}
           className="inline-flex items-center justify-center gap-3 px-12 py-6 bg-[#ccff00] text-black border-4 border-white rounded-full font-black text-xl hover:bg-white hover:border-[#ccff00] hover:scale-105 transition-all shadow-[8px_8px_0px_0px_rgba(255,255,255,0.2)]"
         >
            {t.landing.getEarlyAccess} <Zap size={24} fill="black" />
         </button>
      </div>

    </div>
  );
};

export default LandingPage;