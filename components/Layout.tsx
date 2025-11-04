
import React, { ReactNode } from "react";
import Header from "./Header";
import Footer from "./Footer";
import { useLanguage } from "../context/LanguageContext";

type Props = {
  children: ReactNode;
};

const Layout: React.FC<Props> = ({ children }) => {
  const { lang } = useLanguage();

  return (
    <div
      dir={lang === "ar" ? "rtl" : "ltr"}
      className="min-h-screen flex flex-col bg-slate-50"
    >
      <Header />
      <main className="flex-1 max-w-6xl w-full mx-auto px-4 py-8">
        {children}
      </main>
      <Footer />
    </div>
  );
};

export default Layout;
