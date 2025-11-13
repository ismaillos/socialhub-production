
import React, { useState, useEffect } from "react";
import { useRouter } from "next/router";
import Layout from "../components/Layout";
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
  const [generatedText, setGeneratedText] = useState<string | undefined>();
  const [generatedHashtags, setGeneratedHashtags] = useState<string[] | undefined>();
  const [imagePrompt, setImagePrompt] = useState<string | undefined>();
  const [imageUrl, setImageUrl] = useState<string | undefined>();
  const [videoUrl, setVideoUrl] = useState<string | undefined>();

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
    setGeneratedText(undefined);
    setGeneratedHashtags(undefined);
    setImagePrompt(undefined);
    setImageUrl(undefined);
    setVideoUrl(undefined);
    try{
      const res = await fetch("/api/generate",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({ contentType, language: genLang, theme, tone, idea })
      });
      if(!res.ok) throw new Error("API error");
      const data = await res.json();
      setGeneratedText(data.text);
      setGeneratedHashtags(data.hashtags);
      setImagePrompt(data.imagePrompt);
    }catch(e){ console.error(e); alert("Error while generating content."); }
    finally{ setLoading(false); }
  };

  const handleGenerateImage = async () => {
    const base = imagePrompt || idea;
    if(!base) return;
    setLoading(true);
    try{
      const prompt = `Ultra clean social media visual, mobile-first composition, space for big title at top and hashtags at bottom, no text rendered, high contrast, ${base}`;
      const res = await fetch("/api/generate-image",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({ prompt })
      });
      const data = await res.json();
      if(!res.ok){ alert("Image API error: "+(data.error||"unknown")); return; }
      setImageUrl(data.imageUrl);
    }catch(e){ console.error(e); alert("Could not generate image."); }
    finally{ setLoading(false); }
  };

  return (
    <Layout>
      <StepIndicator current={2} />

      <div className="grid lg:grid-cols-[minmax(0,1.1fr)_minmax(0,1fr)] gap-6">
        <div className="vl-card p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h1 className="text-lg font-semibold text-slate-900">Describe your idea</h1>
            <div className="text-[11px] text-slate-500">You keep 100% of rights.</div>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-700 mb-1">Content type</label>
            <div className="inline-flex flex-wrap gap-2">
              <button onClick={()=>setContentType("video")} className={`vl-btn ${contentType==="video"?"vl-btn-primary":"vl-btn-ghost"}`}>🎬 Video (Reel/TikTok)</button>
              <button onClick={()=>setContentType("post")} className={`vl-btn ${contentType==="post"?"vl-btn-primary":"vl-btn-ghost"}`}>🖼️ Post image + text</button>
              <button onClick={()=>setContentType("carousel")} className={`vl-btn ${contentType==="carousel"?"vl-btn-primary":"vl-btn-ghost"}`}>📜 Carousel</button>
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-700 mb-1">Language</label>
            <div className="inline-flex gap-2">
              {(["FR","EN","AR"] as GenLanguage[]).map(l=>(
                <button key={l} onClick={()=>setGenLang(l)} className={`vl-btn ${genLang===l?"vl-btn-ghost border-vl_primary text-vl_primary":"vl-btn-ghost"}`}>{l}</button>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-700 mb-1">Theme</label>
            <div className="flex flex-wrap gap-2">
              {["marketing","business","education","social","autre"].map(v=>(
                <button key={v} onClick={()=>setTheme(v)} className={`vl-btn ${theme===v?"vl-btn-ghost border-vl_accent text-vl_accent":"vl-btn-ghost"}`}>{v}</button>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-700 mb-1">Tone</label>
            <div className="flex flex-wrap gap-2">
              {[["inspirant","Inspirational"],["serieux","Serious"],["fun","Fun"]].map(([v,l])=>(
                <button key={v} onClick={()=>setTone(v)} className={`vl-btn ${tone===v?"vl-btn-ghost border-slate-900 text-slate-900":"vl-btn-ghost"}`}>{l}</button>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-700 mb-1">Your idea in one sentence</label>
            <textarea value={idea} onChange={e=>setIdea(e.target.value)} placeholder="Ex: A short video that explains how to use AI to start a small local business." className="w-full border border-slate-300 rounded-2xl text-sm px-3 py-3 min-h-[100px] focus:outline-none focus:ring-2 focus:ring-vl_primary/30" />
          </div>

          <div className="flex flex-wrap gap-3 items-center">
            <button onClick={handleGenerate} disabled={loading||!idea.trim()} className="vl-btn vl-btn-primary">
              {loading? "Generating..." : "🚀 Generate my content"}
            </button>
            <button onClick={handleGenerateImage} disabled={loading||(!imagePrompt && !idea.trim())} className="vl-btn vl-btn-ghost">🎨 Generate image (AI)</button>
          </div>
        </div>

        <div className="p-1">
          <ContentPreview
            loading={loading}
            text={generatedText}
            hashtags={generatedHashtags}
            imagePrompt={imagePrompt}
            imageUrl={imageUrl}
            videoUrl={videoUrl}
            contentType={contentType}
          />
        </div>
      </div>
    </Layout>
  );
}
