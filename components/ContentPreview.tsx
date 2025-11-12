
import SocialPreview from "./SocialPreview";
type ContentType = "video" | "post" | "carousel";
export default function ContentPreview({ loading, title, text, hashtags, imagePrompt, imageUrl, videoPrompt, contentType }:{
  loading:boolean; title?:string; text?:string; hashtags?:string[]; imagePrompt?:string; imageUrl?:string; videoPrompt?:string; contentType:ContentType;
}){
  if(loading){ return <div className="h-full flex flex-col items-center justify-center text-sm text-slate-500"><div className="w-10 h-10 border-4 border-vl_primary/40 border-t-vl_primary rounded-full animate-spin mb-3" /><p>AI is working…</p></div>; }
  if(!text && !title){ return <div className="h-full flex items-center justify-center text-sm text-slate-400">Your content will appear here.</div>; }
  return (
    <div className="space-y-4">
      <div className="vl-card p-4 space-y-2">
        <div className="hdr">Title & Post</div>
        {!!title && <h3 className="text-lg font-extrabold text-slate-900">{title}</h3>}
        {!!text && <p className="text-sm whitespace-pre-wrap text-slate-800">{text}</p>}
      </div>
      <div className="grid md:grid-cols-2 gap-4">
        <div className="vl-card p-4">
          <div className="hdr">Hashtags</div>
          <p className="text-sm font-semibold text-slate-800">{hashtags?.length? hashtags.map(h=>`#${h}`).join("  ") : "#viralobby  #ai  #contentcreator  #digitalmarketing"}</p>
        </div>
        <div className="vl-card p-4">
          <div className="hdr">Image</div>
          {imageUrl? (<><img src={imageUrl} alt="Generated" className="w-full rounded-xl border border-slate-200 mb-3" /><a href={imageUrl} download className="vl-btn vl-btn-ghost text-xs">⬇️ Download</a></>)
          : (<><p className="text-xs text-slate-700 mb-2">{imagePrompt || "A visual idea is suggested based on the text."}</p><p className="block-sub">Click “Generate image”.</p></>)}
        </div>
      </div>
      <SocialPreview title={title} text={text} hashtags={hashtags} contentType={contentType} />
      {!!videoPrompt && (<div className="vl-card p-4"><div className="hdr">Video prompt (Google Veo 2 / 3)</div><textarea readOnly className="input text-xs" rows={6} value={videoPrompt} /><div className="mt-2 flex gap-2"><button onClick={()=>navigator.clipboard.writeText(videoPrompt!)} className="vl-btn vl-btn-ghost text-xs">📋 Copy prompt</button><a className="vl-btn vl-btn-primary text-xs" href="https://aistudio.google.com/" target="_blank" rel="noreferrer">↗ Open Google AI Studio</a></div></div>)}
    </div>
  );
}
