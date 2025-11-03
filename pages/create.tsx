
import React, { useState } from "react";
import Layout from "../components/Layout";
import StepIndicator from "../components/StepIndicator";
import ContentPreview from "../components/ContentPreview";
import { useLanguage } from "../context/LanguageContext";

type ContentType = "video" | "post";
type GenLanguage = "FR" | "EN";

export default function CreatePage() {
  const { lang } = useLanguage();
  const [contentType, setContentType] = useState<ContentType>("video");
  const [genLang, setGenLang] = useState<GenLanguage>("FR");
  const [theme, setTheme] = useState("emploi");
  const [tone, setTone] = useState("inspirant");
  const [idea, setIdea] = useState("");
  const [loading, setLoading] = useState(false);
  const [generatedText, setGeneratedText] = useState<string | undefined>();
  const [generatedHashtags, setGeneratedHashtags] = useState<string[] | undefined>();
  const [imagePrompt, setImagePrompt] = useState<string | undefined>();

  const labels = {
    title: lang === "fr" ? "Décris ton idée" : "Describe your idea",
    subtitle:
      lang === "fr"
        ? "Plus tu es précis, meilleur sera le contenu généré."
        : "The more precise you are, the better the result.",
    typeLabel: lang === "fr" ? "Type de contenu" : "Content type",
    langLabel: lang === "fr" ? "Langue du contenu" : "Content language",
    themeLabel: lang === "fr" ? "Thème" : "Theme",
    toneLabel: lang === "fr" ? "Ton du contenu" : "Tone",
    ideaLabel:
      lang === "fr" ? "Décris ton idée en une phrase" : "Describe your idea in one sentence",
    ideaPlaceholder:
      lang === "fr"
        ? "Ex : Je veux une vidéo qui motive les jeunes marocains à apprendre le digital pour trouver un job."
        : "Ex: I want a video that motivates young Moroccans to learn digital skills to find a job.",
    rightsNote:
      lang === "fr"
        ? "Tu gardes 100% de tes droits sur le contenu généré."
        : "You keep 100% of the rights on the generated content.",
    generateBtn: loading
      ? lang === "fr"
        ? "Génération en cours..."
        : "Generating..."
      : lang === "fr"
      ? "🚀 Générer mon contenu"
      : "🚀 Generate my content",
    copyText: lang === "fr" ? "📋 Copier le texte" : "📋 Copy text",
    copyTags: lang === "fr" ? "# Copier les hashtags" : "# Copy hashtags"
  };

  const handleGenerate = async () => {
    if (!idea.trim()) return;
    setLoading(true);
    setGeneratedText(undefined);
    setGeneratedHashtags(undefined);
    setImagePrompt(undefined);

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
          : "An error occurred. Please try again."
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
                🎬 {lang === "fr" ? "Vidéo courte" : "Short video"}
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
                🖼️ {lang === "fr" ? "Post image + texte" : "Image + text post"}
              </button>
            </div>
          </div>

          {/* Langue du contenu */}
          <div>
            <label className="block text-xs font-medium text-slate-700 mb-1">
              {labels.langLabel}
            </label>
            <div className="inline-flex gap-2 text-xs">
              {(["FR", "EN"] as GenLanguage[]).map((l) => (
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
                  {l === "FR" ? "Français" : "English"}
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
                ["emploi", lang === "fr" ? "Emploi / Travail" : "Jobs / Work"],
                ["business", "Business / Freelance"],
                ["motivation", lang === "fr" ? "Motivation" : "Motivation"],
                ["education", lang === "fr" ? "Éducation" : "Education"],
                ["social", lang === "fr" ? "Social / Impact" : "Social / Impact"],
                ["autre", lang === "fr" ? "Autre" : "Other"]
              ].map(([value, label]) => (
                <button
                  type="button"
                  key={value}
                  onClick={() => setTheme(value)}
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
                ["inspirant", lang === "fr" ? "Inspirant & motivant" : "Inspiring & motivational"],
                ["serieux", lang === "fr" ? "Sérieux & pro" : "Serious & professional"],
                ["fun", lang === "fr" ? "Fun & léger" : "Fun & light"]
              ].map(([value, label]) => (
                <button
                  type="button"
                  key={value}
                  onClick={() => setTone(value)}
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

          <div className="flex flex-wrap gap-3 items-center">
            <button
              type="button"
              onClick={handleGenerate}
              disabled={loading || !idea.trim()}
              className="inline-flex items-center justify-center px-4 py-2.5 rounded-xl bg-vlPurple text-white text-sm font-medium shadow hover:bg-vlPurple/90 disabled:shadow-none"
            >
              {labels.generateBtn}
            </button>
            {generatedText && (
              <>
                <button
                  type="button"
                  onClick={handleCopyText}
                  className="text-xs px-3 py-2 rounded-xl border border-slate-300 bg-white hover:bg-slate-50"
                >
                  {labels.copyText}
                </button>
                <button
                  type="button"
                  onClick={handleCopyHashtags}
                  className="text-xs px-3 py-2 rounded-xl border border-slate-300 bg-white hover:bg-slate-50"
                >
                  {labels.copyTags}
                </button>
              </>
            )}
          </div>
        </div>

        <div className="bg-slate-100/80 border border-slate-200 rounded-2xl p-4 sm:p-5">
          <ContentPreview
            loading={loading}
            text={generatedText}
            hashtags={generatedHashtags}
            imagePrompt={imagePrompt}
          />
        </div>
      </div>
    </Layout>
  );
}
