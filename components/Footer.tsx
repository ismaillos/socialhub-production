
import { useLanguage } from "../context/LanguageContext";

const Footer = () => {
  const { lang } = useLanguage();

  return (
    <footer className="border-t bg-white">
      <div className="max-w-6xl mx-auto px-4 py-4 text-xs text-slate-500 flex flex-col sm:flex-row gap-2 sm:items-center sm:justify-between">
        <div>
          © {new Date().getFullYear()} Viralobby Studio · Casablanca, Morocco
        </div>
        <div>
          {lang === "fr"
            ? "Support :"
            : lang === "ar"
            ? "الدعم الفني:"
            : "Support:"}{" "}
          <a
            href="mailto:contact@viralobby.com"
            className="text-vlPurple hover:underline"
          >
            contact@viralobby.com
          </a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
