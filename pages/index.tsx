
import Link from "next/link";
import Layout from "../components/Layout";
import { useLanguage } from "../context/LanguageContext";

export default function Home() {
  const { lang } = useLanguage();

  const t = {
    heroTitle1:
      lang === "fr"
        ? "Crée ton prochain"
        : lang === "ar"
        ? "أنشئ المحتوى التالي"
        : "Create your next",
    heroTitle2:
      lang === "fr"
        ? "contenu viral en 60 secondes."
        : lang === "ar"
        ? "محتوى منتشر خلال ٦٠ ثانية."
        : "viral content in 60 seconds.",
    heroSubtitle:
      lang === "fr"
        ? "Décris ton idée. Viralobby Studio écrit le texte, propose le visuel et les hashtags. Tu n’as plus qu’à publier."
        : lang === "ar"
        ? "صف فكرتك. يقوم Viralobby Studio بإنشاء النص واقتراح التصور البصري والوسوم المناسبة. كل ما عليك فعله هو النشر."
        : "Describe your idea. Viralobby Studio writes the text, suggests the visual and hashtags. You just hit publish.",
    ctaMain:
      lang === "fr"
        ? "🚀 Créer un contenu"
        : lang === "ar"
        ? "🚀 أنشئ محتوى الآن"
        : "🚀 Create content",
    ctaSecondary:
      lang === "fr"
        ? "Voir comment ça marche"
        : lang === "ar"
        ? "كيف يعمل؟"
        : "See how it works",
    badgeText:
      lang === "fr"
        ? "Studio IA pour créateurs, freelances et marques."
        : lang === "ar"
        ? "استوديو للذكاء الاصطناعي مخصص لصناع المحتوى، المستقلين والعلامات التجارية."
        : "AI studio for creators, freelancers and brands.",
    badge1Title:
      lang === "fr"
        ? "Gratuit au début"
        : lang === "ar"
        ? "مجاناً في البداية"
        : "Free to start",
    badge1Text:
      lang === "fr"
        ? "3 contenus / jour inclus"
        : lang === "ar"
        ? "٣ محتويات يومياً مشمولة"
        : "3 creations / day included",
    badge2Title:
      lang === "fr"
        ? "Pensé pour le Maroc"
        : lang === "ar"
        ? "مصمم للمغرب والمنطقة"
        : "Designed for Morocco & beyond",
    badge2Text:
      lang === "fr"
        ? "FR / AR / EN · Social & business"
        : lang === "ar"
        ? "الفرنسية / العربية / الإنجليزية · محتوى اجتماعي وتجاري"
        : "FR / AR / EN · Social & business",
    sectionHowTitle:
      lang === "fr"
        ? "Comment ça marche ?"
        : lang === "ar"
        ? "كيف يعمل Viralobby Studio؟"
        : "How does it work?",
    step1Title:
      lang === "fr"
        ? "1. Tu décris ton idée"
        : lang === "ar"
        ? "١. صف فكرتك"
        : "1. Describe your idea",
    step1Text:
      lang === "fr"
        ? "Vidéo, post, reel… Tu choisis le type de contenu, la langue et le ton."
        : lang === "ar"
        ? "فيديو، منشور، أو مقطع قصير… تختار نوع المحتوى، اللغة والأسلوب."
        : "Video, post, reel… You choose content type, language and tone.",
    step2Title:
      lang === "fr"
        ? "2. L’IA génère"
        : lang === "ar"
        ? "٢. الذكاء الاصطناعي ينشئ المحتوى"
        : "2. AI generates",
    step2Text:
      lang === "fr"
        ? "Viralobby Studio te propose un script, une idée de visuel et des hashtags optimisés."
        : lang === "ar"
        ? "يقترح Viralobby Studio نصاً جاهزاً، وفكرة واضحة للتصور البصري، ووسوماً محسّنة."
        : "Viralobby Studio suggests a script, a visual idea and optimized hashtags.",
    step3Title:
      lang === "fr"
        ? "3. Tu publies"
        : lang === "ar"
        ? "٣. تنشر وتتابع النتائج"
        : "3. You publish",
    step3Text:
      lang === "fr"
        ? "Tu copies-colles dans Instagram, TikTok ou LinkedIn… et tu observes les réactions."
        : lang === "ar"
        ? "تنسخ المحتوى وتنشره على إنستغرام، تيك توك أو لينكدإن… ثم تتابع التفاعل والنتائج."
        : "You paste into Instagram, TikTok or LinkedIn… and watch the reactions.",
    exampleTitle:
      lang === "fr"
        ? "Exemple de contenu généré"
        : lang === "ar"
        ? "مثال على محتوى مُنشأ"
        : "Example of generated content"
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
            {t.exampleTitle}
          </h2>
          <div className="space-y-3 text-xs text-slate-700">
            <div className="border border-slate-200 rounded-2xl p-3">
              <div className="text-[11px] text-slate-400 mb-1">
                {lang === "fr"
                  ? "Script vidéo · FR"
                  : lang === "ar"
                  ? "نص فيديو قصير · AR"
                  : "Video script · EN"}
              </div>
              <p>
                {lang === "fr"
                  ? "“Tu penses que le digital n'est pas pour toi ? En 2025, même un simple smartphone peut devenir ton meilleur outil de marketing…”"
                  : lang === "ar"
                  ? "« هل تعتقد أن التسويق الرقمي ليس مناسباً لك؟ في عام ٢٠٢٥ يمكن أن يصبح الهاتف الذكي وحده أقوى أداة لتسويق مشروعك. دع Viralobby Studio يساعدك على إطلاق أول حملة لك. »"
                  : "“You think digital marketing is not for you? In 2025, even a simple smartphone can become your most powerful business tool. Let Viralobby Studio help you launch your first campaign.”"}
              </p>
            </div>
            <div className="border border-slate-200 rounded-2xl p-3">
              <div className="text-[11px] text-slate-400 mb-1">
                {lang === "fr"
                  ? "Idée visuel"
                  : lang === "ar"
                  ? "فكرة التصور البصري"
                  : "Visual idea"}
              </div>
              <p>
                {lang === "fr"
                  ? "Jeune créateur·ice marocain·e, téléphone à la main, interface de réseaux sociaux, ambiance moderne."
                  : lang === "ar"
                  ? "شاب أو شابة من المغرب يحمل هاتفاً ذكياً، مع واجهة شبكات اجتماعية على الشاشة وألوان عصرية جذابة."
                  : "Young Moroccan creator holding a smartphone, social media interface on screen, modern and vibrant colors."}
              </p>
            </div>
            <div className="border border-slate-200 rounded-2xl p-3">
              <div className="text-[11px] text-slate-400 mb-1">
                Hashtags
              </div>
              <p>#viralobby #ai #contentcreator #digitalmarketing #morocco</p>
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
