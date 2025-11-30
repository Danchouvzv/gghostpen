import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { ru } from '../locales/ru';
import { en } from '../locales/en';

export type Language = 'ru' | 'en';

type Translations = typeof ru;

interface LanguageContextType {
  language: Language;
  setLanguage: (lang: Language) => void;
  t: Translations;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within LanguageProvider');
  }
  return context;
};

interface LanguageProviderProps {
  children: ReactNode;
}

export const LanguageProvider: React.FC<LanguageProviderProps> = ({ children }) => {
  const [language, setLanguageState] = useState<Language>(() => {
    const saved = localStorage.getItem('ghostpen_language');
    return (saved as Language) || 'ru';
  });

  useEffect(() => {
    localStorage.setItem('ghostpen_language', language);
  }, [language]);

  const setLanguage = (lang: Language) => {
    setLanguageState(lang);
  };

  const translations: Translations = language === 'ru' ? ru : en;

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t: translations }}>
      {children}
    </LanguageContext.Provider>
  );
};

