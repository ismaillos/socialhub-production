
import Link from "next/link";
import { useLanguage } from "../context/LanguageContext";

const Header = () => {
  const { lang, setLang } = useLanguage();

  return (
    <header className="border-b bg-white/80 backdrop-blur sticky top-0 z-20">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link href="/">
          <div className="flex items-center gap-2 cursor-pointer">
            <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-vlPurple to-vlPink flex items-center justify-center text-white font-bold text-lg">
              V
            </div>
            <div className="leading-tight">
              <div className="font-semibold text-slate-900">Viralloby Studio</div>
              <div className="text-xs text-slate-500">
                {lang === "fr"
                  ? "Crée ton contenu viral avec l’IA"
                  : "Create your viral content with AI"}
              </div>
            </div>
          </div>
        </Link>

        <nav className="flex items-center gap-4 text-sm">
          <Link
            href="/create"
            className="text-slate-700 hover:text-vlPurple"
          >
            {lang === "fr" ? "Créer un contenu" : "Create content"}
          </Link>
          <div className="inline-flex items-center gap-1 text-xs border px-2 py-1 rounded-full text-slate-600 bg-slate-50">
            <button
              type="button"
              onClick={() => setLang("fr")}
              className={`px-1 ${
                lang === "fr" ? "font-semibold text-vlPurple" : "opacity-60"
              }`}
            >
              FR
            </button>
            <span className="text-slate-300">|</span>
            <button
              type="button"
              onClick={() => setLang("en")}
              className={`px-1 ${
                lang === "en" ? "font-semibold text-vlPurple" : "opacity-60"
              }`}
            >
              EN
            </button>
          </div>
        </nav>
      </div>
    </header>
  );
};

export default Header;
