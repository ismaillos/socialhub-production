
import Link from "next/link";
import Layout from "../components/Layout";
import { useLanguage } from "../context/LanguageContext";

type Template = {
  id: string;
  theme: string;
  tone: string;
  ideaFr: string;
  ideaEn: string;
  ideaAr: string;
  labelFr: string;
  labelEn: string;
  labelAr: string;
};

const templates: Template[] = [
  {
    id: "hook-ia-business",
    theme: "business",
    tone: "inspirant",
    labelFr: "Hook vidéo : lancer un business avec l’IA",
    labelEn: "Video hook: launch a business with AI",
    labelAr: "مقدمة فيديو: إطلاق مشروع باستخدام الذكاء الاصطناعي",
    ideaFr:
      "Je veux un script de vidéo courte qui montre comment une personne peut lancer un petit business rentable grâce à l’IA, même sans gros budget.",
    ideaEn:
      "I want a short video script showing how someone can launch a small profitable business using AI, even with a low budget.",
    ideaAr:
      "أريد نص فيديو قصير يوضح كيف يمكن لشخص أن يطلق مشروعاً صغيراً مربحاً باستخدام الذكاء الاصطناعي، حتى بميزانية محدودة."
  },
  {
    id: "carrousel-educatif",
    theme: "education",
    tone: "serieux",
    labelFr: "Carrousel éducatif : apprendre avec l’IA",
    labelEn: "Educational carousel: learning with AI",
    labelAr: "كاروسيل تعليمي: التعلّم بالذكاء الاصطناعي",
    ideaFr:
      "Je veux un texte pour un carrousel Instagram qui explique en 5 slides comment un étudiant peut utiliser l’IA pour mieux apprendre.",
    ideaEn:
      "I want text for an Instagram carousel with 5 slides explaining how a student can use AI to learn better.",
    ideaAr:
      "أريد نصاً لكاروسيل على إنستغرام من ٥ شرائح يشرح كيف يمكن للطالب استخدام الذكاء الاصطناعي لتحسين تعلّمه."
  },
  {
    id: "promo-offre",
    theme: "marketing",
    tone: "fun",
    labelFr: "Post promo : offre limitée -50%",
    labelEn: "Promo post: -50% limited offer",
    labelAr: "منشور ترويجي: عرض خاص -٥٠٪",
    ideaFr:
      "Je veux un texte court et dynamique pour annoncer une réduction de -50% sur une offre digitale, avec un appel à l’action clair.",
    ideaEn:
      "I want a short dynamic caption to announce a -50% discount on a digital offer, with a clear call to action.",
    ideaAr:
      "أريد نصاً قصيراً وحيوياً للإعلان عن خصم -٥٠٪ على عرض رقمي، مع دعوة واضحة لاتخاذ إجراء."
  }
];

export default function TemplatesPage() {
  const { lang } = useLanguage();

  const getIdea = (tpl: Template) =>
    lang === "fr" ? tpl.ideaFr : lang === "ar" ? tpl.ideaAr : tpl.ideaEn;

  const getLabel = (tpl: Template) =>
    lang === "fr" ? tpl.labelFr : lang === "ar" ? tpl.labelAr : tpl.labelEn;

  const title =
    lang === "fr"
      ? "Templates de contenus viraux"
      : lang === "ar"
      ? "قوالب محتوى جاهزة للانتشار"
      : "Viral content templates";

  const subtitle =
    lang === "fr"
      ? "Choisis un template, adapte quelques mots, et publie."
      : lang === "ar"
      ? "اختر قالباً، عدّل بعض الكلمات، ثم انشر."
      : "Pick a template, tweak a few words, and publish.";

  return (
    <Layout>
      <div className="space-y-4 mb-6">
        <h1 className="text-xl font-semibold text-slate-900">{title}</h1>
        <p className="text-sm text-slate-600">{subtitle}</p>
      </div>

      <div className="grid md:grid-cols-3 gap-4">
        {templates.map((tpl) => (
          <div
            key={tpl.id}
            className="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm flex flex-col justify-between"
          >
            <div className="space-y-2">
              <h2 className="text-sm font-semibold text-slate-900">
                {getLabel(tpl)}
              </h2>
              <p className="text-xs text-slate-600 line-clamp-5">
                {getIdea(tpl)}
              </p>
              <p className="text-[11px] text-slate-400 mt-1">
                {lang === "fr"
                  ? `Thème : ${tpl.theme} · Ton : ${tpl.tone}`
                  : lang === "ar"
                  ? `الموضوع: ${tpl.theme} · الأسلوب: ${tpl.tone}`
                  : `Theme: ${tpl.theme} · Tone: ${tpl.tone}`}
              </p>
            </div>
            <div className="mt-4">
              <Link
                href={{
                  pathname: "/create",
                  query: {
                    theme: tpl.theme,
                    tone: tpl.tone,
                    idea: getIdea(tpl)
                  }
                }}
                className="inline-flex items-center justify-center w-full px-3 py-2 text-xs rounded-xl bg-vlPurple text-white hover:bg-vlPurple/90"
              >
                {lang === "fr"
                  ? "Utiliser ce template"
                  : lang === "ar"
                  ? "استخدام هذا القالب"
                  : "Use this template"}
              </Link>
            </div>
          </div>
        ))}
      </div>
    </Layout>
  );
}
