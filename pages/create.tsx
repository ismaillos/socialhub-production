
import React, { useState, useEffect } from "react";
import { useRouter } from "next/router";
import StepIndicator from "../components/StepIndicator";
import ContentPreview from "../components/ContentPreview";
type ContentType = "video" | "post" | "carousel";
type GenLanguage = "FR" | "EN" | "AR";
export default function CreatePage(){
  const router = useRouter();
  const [contentType, setContentType] = useState<ContentType>("video");
  const [genLang, setGenLang] = useState<GenLanguage>("FR");
  const [theme, setTheme] = useState("marketing");
  const [tone, setTone] = useState("inspirant");
  const [idea, setIdea] = useState("");
  const [loading, setLoading] = useState(false);
  const [title, setTitle] = useState<string | undefined>();
  const [generatedText, setGeneratedText] = useState<string | undefined>();
  const [generatedHashtags, setGeneratedHashtags] = useState<string[] | undefined>();
  const [imagePrompt, setImagePrompt] = useState<string | undefined>();
  const [imageUrl, setImageUrl] = useState<string | undefined>();
  const [videoPrompt, setVideoPrompt] = useState<string | undefined>();
  useEffect(()=>{
    if(!router.isReady) return;
    const q = router.query;
    if(typeof q.idea==="string") setIdea(q.idea);
    if(typeof q.theme==="string") setTheme(q.theme);
    if(typeof q.tone==="string") setTone(q.tone);
  }, [router.isReady, router.query]);
  const handleGenerate = async () => {
    if(!idea.trim()) return;
    setLoading(true);
    setTitle(undefined); setGeneratedText(undefined); setGeneratedHashtags(undefined);
    setImagePrompt(undefined); setImageUrl(undefined); setVideoPrompt(undefined);
    try{
      const res = await fetch("/api/generate",{ method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({ contentType, language: genLang, theme, tone, idea }) });
      if(!res.ok) throw new Error("API error");
      const data = await res.json();
      const first = (data.text||"").split(/\n/)[0] || "Your viral hook";
      setTitle(first); setGeneratedText(data.text); setGeneratedHashtags(data.hashtags); setImagePrompt(data.imagePrompt);
    }catch(e){ console.error(e); alert("Error while generating content."); }
    finally{ setLoading(false); }
  };
  const handleGenerateImage = async () => {
    const base = imagePrompt || idea; if(!base) return;
    setLoading(true);
    try{
      const prompt = `Ultra clean social media visual, mobile-first composition, space for big title at top and hashtags at bottom, no text rendered, high contrast, ${base}`;
      const res = await fetch("/api/generate-image",{ method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({ prompt }) });
      const data = await res.json();
      if(!res.ok){ alert(`Image API error:\n${data?.error || "unknown"}${data?.details? "\nDetails: "+data.details : ""}`); return; }
      setImageUrl(data.imageUrl);
    }catch(e){ console.error(e); alert("Could not generate image."); }
    finally{ setLoading(false); }
  };
  const handleBuildVideoPrompt = async () => {
    const base = generatedText || idea; if(!base) return alert("Generate the text first or enter an idea.");
    setLoading(true);
    try{
      const res = await fetch("/api/generate-video-prompt", { method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({ script: base, theme, tone }) });
      const data = await res.json();
      if(!res.ok){ alert(`Prompt build error:\n${data?.error || "unknown"}${data?.details? "\nDetails: "+data.details : ""}`); return; }
      setVideoPrompt(data.prompt);
    }catch(e){ console.error(e); alert("Could not build video prompt."); }
    finally{ setLoading(false); }
  };
  return (
    <div>
      <StepIndicator current={2} />
      <div className="grid lg:grid-cols-[minmax(0,1.1fr)_minmax(0,1fr)] gap-6">
        <div className="vl-card p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h1 className="text-lg font-semibold text-slate-900">Describe your idea</h1>
            <div className="text-[11px] text-slate-500">You keep 100% of rights.</div>
          </div>
          <div>
            <div className="hdr">Content type</div>
            <div className="inline-flex flex-wrap gap-2 mt-1">
              <button onClick={()=>setContentType("video")} className={`vl-btn ${contentType==="video"?"vl-btn-primary":"vl-btn-ghost"}`}>🎬 Video (Reel/TikTok)</button>
              <button onClick={()=>setContentType("post")} className={`vl-btn ${contentType==="post"?"vl-btn-primary":"vl-btn-ghost"}`}>🖼️ Post image + text</button>
              <button onClick={()=>setContentType("carousel")} className={`vl-btn ${contentType==="carousel"?"vl-btn-primary":"vl-btn-ghost"}`}>📜 Carousel</button>
            </div>
          </div>
          <div>
            <div className="hdr">Language</div>
            <div className="inline-flex gap-2 mt-1">
              {(["FR","EN","AR"] as GenLanguage[]).map(l=>(
                <button key={l} onClick={()=>setGenLang(l)} className={`vl-btn ${genLang===l?"vl-btn-ghost border-vl_primary text-vl_primary":"vl-btn-ghost"}`}>{l}</button>
              ))}
            </div>
          </div>
          <div>
            <div className="hdr">Theme</div>
            <div className="flex flex-wrap gap-2 mt-1">
              {["marketing","business","education","social","autre"].map(v=>(
                <button key={v} onClick={()=>setTheme(v)} className={`vl-btn ${theme===v?"vl-btn-ghost border-vl_accent text-vl_accent":"vl-btn-ghost"}`}>{v}</button>
              ))}
            </div>
          </div>
          <div>
            <div className="hdr">Tone</div>
            <div className="flex flex-wrap gap-2 mt-1">
              {[["inspirant","Inspirational"],["serieux","Serious"],["fun","Fun"]].map(([v,l])=>(
                <button key={v} onClick={()=>setTone(v)} className={`vl-btn ${tone===v?"vl-btn-ghost border-slate-900 text-slate-900":"vl-btn-ghost"}`}>{l}</button>
              ))}
            </div>
          </div>
          <div>
            <div className="hdr">Your idea in one sentence</div>
            <textarea value={idea} onChange={e=>setIdea(e.target.value)} placeholder="Ex: A short video that explains how to use AI to start a small local business." className="input" />
          </div>
          <div className="flex flex-wrap gap-3 items-center">
            <button onClick={handleGenerate} disabled={loading||!idea.trim()} className="vl-btn vl-btn-primary">{loading? "Generating..." : "🚀 Generate my content"}</button>
            <button onClick={handleGenerateImage} disabled={loading||(!imagePrompt && !idea.trim())} className="vl-btn vl-btn-ghost">🎨 Generate image (AI)</button>
            <button onClick={handleBuildVideoPrompt} disabled={loading||(!generatedText && !idea.trim())} className="vl-btn vl-btn-ghost">🎬 Build video prompt (Veo)</button>
          </div>
        </div>
        <div className="p-1">
          <ContentPreview loading={loading} title={title} text={generatedText} hashtags={generatedHashtags} imagePrompt={imagePrompt} imageUrl={imageUrl} videoPrompt={videoPrompt} contentType={contentType} />
        </div>
      </div>
    </div>
  );
}
