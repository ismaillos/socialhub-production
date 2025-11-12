
import React, { createContext, useContext, useState, ReactNode } from "react";
export type UILang = "fr" | "en" | "ar";
type LangContextType = { lang: UILang; setLang: (l: UILang) => void };
const LanguageContext = createContext<LangContextType | undefined>(undefined);
export const LanguageProvider = ({ children }: { children: ReactNode }) => {
  const [lang, setLang] = useState<UILang>("fr");
  return <LanguageContext.Provider value={{ lang, setLang }}>{children}</LanguageContext.Provider>;
};
export const useLanguage = () => {
  const ctx = useContext(LanguageContext);
  if (!ctx) throw new Error("useLanguage must be used inside LanguageProvider");
  return ctx;
};
