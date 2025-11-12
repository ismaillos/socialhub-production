
import { ReactNode } from "react";
import Header from "./Header";
import Footer from "./Footer";
import { useLanguage } from "../context/LanguageContext";

export default function Layout({ children }: { children: ReactNode }){
  const { lang } = useLanguage();
  return (
    <div dir={lang==="ar"?"rtl":"ltr"} className="min-h-screen flex flex-col bg-hero-gradient">
      <Header />
      <main className="flex-1 container py-8">{children}</main>
      <Footer />
    </div>
  );
}
