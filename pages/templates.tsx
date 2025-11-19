
import Link from "next/link";
const templates=[
  { id:"biz-ai", theme:"business", tone:"inspirant", idea:"A short video script showing how to launch a small profitable business using AI." },
  { id:"edu-carousel", theme:"education", tone:"serieux", idea:"An Instagram carousel in 5 slides to help students learn better with AI." },
  { id:"promo", theme:"marketing", tone:"fun", idea:"A short punchy caption to announce -50% limited offer with clear CTA." }
];
export default function TemplatesPage(){
  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold text-slate-900">Viral content templates</h1>
      <div className="grid md:grid-cols-3 gap-4">
        {templates.map(tpl => (
          <div key={tpl.id} className="vl-card p-4 flex flex-col justify-between">
            <div>
              <div className="text-sm font-semibold text-slate-800 mb-2">Template · {tpl.theme}</div>
              <p className="text-xs text-slate-600 line-clamp-5">{tpl.idea}</p>
              <p className="text-[11px] text-slate-400 mt-2">Tone: {tpl.tone}</p>
            </div>
            <div className="mt-4">
              <Link href={{ pathname:"/create", query:{ theme: tpl.theme, tone: tpl.tone, idea: tpl.idea } }} className="vl-btn vl-btn-primary w-full">Use this template</Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
