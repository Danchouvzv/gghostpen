import React, { useState, useEffect } from 'react';
import { Github, Ghost, Layout, Info, ArrowRight } from 'lucide-react';
import { Author, SocialNetwork, GenerateRequest, GenerateResponse, AppStatus } from './types';
// Переключатель между mock и реальным API
// Для разработки используйте mockApi, для продакшена - api
import { generatePost, getAuthors } from './services/api';
// import { generatePost } from './services/mockApi'; // Раскомментируйте для mock режима

import ControlPanel from './components/ControlPanel';
import DebugPanel from './components/DebugPanel';
import ResultPanel from './components/ResultPanel';
import AboutPage from './components/AboutPage';
import LandingPage from './components/LandingPage';

type View = 'landing' | 'playground' | 'about';

function App() {
  // --- Navigation State ---
  const [currentView, setCurrentView] = useState<View>('landing');

  // --- App Logic State ---
  const [authors, setAuthors] = useState<Author[]>([]);
  const [authorsLoading, setAuthorsLoading] = useState<boolean>(true);
  const [selectedAuthor, setSelectedAuthor] = useState<Author | null>(null);
  const [selectedNetwork, setSelectedNetwork] = useState<SocialNetwork>('linkedin');
  const [topic, setTopic] = useState<string>('');
  
  const [status, setStatus] = useState<AppStatus>(AppStatus.IDLE);
  const [requestData, setRequestData] = useState<GenerateRequest | null>(null);
  const [responseData, setResponseData] = useState<GenerateResponse | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Загружаем авторов с бэкенда при старте
  useEffect(() => {
    const loadAuthors = async () => {
      try {
        setAuthorsLoading(true);
        const response = await getAuthors();
        // Преобразуем данные из API в формат Author
        const authorsData: Author[] = response.authors.map((author: any) => ({
          id: author.id,
          name: author.name,
          profession: author.profession || '', // Профессия из API
          role: author.profession ? author.profession : `${author.total_posts} постов`, // Профессия или количество постов
          avatar: `https://picsum.photos/id/${parseInt(author.id.replace('person_', '')) * 10}/200/200`, // Генерируем аватар
          samplePosts: author.sample_posts || [], // Используем примеры постов из API
          stats: {
            formality: author.stats.formality === 'formal' ? 'High' : author.stats.formality === 'emotional' ? 'Medium' : 'Low',
            avgLength: author.stats.avgLength,
            emojiDensity: author.stats.emojiDensity
          }
        }));
        setAuthors(authorsData);
        setAuthorsLoading(false);
      } catch (error) {
        console.error('Ошибка загрузки авторов:', error);
        setAuthorsLoading(false);
      }
    };

    loadAuthors();
  }, []);

  // --- Handlers ---
  const handleGenerate = async () => {
    if (!selectedAuthor || !topic) return;

    // 1. Build Request
    const request: GenerateRequest = {
      author_id: selectedAuthor.id,
      social_network: selectedNetwork,
      topic: topic,
      sample_posts: selectedAuthor.samplePosts
    };

    setRequestData(request);
    setStatus(AppStatus.LOADING);
    setErrorMsg(null);
    setResponseData(null);

    // Scroll to debug panel on mobile/tablet to show progress
    if (window.innerWidth < 1024) {
       document.getElementById('result-panel')?.scrollIntoView({ behavior: 'smooth' });
    }

    try {
      // 2. Call API
      const result = await generatePost(request);
      
      // 3. Handle Success
      setResponseData(result);
      setStatus(AppStatus.SUCCESS);
    } catch (err: any) {
      // 4. Handle Error
      console.error(err);
      setErrorMsg(err.message || 'Failed to connect to the generation service.');
      setStatus(AppStatus.ERROR);
    }
  };

  return (
    <div className="min-h-screen flex flex-col font-sans text-slate-900 bg-white">
      
      {/* --- Neo-Brutalist Navbar --- */}
      <header className="fixed top-6 left-1/2 -translate-x-1/2 z-50 w-auto max-w-[95vw]">
        <div className="bg-white rounded-none border-2 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] px-3 md:px-5 h-16 flex items-center gap-3 md:gap-6 transition-transform hover:-translate-y-0.5">
          
          {/* Logo */}
          <button 
            className="flex items-center gap-2 group p-1" 
            onClick={() => setCurrentView('landing')}
          >
            <div className="relative w-9 h-9 bg-black rounded-none flex items-center justify-center text-white border-2 border-transparent group-hover:bg-[#ccff00] group-hover:text-black group-hover:border-black transition-all duration-200">
                <Ghost size={20} className="fill-current" />
            </div>
            <span className="font-black text-lg tracking-tighter text-black hidden sm:block uppercase">
              GhostPen
            </span>
          </button>

          <div className="w-0.5 h-8 bg-black hidden sm:block"></div>

          {/* Nav Items */}
          <nav className="flex items-center gap-1 sm:p-0">
            <button 
              onClick={() => setCurrentView('playground')}
              className={`flex items-center gap-1.5 px-4 py-2 rounded-none text-[10px] md:text-xs font-black uppercase tracking-wide transition-all duration-200 border-2 ${
                currentView === 'playground' 
                  ? 'bg-[#ccff00] border-black text-black shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] -translate-y-0.5' 
                  : 'bg-transparent border-transparent text-slate-500 hover:text-black hover:bg-slate-100'
              }`}
            >
              <Layout size={14} className="hidden sm:block" /> Playground
            </button>
            <button 
              onClick={() => setCurrentView('about')}
              className={`flex items-center gap-1.5 px-4 py-2 rounded-none text-[10px] md:text-xs font-black uppercase tracking-wide transition-all duration-200 border-2 ${
                currentView === 'about' 
                  ? 'bg-[#ccff00] border-black text-black shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] -translate-y-0.5' 
                  : 'bg-transparent border-transparent text-slate-500 hover:text-black hover:bg-slate-100'
              }`}
            >
              <Info size={14} className="hidden sm:block" /> About
            </button>
          </nav>

          <div className="hidden md:flex items-center gap-3 pl-2">
             <div className="flex items-center gap-1 text-[10px] font-black text-black bg-slate-100 border-2 border-black px-2 py-1 shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]">
                <span>EN</span>
             </div>
             <a 
               href="https://github.com/Danchouvzv/gghostpen" 
               target="_blank" 
               rel="noopener noreferrer"
               className="p-2 text-black hover:bg-[#ccff00] border-2 border-transparent hover:border-black transition-all"
             >
               <Github size={20} />
             </a>
          </div>
        </div>
      </header>

      {/* --- Main Content --- */}
      <main className="flex-1 w-full flex flex-col">
        {currentView === 'landing' && (
          <LandingPage onStart={() => setCurrentView('playground')} />
        )}

        {currentView === 'playground' && (
          <div className="animate-fade-in flex-1 pt-32 pb-6 px-4 md:px-6 lg:px-8 max-w-[1920px] mx-auto w-full relative">
            
            {/* Playground Background Pattern */}
            <div className="fixed inset-0 z-[-1] pointer-events-none bg-[linear-gradient(rgba(0,0,0,0.05)_1px,transparent_1px),linear-gradient(90deg,rgba(0,0,0,0.05)_1px,transparent_1px)] bg-[size:20px_20px]"></div>
            
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 h-full min-h-[700px]">
              
              {/* Left: Controls (3 Cols) */}
              <div className="lg:col-span-3 h-auto lg:h-[calc(100vh-160px)] animate-slide-up" style={{ animationDelay: '0.1s' }}>
                <ControlPanel 
                  authors={authors}
                  authorsLoading={authorsLoading}
                  selectedAuthor={selectedAuthor}
                  setSelectedAuthor={setSelectedAuthor}
                  selectedNetwork={selectedNetwork}
                  setSelectedNetwork={setSelectedNetwork}
                  topic={topic}
                  setTopic={setTopic}
                  onGenerate={handleGenerate}
                  isGenerating={status === AppStatus.LOADING}
                />
              </div>

              {/* Center: Stage/Result (6 Cols - Increased Focus) */}
              <div id="result-panel" className="lg:col-span-6 h-[600px] lg:h-[calc(100vh-160px)] animate-slide-up" style={{ animationDelay: '0.2s' }}>
                <ResultPanel 
                  status={status}
                  response={responseData}
                  network={selectedNetwork}
                  error={errorMsg}
                  author={selectedAuthor}
                />
              </div>

              {/* Right: Inspector/Debug (3 Cols) */}
              <div className="lg:col-span-3 h-[400px] lg:h-[calc(100vh-160px)] animate-slide-up" style={{ animationDelay: '0.3s' }}>
                <DebugPanel 
                  request={requestData}
                  response={responseData}
                  author={selectedAuthor}
                />
              </div>

            </div>
          </div>
        )}

        {currentView === 'about' && (
          <AboutPage />
        )}
      </main>
      
    </div>
  );
}

export default App;