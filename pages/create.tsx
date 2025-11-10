
import React, { useState, useEffect } from "react";
import { useRouter } from "next/router";
import Layout from "../components/Layout";
import StepIndicator from "../components/StepIndicator";
import ContentPreview from "../components/ContentPreview";
import { useLanguage } from "../context/LanguageContext";

type ContentType = "video" | "post" | "carousel";
type GenLanguage = "FR" | "EN" | "AR";

export default function CreatePage() {
  const { lang } = useLanguage();
  const router = useRouter();

  const [contentType, setContentType] = useState<ContentType>("video");
  const [genLang, setGenLang] = useState<GenLanguage>("FR");
  const [theme, setTheme] = useState("marketing");
  const [tone, setTone] = useState("inspirant");
  const [idea, setIdea] = useState("");
  const [loading, setLoading] = useState(false);
  const [generatedText, setGeneratedText] = useState<string | undefined>();
  const [generatedHashtags, setGeneratedHashtags] = useState<string[] | undefined>();
  const [imagePrompt, setImagePrompt] = useState<string | undefined>();
  const [imageUrl, setImageUrl] = useState<string | undefined>();

  useEffect(() => {
    if (!router.isReady) return;
    const q = router.query;
    if (q.idea && typeof q.idea === "string") {
      setIdea(q.idea);
    }
    if (q.theme && typeof q.theme === "string") {
      setTheme(q.theme);
    }
    if (q.tone && typeof q.tone === "string") {
      setTone(q.tone);
    }
  }, [router.isReady, router.query]);

  const labels = {
    title:
      lang === "fr"
        ? "Décris ton idée"
        : lang === "ar"
        ? "صف فكرتك"
        : "Describe your idea",
    subtitle:
      lang === "fr"
        ? "Plus tu es précis, meilleur sera le contenu généré."
        : lang === "ar"
        ? "كلما كان وصفك دقيقاً، كان المحتوى المُنشأ أفضل."
        : "The more precise you are, the better the result.",
    typeLabel:
      lang === "fr"
        ? "Type de contenu"
        : lang === "ar"
        ? "نوع المحتوى"
        : "Content type",
    langLabel:
      lang === "fr"
        ? "Langue du contenu"
        : lang === "ar"
        ? "لغة المحتوى"
        : "Content language",
    themeLabel:
      lang === "fr"
        ? "Thème"
        : lang === "ar"
        ? "الموضوع"
        : "Theme",
    toneLabel:
      lang === "fr"
        ? "Ton du contenu"
        : lang === "ar"
        ? "أسلوب المحتوى"
        : "Tone",
    ideaLabel:
      lang === "fr"
        ? "Décris ton idée en une phrase"
        : lang === "ar"
        ? "صف فكرتك في جملة واحدة"
        : "Describe your idea in one sentence",
    ideaPlaceholder:
      lang === "fr"
        ? "Ex : Je veux une vidéo qui explique comment utiliser l’IA pour lancer un petit business local."
        : lang === "ar"
        ? "مثال: أريد فيديو قصيراً يشرح كيف يمكن استخدام الذكاء الاصطناعي لإطلاق مشروع محلي صغير."
        : "Ex: I want a short video that explains how to use AI to start a small local business.",
    rightsNote:
      lang === "fr"
        ? "Tu gardes 100% de tes droits sur le contenu généré."
        : lang === "ar"
        ? "تحتفظ بنسبة ١٠٠٪ من حقوقك على المحتوى الذي تم إنشاؤه."
        : "You keep 100% of the rights on the generated content.",
    generateBtn: loading
      ? lang === "fr"
        ? "Génération en cours..."
        : lang === "ar"
        ? "جاري توليد المحتوى..."
        : "Generating..."
      : lang === "fr"
      ? "🚀 Générer mon contenu"
      : lang === "ar"
      ? "🚀 أنشئ المحتوى الآن"
      : "🚀 Generate my content",
    copyText:
      lang === "fr"
        ? "📋 Copier le texte"
        : lang === "ar"
        ? "📋 نسخ النص"
        : "📋 Copy text",
    copyTags:
      lang === "fr"
        ? "# Copier les hashtags"
        : lang === "ar"
        ? "# نسخ الوسوم"
        : "# Copy hashtags",
    genImage:
      lang === "fr"
        ? "🎨 Générer l’image avec l’IA"
        : lang === "ar"
        ? "🎨 توليد صورة بالذكاء الاصطناعي"
        : "🎨 Generate image with AI"
  };

  const handleGenerate = async () => {
    if (!idea.trim()) return;
    setLoading(true);
    setGeneratedText(undefined);
    setGeneratedHashtags(undefined);
    setImagePrompt(undefined);
    setImageUrl(undefined);

    try {
      const res = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          contentType,
          language: genLang,
          theme,
          tone,
          idea
        })
      });

      if (!res.ok) {
        throw new Error("API error");
      }

      const data = await res.json();
      setGeneratedText(data.text);
      setGeneratedHashtags(data.hashtags);
      setImagePrompt(data.imagePrompt);
    } catch (err) {
      console.error(err);
      alert(
        lang === "fr"
          ? "Une erreur est survenue. Réessaie dans un instant."
          : lang === "ar"
          ? "حدث خطأ ما. يُرجى المحاولة مرة أخرى بعد قليل."
          : "An error occurred. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateImage = async () => {
    const prompt = imagePrompt || idea;
    if (!prompt) return;

    setLoading(true);
    try {
      const res = await fetch("/api/generate-image", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt })
      });

      if (!res.ok) throw new Error("Image API error");

      const data = await res.json();
      setImageUrl(data.imageUrl);
    } catch (err) {
      console.error(err);
      alert(
        lang === "fr"
          ? "Impossible de générer l’image pour le moment."
          : lang === "ar"
          ? "تعذَّر توليد الصورة حالياً."
          : "Could not generate image right now."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleCopyText = () => {
    if (!generatedText) return;
    navigator.clipboard.writeText(generatedText).catch(() => {});
  };

  const handleCopyHashtags = () => {
    if (!generatedHashtags) return;
    navigator.clipboard.writeText(
      generatedHashtags.map((h) => `#${h}`).join(" ")
    );
  };

  return (
    <Layout>
      <StepIndicator current={2} />

      <div className="grid lg:grid-cols-[minmax(0,1.2fr)_minmax(0,1fr)] gap-6">
        <div className="bg-white border border-slate-200 rounded-2xl p-4 sm:p-5 shadow-sm space-y-4">
          <h1 className="text-lg font-semibold text-slate-900 mb-1">
            {labels.title}
          </h1>
          <p className="text-xs text-slate-500 mb-2">{labels.subtitle}</p>

          {/* Type de contenu */}
          <div>
            <label className="block text-xs font-medium text-slate-700 mb-1">
              {labels.typeLabel}
            </label>
            <div className="inline-flex flex-wrap gap-2">
              <button
                type="button"
                onClick={() => setContentType("video")}
                className={`px-3 py-1.5 rounded-full text-xs border ${
                  contentType === "video"
                    ? "bg-vlPurple text-white border-vlPurple"
                    : "bg-white text-slate-700 border-slate-300"
                }`}
              >
                🎬{" "}
                {lang === "fr"
                  ? "Vidéo courte (Reel/TikTok)"
                  : lang === "ar"
                  ? "فيديو قصير (ريل / تيك توك)"
                  : "Short video (Reel/TikTok)"}
              </button>

              <button
                type="button"
                onClick={() => setContentType("post")}
                className={`px-3 py-1.5 rounded-full text-xs border ${
                  contentType === "post"
                    ? "bg-vlPurple text-white border-vlPurple"
                    : "bg-white text-slate-700 border-slate-300"
                }`}
              >
                🖼️{" "}
                {lang === "fr"
                  ? "Post image + texte"
                  : lang === "ar"
                  ? "منشور صورة مع نص"
                  : "Image + text post"}
              </button>

              <button
                type="button"
                onClick={() => setContentType("carousel")}
                className={`px-3 py-1.5 rounded-full text-xs border ${
                  contentType === "carousel"
                    ? "bg-vlPurple text-white border-vlPurple"
                    : "bg-white text-slate-700 border-slate-300"
                }`}
              >
                📜{" "}
                {lang === "fr"
                  ? "Carrousel (séquence d’images + texte)"
                  : lang === "ar"
                  ? "كاروسيل (تسلسل صور مع نص)"
                  : "Carousel (sequence of images + text)"}
              </button>
            </div>
          </div>

          {/* Langue du contenu */}
          <div>
            <label className="block text-xs font-medium text-slate-700 mb-1">
              {labels.langLabel}
            </label>
            <div className="inline-flex gap-2 text-xs">
              {(["FR", "EN", "AR"] as GenLanguage[]).map((l) => (
                <button
                  key={l}
                  type="button"
                  onClick={() => setGenLang(l)}
                  className={`px-3 py-1.5 rounded-full border ${
                    genLang === l
                      ? "bg-vlPink text-white border-vlPink"
                      : "bg-white text-slate-700 border-slate-300"
                  }`}
                >
                  {l === "FR"
                    ? "Français"
                    : l === "EN"
                    ? "English"
                    : "العربية"}
                </button>
              ))}
            </div>
          </div>

          {/* Thème */}
          <div>
            <label className="block text-xs font-medium text-slate-700 mb-1">
              {labels.themeLabel}
            </label>
            <div className="flex flex-wrap gap-2 text-xs">
              {[
                [
                  "marketing",
                  lang === "fr"
                    ? "Marketing digital"
                    : lang === "ar"
                    ? "التسويق الرقمي"
                    : "Digital marketing"
                ],
                [
                  "business",
                  lang === "fr"
                    ? "Business / Freelance"
                    : lang === "ar"
                    ? "الأعمال / العمل الحر"
                    : "Business / Freelance"
                ],
                [
                  "education",
                  lang === "fr"
                    ? "Éducation"
                    : lang === "ar"
                    ? "التعليم"
                    : "Education"
                ],
                [
                  "social",
                  lang === "fr"
                    ? "Social / Impact"
                    : lang === "ar"
                    ? "اجتماعي / أثر"
                    : "Social / Impact"
                ],
                [
                  "autre",
                  lang === "fr"
                    ? "Autre"
                    : lang === "ar"
                    ? "موضوع آخر"
                    : "Other"
                ]
              ].map(([value, label]) => (
                <button
                  type="button"
                  key={value}
                  onClick={() => setTheme(value as string)}
                  className={`px-3 py-1.5 rounded-full border ${
                    theme === value
                      ? "bg-slate-900 text-white border-slate-900"
                      : "bg-white text-slate-700 border-slate-300"
                  }`}
                >
                  {label}
                </button>
              ))}
            </div>
          </div>

          {/* Ton */}
          <div>
            <label className="block text-xs font-medium text-slate-700 mb-1">
              {labels.toneLabel}
            </label>
            <div className="flex flex-wrap gap-2 text-xs">
              {[
                [
                  "inspirant",
                  lang === "fr"
                    ? "Inspirant & motivant"
                    : lang === "ar"
                    ? "ملهم ومحفِّز"
                    : "Inspiring & motivational"
                ],
                [
                  "serieux",
                  lang === "fr"
                    ? "Sérieux & pro"
                    : lang === "ar"
                    ? "جدي واحترافي"
                    : "Serious & professional"
                ],
                [
                  "fun",
                  lang === "fr"
                    ? "Fun & léger"
                    : lang === "ar"
                    ? "خفيف وممتع"
                    : "Fun & light"
                ]
              ].map(([value, label]) => (
                <button
                  type="button"
                  key={value}
                  onClick={() => setTone(value as string)}
                  className={`px-3 py-1.5 rounded-full border ${
                    tone === value
                      ? "bg-slate-900 text-white border-slate-900"
                      : "bg-white text-slate-700 border-slate-300"
                  }`}
                >
                  {label}
                </button>
              ))}
            </div>
          </div>

          {/* Idée */}
          <div>
            <label className="block text-xs font-medium text-slate-700 mb-1">
              {labels.ideaLabel}
            </label>
            <textarea
              className="w-full border border-slate-300 rounded-xl text-sm px-3 py-2 min-h-[90px] focus:outline-none focus:ring-2 focus:ring-vlPurple/40"
              placeholder={labels.ideaPlaceholder}
              value={idea}
              onChange={(e) => setIdea(e.target.value)}
            />
            <p className="text-[11px] text-slate-400 mt-1">
              {labels.rightsNote}
            </p>
          </div>

          {/* Barre d’actions */}
          <div className="flex flex-col gap-3 mt-3">
            <div className="flex flex-wrap gap-3 items-center">
              {/* Générer */}
              <button
                type="button"
                onClick={handleGenerate}
                disabled={loading || !idea.trim()}
                className="inline-flex items-center justify-center px-4 py-2.5 rounded-xl bg-vlPurple text-white text-sm font-medium shadow hover:bg-vlPurple/90 disabled:shadow-none"
              >
                {labels.generateBtn}
              </button>

              {/* Générer l'image avec IA */}
              <button
                type="button"
                onClick={handleGenerateImage}
                disabled={loading || (!imagePrompt && !idea.trim())}
                className="text-xs px-3 py-2 rounded-xl border border-slate-300 bg-white hover:bg-slate-50"
              >
                {labels.genImage}
              </button>

              {/* Générer une variante */}
              <button
                type="button"
                onClick={handleGenerate}
                disabled={loading || !generatedText}
                className="text-xs px-3 py-2 rounded-xl border border-slate-300 bg-white hover:bg-slate-50"
              >
                🟢{" "}
                {lang === "fr"
                  ? "Générer une variante"
                  : lang === "ar"
                  ? "توليد نسخة أخرى"
                  : "Generate a variant"}
              </button>

              {/* Modifier mon idée */}
              <button
                type="button"
                onClick={() => {
                  const textarea = document.querySelector("textarea");
                  if (textarea instanceof HTMLTextAreaElement) {
                    textarea.scrollIntoView({ behavior: "smooth", block: "center" });
                    textarea.focus();
                  }
                }}
                className="text-xs px-3 py-2 rounded-xl border border-slate-300 bg-white hover:bg-slate-50"
              >
                ✏️{" "}
                {lang === "fr"
                  ? "Modifier mon idée"
                  : lang === "ar"
                  ? "تعديل الفكرة"
                  : "Edit my idea"}
              </button>
            </div>

            <div className="flex flex-wrap gap-3 items-center text-xs">
              {/* Copier texte */}
              <button
                type="button"
                onClick={handleCopyText}
                disabled={!generatedText}
                className="px-3 py-2 rounded-xl border border-slate-300 bg-white hover:bg-slate-50"
              >
                {labels.copyText}
              </button>

              {/* Copier hashtags */}
              <button
                type="button"
                onClick={handleCopyHashtags}
                disabled={!generatedHashtags}
                className="px-3 py-2 rounded-xl border border-slate-300 bg-white hover:bg-slate-50"
              >
                {labels.copyTags}
              </button>

              {/* Sauvegarder (placeholder) */}
              <button
                type="button"
                onClick={() =>
                  alert(
                    lang === "fr"
                      ? "Plus tard : sauvegarde de contenu dans ton compte."
                      : lang === "ar"
                      ? "لاحقاً: حفظ المحتوى في حسابك."
                      : "Coming soon: save content to your account."
                  )
                }
                className="px-3 py-2 rounded-xl border border-dashed border-slate-300 bg-white hover:bg-slate-50"
              >
                💾{" "}
                {lang === "fr"
                  ? "Sauvegarder ce contenu"
                  : lang === "ar"
                  ? "حفظ هذا المحتوى"
                  : "Save this content"}
              </button>

              {/* Mini tuto publication */}
              <button
                type="button"
                onClick={() =>
                  alert(
                    lang === "fr"
                      ? "Plus tard : mini tuto pour poster sur Instagram / TikTok."
                      : lang === "ar"
                      ? "لاحقاً: شرح مبسط لكيفية النشر على إنستغرام / تيك توك."
                      : "Coming soon: mini tutorial for posting on Instagram / TikTok."
                  )
                }
                className="px-3 py-2 rounded-xl border border-slate-300 bg-white hover:bg-slate-50"
              >
                📲{" "}
                {lang === "fr"
                  ? "Comment le poster ?"
                  : lang === "ar"
                  ? "كيف أنشر هذا المحتوى؟"
                  : "How to post it?"}
              </button>
            </div>
          </div>
        </div>

        <div className="bg-slate-100/80 border border-slate-200 rounded-2xl p-4 sm:p-5">
          <ContentPreview
            loading={loading}
            text={generatedText}
            hashtags={generatedHashtags}
            imagePrompt={imagePrompt}
            imageUrl={imageUrl}
          />
        </div>
      </div>
    </Layout>
  );
}
