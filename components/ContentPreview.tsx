
type Props = {
  loading: boolean;
  text?: string;
  hashtags?: string[];
  imagePrompt?: string;
};

import { useLanguage } from "../context/LanguageContext";

const ContentPreview: React.FC<Props> = ({ loading, text, hashtags, imagePrompt }) => {
  const { lang } = useLanguage();

  if (loading) {
    return (
      <div className="h-full flex flex-col items-center justify-center text-sm text-slate-500">
        <div className="w-10 h-10 border-4 border-vlPurple/40 border-t-vlPurple rounded-full animate-spin mb-3" />
        <p>{lang === "fr" ? "L’IA travaille pour toi…" : "AI is working for you..."}</p>
      </div>
    );
  }

  if (!text) {
    return (
      <div className="h-full flex flex-col items-center justify-center text-sm text-slate-400 text-center px-4">
        <p>
          {lang === "fr"
            ? "Ton contenu apparaîtra ici après la génération. Décris ton idée à gauche et clique sur “Générer”."
            : "Your content will appear here after generation. Describe your idea on the left and click “Generate”."}
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4 h-full flex flex-col">
      <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm flex-1">
        <h3 className="text-sm font-semibold text-slate-800 mb-1">
          {lang === "fr" ? "Texte du post" : "Post text"}
        </h3>
        <p className="text-sm whitespace-pre-wrap text-slate-800">{text}</p>
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm">
          <h3 className="text-sm font-semibold text-slate-800 mb-1">
            {lang === "fr" ? "Idée de visuel" : "Visual idea"}
          </h3>
          <p className="text-xs text-slate-700">
            {imagePrompt ||
              (lang === "fr"
                ? "Une image sera proposée en fonction du texte (créateur de contenu, smartphone, ambiance moderne, réseaux sociaux)."
                : "An image will be suggested based on the text (content creator, smartphone, modern vibes, social media).")}
          </p>
        </div>
        <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm">
          <h3 className="text-sm font-semibold text-slate-800 mb-1">
            Hashtags
          </h3>
          <p className="text-xs text-slate-700">
            {hashtags && hashtags.length
              ? hashtags.map((h) => `#${h}`).join("  ")
              : "#viralloby  #ai  #contentcreator  #morocco"}
          </p>
        </div>
      </div>
    </div>
  );
};

export default ContentPreview;
