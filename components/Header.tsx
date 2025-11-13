
import Link from "next/link";
import Image from "next/image";
import { useLanguage } from "../context/LanguageContext";

const Header = () => {
  const { lang, setLang } = useLanguage();
  return (
    <header className="sticky top-0 z-30 border-b bg-white/70 backdrop-blur">
      <div className="container py-3 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-3">
          <Image src="/logo.png" alt="Viralobby Studio" width={42} height={42} className="rounded-xl" />
          <span className="text-base sm:text-lg font-semibold text-vl_primary">Viralobby Studio</span>
        </Link>
        <nav className="flex items-center gap-4 text-sm">
          <Link href="/create" className="text-slate-700 hover:text-vl_primary">Create</Link>
          <Link href="/templates" className="text-slate-700 hover:text-vl_primary">Templates</Link>
          <div className="vl-chip border-slate-300 bg-white">
            <button onClick={() => setLang("fr")} className={lang==="fr"?"font-semibold text-vl_primary":"opacity-60"}>FR</button>
            <span className="text-slate-300">|</span>
            <button onClick={() => setLang("en")} className={lang==="en"?"font-semibold text-vl_primary":"opacity-60"}>EN</button>
            <span className="text-slate-300">|</span>
            <button onClick={() => setLang("ar")} className={lang==="ar"?"font-semibold text-vl_primary":"opacity-60"}>AR</button>
          </div>
        </nav>
      </div>
    </header>
  );
};
export default Header;
