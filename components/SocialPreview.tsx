
type ContentType = "video" | "post" | "carousel";
export default function SocialPreview({ title, text, hashtags, contentType }:{ title?:string; text?:string; hashtags?:string[]; contentType:ContentType; }){
  if(!text && !title) return null;
  const firstLine = (title||text||"").split(/\n/)[0].slice(0,80);
  const tagsLine = (hashtags?.length? hashtags.slice(0,4).map(h=>`#${h}`).join("  "): "#viralobby  #ai  #contentcreator");
  let platforms = contentType==="video"
    ? [{id:"reel",ratio:"9:16",label:"Instagram Reel"},{id:"tiktok",ratio:"9:16",label:"TikTok"},{id:"shorts",ratio:"9:16",label:"YouTube Shorts"}]
    : contentType==="post"
    ? [{id:"insta",ratio:"4:5",label:"Instagram (4:5)"},{id:"linkedin",ratio:"1.91:1",label:"LinkedIn"},{id:"facebook",ratio:"1.91:1",label:"Facebook"}]
    : [{id:"insta-carousel",ratio:"4:5",label:"Instagram Carousel"},{id:"linkedin-doc",ratio:"1.41:1",label:"LinkedIn Document"},{id:"fb-album",ratio:"1:1",label:"Facebook Album"}];
  const getPadding=(r:string)=> r==="1:1"?"100%": r==="4:5"?"125%": r==="9:16"?"177%": r==="1.91:1"?"52%": r==="1.41:1"?"70%":"56.25%";
  return (
    <div className="vl-card p-4 space-y-3">
      <h3 className="hdr">Platform previews</h3>
      <div className="grid sm:grid-cols-2 gap-3">
        {platforms.map(p=>(
          <div key={p.id} className="space-y-1">
            <div className="text-[11px] text-slate-600 font-medium">{p.label} · {p.ratio}</div>
            <div className="relative w-full rounded-2xl bg-slate-900 text-white overflow-hidden">
              <div style={{paddingTop:getPadding(p.ratio)}} />
              <div className="absolute inset-0 p-2 flex flex-col justify-between text-[10px]">
                <div className="bg-black/60 rounded-lg px-2 py-1"><div className="font-bold truncate">{firstLine}</div></div>
                <div className="bg-black/40 rounded-lg px-2 py-1 mt-1"><div className="truncate">{tagsLine}</div></div>
              </div>
              <div className="absolute inset-2 border border-dashed border-white/35 rounded-xl pointer-events-none" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
