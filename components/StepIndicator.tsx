
type Props = {
  current: 1 | 2 | 3;
};

const stepsBase = [
  {
    id: 1,
    fr: "1. Décris ton idée",
    en: "1. Describe your idea",
    ar: "١. صف فكرتك"
  },
  {
    id: 2,
    fr: "2. Génération IA",
    en: "2. AI generation",
    ar: "٢. توليد المحتوى بالذكاء الاصطناعي"
  },
  {
    id: 3,
    fr: "3. Télécharge & publie",
    en: "3. Download & publish",
    ar: "٣. حمِّل وانشر"
  }
];

import { useLanguage } from "../context/LanguageContext";

const StepIndicator: React.FC<Props> = ({ current }) => {
  const { lang } = useLanguage();

  return (
    <div className="flex flex-wrap items-center gap-3 text-xs sm:text-sm mb-6">
      {stepsBase.map((step) => {
        const active = step.id === current;
        const done = step.id < current;
        const label = lang === "fr" ? step.fr : lang === "ar" ? step.ar : step.en;
        return (
          <div className="flex items-center gap-2" key={step.id}>
            <div
              className={[
                "w-6 h-6 rounded-full flex items-center justify-center border text-xs font-semibold",
                done
                  ? "bg-vlPurple text-white border-vlPurple"
                  : active
                  ? "bg-vlPink text-white border-vlPink"
                  : "bg-white text-slate-400 border-slate-300"
              ].join(" ")}
            >
              {step.id}
            </div>
            <span
              className={
                active || done ? "text-slate-900 font-medium" : "text-slate-400"
              }
            >
              {label}
            </span>
            {step.id !== 3 && (
              <div className="w-6 h-px bg-slate-300 mx-1 hidden sm:block" />
            )}
          </div>
        );
      })}
    </div>
  );
};

export default StepIndicator;
