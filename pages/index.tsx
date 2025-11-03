
import Link from "next/link";
import Layout from "../components/Layout";
import { useLanguage } from "../context/LanguageContext";

export default function Home() {
  const { lang } = useLanguage();

  const t = {
    heroTitle1:
      lang === "fr" ? "Crée ton prochain" : "Create your next",
    heroTitle2:
      lang === "fr"
        ? "contenu viral en 60 secondes."
        : "viral content in 60 seconds.",
    heroSubtitle:
      lang === "fr"
        ? "Décris ton idée. L’IA écrit le texte, propose le visuel et les hashtags. Tu n’as plus qu’à publier."
        : "Describe your idea. AI writes the text, suggests the visual and hashtags. You just hit publish.",
    ctaMain: lang === "fr" ? "🚀 Créer un contenu" : "🚀 Create content",
    ctaSecondary:
      lang === "fr" ? "Voir comment ça marche" : "See how it works",
    badgeText:
      lang === "fr"
        ? "Studio IA pour créateurs, freelances et marques."
        : "AI studio for creators, freelancers and brands.",
    badge1Title: lang === "fr" ? "Gratuit au début" : "Free to start",
    badge1Text:
      lang === "fr" ? "3 contenus / jour inclus" : "3 creations / day included",
    badge2Title:
      lang === "fr" ? "Pensé pour le Maroc" : "Designed for Morocco & beyond",
    badge2Text:
      lang === "fr"
        ? "FR / AR / EN · Social & business"
        : "FR / AR / EN · Social & business",
    sectionHowTitle:
      lang === "fr" ? "Comment ça marche ?" : "How does it work?",
    step1Title: lang === "fr" ? "1. Tu décris ton idée" : "1. Describe your idea",
    step1Text:
      lang === "fr"
        ? "Vidéo, post, reel… Tu choisis le type de contenu, la langue et le ton."
        : "Video, post, reel… You choose content type, language and tone.",
    step2Title: lang === "fr" ? "2. L’IA génère" : "2. AI generates",
    step2Text:
      lang === "fr"
        ? "Viralloby te propose un script, une idée de visuel et des hashtags optimisés."
        : "Viralloby suggests a script, a visual idea and optimized hashtags.",
    step3Title: lang === "fr" ? "3. Tu publies" : "3. You publish",
    step3Text:
      lang === "fr"
        ? "Tu copies-colles dans Instagram, TikTok ou LinkedIn… et tu observes les réactions."
        : "You paste into Instagram, TikTok or LinkedIn… and watch the reactions."
  };

  return (
    <Layout>
      <div className="grid md:grid-cols-2 gap-10 items-center">
        <div className="space-y-6">
          <span className="inline-flex items-center gap-2 text-xs px-3 py-1 rounded-full bg-vlPurple/10 text-vlPurple border border-vlPurple/30">
            <span className="w-2 h-2 rounded-full bg-vlPurple" />
            {t.badgeText}
          </span>

          <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold text-slate-900 leading-tight">
            {t.heroTitle1}
            <span className="text-vlPurple block">{t.heroTitle2}</span>
          </h1>

          <p className="text-sm sm:text-base text-slate-600 max-w-xl">
            {t.heroSubtitle}
          </p>

          <div className="flex flex-wrap gap-3">
            <Link
              href="/create"
              className="inline-flex items-center justify-center px-5 py-3 rounded-xl bg-vlPurple text-white text-sm font-medium shadow hover:bg-vlPurple/90"
            >
              {t.ctaMain}
            </Link>
            <a
              href="#how-it-works"
              className="inline-flex items-center justify-center px-4 py-3 rounded-xl border border-slate-300 text-sm text-slate-700 bg-white hover:bg-slate-50"
            >
              {t.ctaSecondary}
            </a>
          </div>

          <div className="flex gap-6 text-xs text-slate-500">
            <div>
              <div className="font-semibold text-slate-800">
                {t.badge1Title}
              </div>
              <div>{t.badge1Text}</div>
            </div>
            <div>
              <div className="font-semibold text-slate-800">
                {t.badge2Title}
              </div>
              <div>{t.badge2Text}</div>
            </div>
          </div>
        </div>

        <div className="bg-white border border-slate-200 rounded-3xl p-4 sm:p-6 shadow-sm">
          <h2 className="text-sm font-semibold text-slate-800 mb-3">
            {lang === "fr"
              ? "Exemple de contenu généré"
              : "Example of generated content"}
          </h2>
          <div className="space-y-3 text-xs text-slate-700">
            <div className="border border-slate-200 rounded-2xl p-3">
              <div className="text-[11px] text-slate-400 mb-1">
                Script vidéo · {lang === "fr" ? "FR" : "EN"}
              </div>
              <p>
                {lang === "fr"
                  ? `“Tu penses que le digital n'est pas pour toi ? En 2025, même un simple smartphone peut devenir ton meilleur outil de travail...”`
                  : `"You think digital is not for you? In 2025, even a simple smartphone can become your best work tool..."`}
              </p>
            </div>
            <div className="border border-slate-200 rounded-2xl p-3">
              <div className="text-[11px] text-slate-400 mb-1">
                {lang === "fr" ? "Idée visuel" : "Visual idea"}
              </div>
              <p>
                {lang === "fr"
                  ? "Jeune marocain·e dans un café, ordinateur portable, ambiance chaleureuse."
                  : "Young Moroccan in a café, laptop open, warm and modern atmosphere."}
              </p>
            </div>
            <div className="border border-slate-200 rounded-2xl p-3">
              <div className="text-[11px] text-slate-400 mb-1">
                Hashtags
              </div>
              <p>#viralloby #ai #contentcreator #morocco #futureofwork</p>
            </div>
          </div>
        </div>
      </div>

      <section id="how-it-works" className="mt-16 space-y-6">
        <h2 className="text-xl font-semibold text-slate-900">
          {t.sectionHowTitle}
        </h2>
        <div className="grid sm:grid-cols-3 gap-4 text-sm">
          <div className="bg-white border border-slate-200 rounded-2xl p-4">
            <div className="text-2xl mb-2">✏️</div>
            <div className="font-semibold mb-1">{t.step1Title}</div>
            <p className="text-slate-600">{t.step1Text}</p>
          </div>
          <div className="bg-white border border-slate-200 rounded-2xl p-4">
            <div className="text-2xl mb-2">🤖</div>
            <div className="font-semibold mb-1">{t.step2Title}</div>
            <p className="text-slate-600">{t.step2Text}</p>
          </div>
          <div className="bg-white border border-slate-200 rounded-2xl p-4">
            <div className="text-2xl mb-2">📲</div>
            <div className="font-semibold mb-1">{t.step3Title}</div>
            <p className="text-slate-600">{t.step3Text}</p>
          </div>
        </div>
      </section>
    </Layout>
  );
}
