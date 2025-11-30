import React, { useState } from 'react';
import { Ghost, LogIn, Mail, Lock, ArrowRight, UserPlus } from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';

interface LoginPageProps {
  onLogin: (email: string, password: string) => Promise<void>;
  onSwitchToRegister: () => void;
  isLoading?: boolean;
}

const LoginPage: React.FC<LoginPageProps> = ({ onLogin, onSwitchToRegister, isLoading = false }) => {
  const { t } = useLanguage();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    
    if (!email || !password) {
      setError(t.auth.fillAllFields);
      return;
    }

    try {
      await onLogin(email, password);
    } catch (err: any) {
      setError(err.message || t.auth.loginError);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-6 bg-white relative">
      {/* Background Grid */}
      <div className="absolute inset-0 z-0 opacity-10" 
           style={{ backgroundImage: 'linear-gradient(#000 1px, transparent 1px), linear-gradient(90deg, #000 1px, transparent 1px)', backgroundSize: '40px 40px' }}>
      </div>

      <div className="relative z-10 w-full max-w-md">
        {/* Logo */}
        <div className="flex items-center justify-center gap-3 mb-8">
          <div className="w-12 h-12 bg-black rounded-none flex items-center justify-center text-white border-2 border-black">
            <Ghost size={24} className="fill-current" />
          </div>
          <span className="font-black text-2xl tracking-tighter text-black uppercase">
            GhostPen
          </span>
        </div>

        {/* Login Card */}
        <div className="bg-white border-2 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] p-8">
          <div className="mb-6">
            <h2 className="text-3xl font-black text-black uppercase tracking-tighter mb-2">
              {t.auth.loginTitle}
            </h2>
            <p className="text-sm text-slate-600 font-bold">
              {t.auth.loginSubtitle}
            </p>
          </div>

          {error && (
            <div className="mb-4 p-3 bg-red-50 border-2 border-red-500 text-red-700 text-sm font-bold">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Email */}
            <div>
              <label className="block text-xs font-black text-black uppercase tracking-wider mb-2">
                {t.auth.email}
              </label>
              <div className="relative">
                <Mail size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 border-2 border-black bg-white text-black font-bold focus:outline-none focus:bg-[#ccff00] transition-all"
                  placeholder="your@email.com"
                  disabled={isLoading}
                />
              </div>
            </div>

            {/* Password */}
            <div>
              <label className="block text-xs font-black text-black uppercase tracking-wider mb-2">
                {t.auth.password}
              </label>
              <div className="relative">
                <Lock size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 border-2 border-black bg-white text-black font-bold focus:outline-none focus:bg-[#ccff00] transition-all"
                  placeholder="••••••••"
                  disabled={isLoading}
                />
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full group relative px-6 py-4 bg-black text-white text-base font-black uppercase tracking-wide border-2 border-black transition-all hover:-translate-y-1 hover:shadow-[6px_6px_0px_0px_#ccff00] active:translate-y-0 active:shadow-none disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {isLoading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent animate-spin"></div>
                  <span>{t.auth.loading}</span>
                </>
              ) : (
                <>
                  <LogIn size={18} />
                  <span>{t.auth.loginButton}</span>
                  <ArrowRight size={18} className="group-hover:translate-x-1 transition-transform" />
                </>
              )}
            </button>
          </form>

          {/* Switch to Register */}
          <div className="mt-6 pt-6 border-t-2 border-black">
            <p className="text-sm text-slate-600 font-bold text-center mb-3">
              {t.auth.switchToRegister.split('?')[0]}?
            </p>
            <button
              onClick={onSwitchToRegister}
              className="w-full px-6 py-3 bg-white text-black text-sm font-black uppercase tracking-wide border-2 border-black transition-all hover:bg-[#ccff00] hover:-translate-y-0.5 hover:shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] flex items-center justify-center gap-2"
            >
              <UserPlus size={16} />
              <span>{t.auth.switchToRegister.split('? ')[1]}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;

