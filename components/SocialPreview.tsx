
import { useLanguage } from "../context/LanguageContext";

type Props = {
  text?: string;
  hashtags?: string[];
};

const SocialPreview: React.FC<Props> = ({ text, hashtags }) => {
  const { lang } = useLanguage();

  if (!text) return null;

  const firstLine = text.split(/\n/)[0].slice(0, 80);
  const tagsLine =
    hashtags && hashtags.length
      ? hashtags
          .slice(0, 4)
          .map((h) => `#${h}`)
          .join("  ")
      : "#viralobby  #ai  #contentcreator";

  const platforms = [
    {
      id: "insta-reel",
      ratio: "9:16",
      labelFr: "Reel Instagram",
      labelEn: "Instagram Reel",
      labelAr: "ريل إنستغرام"
    },
    {
      id: "insta-post",
      ratio: "1:1",
      labelFr: "Post carré",
      labelEn: "Square post",
      labelAr: "منشور مربّع"
    },
    {
      id: "tiktok",
      ratio: "9:16",
      labelFr: "TikTok",
      labelEn: "TikTok",
      labelAr: "تيك توك"
    },
    {
      id: "short",
      ratio: "9:16",
      labelFr: "YouTube Short",
      labelEn: "YouTube Short",
      labelAr: "يوتيوب شورت"
    }
  ];

  const getLabel = (p: (typeof platforms)[number]) =>
    lang === "fr" ? p.labelFr : lang === "ar" ? p.labelAr : p.labelEn;

  const getPadding = (ratio: string) => {
    if (ratio === "1:1") return "100%";
    if (ratio === "9:16") return "177%";
    if (ratio === "16:9") return "56.25%";
    return "150%";
  };

  const titleLabel =
    lang === "fr"
      ? "Aperçu par plateforme"
      : lang === "ar"
      ? "معاينة لكل منصة"
      : "Preview by platform";

  const subtitle =
    lang === "fr"
      ? "Zones sûres approximatives pour le titre et les tags. Vérifie toujours dans l’app officielle avant de publier."
      : lang === "ar"
      ? "مناطق آمنة تقريبية لعرض العنوان والوسوم. يُفضّل التأكد دائماً من المعاينة داخل التطبيق قبل النشر."
      : "Approximate safe zones for title and tags. Always double-check in the official app before posting.";

  return (
    <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm space-y-3">
      <div>
        <h3 className="text-sm font-semibold text-slate-800">{titleLabel}</h3>
        <p className="text-[11px] text-slate-500 mt-1">{subtitle}</p>
      </div>
      <div className="grid sm:grid-cols-2 gap-3">
        {platforms.map((p) => (
          <div key={p.id} className="space-y-1">
            <div className="text-[11px] text-slate-600 font-medium">
              {getLabel(p)} · {p.ratio}
            </div>
            <div className="relative w-full rounded-xl bg-slate-900 text-white overflow-hidden">
              <div style={{ paddingTop: getPadding(p.ratio) }} />
              <div className="absolute inset-0 p-2 flex flex-col justify-between text-[10px]">
                <div className="bg-black/50 rounded-lg px-2 py-1">
                  <div className="font-semibold truncate">{firstLine}</div>
                </div>
                <div className="bg-black/40 rounded-lg px-2 py-1 mt-1">
                  <div className="truncate">{tagsLine}</div>
                </div>
              </div>
              <div className="absolute inset-2 border border-dashed border-white/40 rounded-lg pointer-events-none" />
              <div className="absolute inset-x-0 bottom-0 h-4 bg-gradient-to-t from-black/40 to-transparent pointer-events-none" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SocialPreview;
