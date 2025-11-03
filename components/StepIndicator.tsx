
type Props = {
  current: 1 | 2 | 3;
};

const steps = [
  { id: 1, labelFr: "1. Décris ton idée", labelEn: "1. Describe your idea" },
  { id: 2, labelFr: "2. Génération IA", labelEn: "2. AI generation" },
  { id: 3, labelFr: "3. Télécharge & publie", labelEn: "3. Download & publish" }
];

import { useLanguage } from "../context/LanguageContext";

const StepIndicator: React.FC<Props> = ({ current }) => {
  const { lang } = useLanguage();

  return (
    <div className="flex flex-wrap items-center gap-3 text-xs sm:text-sm mb-6">
      {steps.map((step) => {
        const active = step.id === current;
        const done = step.id < current;
        const label = lang === "fr" ? step.labelFr : step.labelEn;
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
