
import { useState } from "react";
import Sidebar from "@/components/Sidebar";

const contentTypes = [
  { id: "reel", label: "Reel / TikTok / Short", icon: "🎬" },
  { id: "image", label: "Image Post", icon: "🖼️" },
  { id: "carousel", label: "Carousel", icon: "📜" }
];

const platforms = [
  { id: "instagram", label: "Instagram", chip: "Reel / Post" },
  { id: "tiktok", label: "TikTok", chip: "Short vertical" },
  { id: "youtube", label: "YouTube Shorts", chip: "Vertical" },
  { id: "linkedin", label: "LinkedIn", chip: "Feed / Carousel" }
];

export default function CreatePage() {
  const [contentType, setContentType] = useState("reel");
  const [platformId, setPlatformId] = useState("instagram");
  const [topic, setTopic] = useState("");
  const [audience, setAudience] = useState("");
  const [tone, setTone] = useState("Friendly");
  const [language, setLanguage] = useState("English");
  const [keywords, setKeywords] = useState("");

  const [loading, setLoading] = useState(false);
  const [generatedTitle, setGeneratedTitle] = useState("");
  const [generatedBody, setGeneratedBody] = useState("");
  const [generatedHashtags, setGeneratedHashtags] = useState([]);
  const [imagePrompt, setImagePrompt] = useState("");
  const [imageUrl, setImageUrl] = useState("");
  const [videoPrompt, setVideoPrompt] = useState("");

  const handleGenerate = async () => {
    if (!topic.trim()) return;
    setLoading(true);
    setGeneratedTitle("");
    setGeneratedBody("");
    setGeneratedHashtags([]);
    setImagePrompt("");
    setVideoPrompt("");
    try {
      const res = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          contentType,
          platformId,
          topic,
          audience,
          tone,
          language,
          keywords
        })
      });
      const data = await res.json();
      if (!res.ok) {
        alert(data.error || "Error generating content");
        return;
      }
      setGeneratedTitle(data.title || "");
      setGeneratedBody(data.body || "");
      setGeneratedHashtags(data.hashtags || []);
      setImagePrompt(data.imagePrompt || "");
      setVideoPrompt(data.videoPrompt || "");
    } catch (e) {
      console.error(e);
      alert("Network error while generating content");
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateImage = async () => {
    const base = imagePrompt || topic;
    if (!base) return;
    setLoading(true);
    try {
      const res = await fetch("/api/generate-image", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          prompt: `Ultra clean social media visual, no text on image, high-contrast, optimized for ${platformId} in style: ${base}`
        })
      });
      const data = await res.json();
      if (!res.ok) {
        alert(data.error || "Error generating image");
        return;
      }
      setImageUrl(data.imageUrl);
    } catch (e) {
      console.error(e);
      alert("Network error while generating image");
    } finally {
      setLoading(false);
    }
  };

  const handleCopyAll = () => {
    const text = `${generatedTitle}\n\n${generatedBody}\n\n${generatedHashtags.map(h => "#" + h).join(" ")}`;
    navigator.clipboard.writeText(text);
  };

  const handleCopyVeo = () => {
    if (!videoPrompt) return;
    navigator.clipboard.writeText(videoPrompt);
  };

  return (
    <div className="app-shell">
      <Sidebar />
      <div className="flex-1 flex flex-col bg-slate-950">
        <header className="topbar">
          <div>
            <h1 className="text-sm font-semibold text-slate-50">Create Viral Content</h1>
            <p className="text-xs text-slate-500 mt-0.5">
              One brief → post text, visual idea, Veo2/3 video prompt & hashtags.
            </p>
          </div>
          <div className="flex items-center gap-3 text-xs text-slate-400">
            <span>contact@viralobby.com</span>
          </div>
        </header>

        <main className="page-body p-6 grid grid-cols-1 xl:grid-cols-2 gap-6">
          {/* LEFT: INPUTS */}
          <section className="card-dark p-5 flex flex-col gap-5">
            {/* Row: type + platform */}
            <div className="grid sm:grid-cols-2 gap-3">
              <div>
                <h2 className="text-[11px] font-semibold text-slate-400 uppercase tracking-wide mb-2">
                  Content type
                </h2>
                <div className="flex flex-wrap gap-1.5">
                  {contentTypes.map((t) => (
                    <button
                      key={t.id}
                      onClick={() => setContentType(t.id)}
                      className={`chip ${contentType === t.id ? "border-vl_primary bg-slate-900 text-slate-50" : ""}`}
                    >
                      <span className="mr-1">{t.icon}</span>
                      {t.label}
                    </button>
                  ))}
                </div>
              </div>
              <div>
                <h2 className="text-[11px] font-semibold text-slate-400 uppercase tracking-wide mb-2">
                  Platform
                </h2>
                <div className="flex flex-wrap gap-1.5">
                  {platforms.map((p) => (
                    <button
                      key={p.id}
                      onClick={() => setPlatformId(p.id)}
                      className={`chip ${platformId === p.id ? "border-vl_accent bg-slate-900 text-slate-50" : ""}`}
                    >
                      {p.label}
                      <span className="ml-1 text-[10px] text-slate-400">· {p.chip}</span>
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Topic */}
            <div className="space-y-1.5">
              <label className="text-[11px] text-slate-400 uppercase tracking-wide">
                Idea / hook
              </label>
              <textarea
                className="textarea"
                placeholder="e.g., A reel showing how Amaly Kids Club helps Moroccan students learn global goals in a fun way."
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
              />
            </div>

            {/* Audience + tone + language */}
            <div className="grid sm:grid-cols-3 gap-3">
              <div className="space-y-1.5">
                <label className="text-[11px] text-slate-400 uppercase tracking-wide">
                  Audience
                </label>
                <input
                  className="input"
                  placeholder="e.g., Parents, teachers, young creators…"
                  value={audience}
                  onChange={(e) => setAudience(e.target.value)}
                />
              </div>
              <div className="space-y-1.5">
                <label className="text-[11px] text-slate-400 uppercase tracking-wide">
                  Tone
                </label>
                <select
                  className="input"
                  value={tone}
                  onChange={(e) => setTone(e.target.value)}
                >
                  <option>Friendly</option>
                  <option>Professional</option>
                  <option>Bold</option>
                  <option>Educational</option>
                  <option>Playful</option>
                </select>
              </div>
              <div className="space-y-1.5">
                <label className="text-[11px] text-slate-400 uppercase tracking-wide">
                  Language
                </label>
                <select
                  className="input"
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                >
                  <option>English</option>
                  <option>French</option>
                  <option>Arabic</option>
                  <option>Bilingual (FR + AR)</option>
                </select>
              </div>
            </div>

            {/* Keywords */}
            <div className="space-y-1.5">
              <label className="text-[11px] text-slate-400 uppercase tracking-wide">
                Keywords (optional)
              </label>
              <input
                className="input"
                placeholder="e.g., SDG4, education, Amaly Kids Club, Casablanca…"
                value={keywords}
                onChange={(e) => setKeywords(e.target.value)}
              />
            </div>

            {/* Actions */}
            <div className="pt-2 flex flex-col gap-2">
              <button
                onClick={handleGenerate}
                disabled={loading || !topic.trim()}
                className="w-full py-2.5 rounded-2xl bg-gradient-to-r from-vl_primary to-vl_accent text-sm font-semibold text-white hover:from-vl_primary/90 hover:to-vl_accent/90 disabled:opacity-60 disabled:cursor-not-allowed"
              >
                {loading ? "Generating…" : "🚀 Generate content"}
              </button>
              <div className="flex gap-2 text-xs">
                <button
                  onClick={handleGenerateImage}
                  disabled={loading || (!imagePrompt && !topic.trim())}
                  className="flex-1 py-2 rounded-2xl bg-slate-900 text-slate-100 border border-slate-700 hover:bg-slate-800 disabled:opacity-60 disabled:cursor-not-allowed"
                >
                  🎨 Generate image
                </button>
                <button
                  onClick={handleCopyVeo}
                  disabled={!videoPrompt}
                  className="flex-1 py-2 rounded-2xl bg-slate-900 text-slate-100 border border-slate-700 hover:bg-slate-800 disabled:opacity-60 disabled:cursor-not-allowed"
                >
                  🎬 Copy Veo prompt
                </button>
              </div>
            </div>
          </section>

          {/* RIGHT: OUTPUT */}
          <section className="card-dark p-5 flex flex-col gap-4">
            {/* TEXT RESULT */}
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-[11px] font-semibold text-slate-400 uppercase tracking-wide">
                  Text & script
                </h2>
              </div>
              <div className="flex items-center gap-2 text-xs text-slate-400">
                <button
                  onClick={handleCopyAll}
                  disabled={!generatedBody && !generatedTitle}
                  className="px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-700 hover:bg-slate-800 disabled:opacity-60 disabled:cursor-not-allowed flex items-center gap-1"
                >
                  📋 Copy all
                </button>
              </div>
            </div>

            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 px-4 py-3 min-h-[180px] overflow-y-auto">
              {generatedTitle || generatedBody ? (
                <div className="space-y-3 text-sm text-slate-100">
                  {generatedTitle && (
                    <h3 className="text-base font-semibold">{generatedTitle}</h3>
                  )}
                  {generatedBody && (
                    <p className="whitespace-pre-wrap text-sm text-slate-200">
                      {generatedBody}
                    </p>
                  )}
                  {generatedHashtags?.length > 0 && (
                    <p className="text-xs text-vl_accent font-medium">
                      {generatedHashtags.map((h) => "#" + h).join(" ")}
                    </p>
                  )}
                </div>
              ) : (
                <div className="h-full grid place-items-center text-center text-xs text-slate-500">
                  <div className="space-y-3 max-w-sm">
                    <div className="mx-auto h-10 w-10 rounded-full border border-vl_accent grid place-items-center text-2xl text-vl_accent">
                      ✨
                    </div>
                    <h3 className="text-sm font-semibold text-slate-100">
                      Your content will appear here
                    </h3>
                    <p>
                      Describe your idea on the left, pick your platform, then hit{" "}
                      <span className="font-semibold text-slate-100">Generate content</span>.
                    </p>
                  </div>
                </div>
              )}
            </div>

            {/* LOWER GRID: IMAGE + PLATFORM PREVIEW + VEO PROMPT */}
            <div className="grid lg:grid-cols-2 gap-3">
              {/* IMAGE */}
              <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-3 text-xs text-slate-300 flex flex-col gap-2">
                <div className="flex items-center justify-between">
                  <span className="font-semibold">Visual</span>
                  <span className="text-[10px] text-slate-500">For Stitch / Canva / etc.</span>
                </div>
                {imageUrl ? (
                  <div>
                    <img
                      src={imageUrl}
                      alt="Generated visual"
                      className="w-full rounded-xl border border-slate-700 mb-2"
                    />
                    <a
                      href={imageUrl}
                      download
                      className="inline-flex items-center text-[11px] text-vl_accent hover:underline"
                    >
                      ⬇ Download image
                    </a>
                  </div>
                ) : (
                  <p className="text-[11px] text-slate-400">
                    Image will be based on:{" "}
                    <span className="text-slate-100">
                      {imagePrompt || "Generate content, then click Generate image."}
                    </span>
                  </p>
                )}
              </div>

              {/* PLATFORM PREVIEW & VEO PROMPT SHORTCUT */}
              <div className="space-y-3">
                <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-3 text-xs text-slate-300">
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-semibold">Platform preview</span>
                    <span className="text-[10px] text-slate-500 uppercase">
                      {platformId}
                    </span>
                  </div>
                  <div className="rounded-xl bg-slate-950 border border-slate-800 p-2 space-y-1">
                    <div className="text-slate-100 font-semibold text-[11px] truncate">
                      {generatedTitle || "Your first line / hook appears here"}
                    </div>
                    <div className="text-slate-400 text-[11px] line-clamp-3">
                      {generatedBody ||
                        "Preview of how your text will look inside a post or caption. Keep the first 1–2 lines very strong."}
                    </div>
                    <div className="mt-1 text-vl_accent text-[11px] truncate">
                      {generatedHashtags?.length
                        ? generatedHashtags.map((h) => "#" + h).join(" ")
                        : "#viralobby #ai #content"}
                    </div>
                  </div>
                  <p className="text-[10px] text-slate-500 mt-1">
                    Use this as a guide when placing title, body and tags in Stitch or your design tool.
                  </p>
                </div>

                <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-3 text-xs text-slate-300">
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-semibold">Veo2 / Veo3 prompt</span>
                    <button
                      onClick={handleCopyVeo}
                      disabled={!videoPrompt}
                      className="px-2 py-1 rounded-lg bg-slate-900 border border-slate-700 hover:bg-slate-800 disabled:opacity-60 disabled:cursor-not-allowed text-[11px]"
                    >
                      Copy
                    </button>
                  </div>
                  <textarea
                    readOnly
                    value={videoPrompt}
                    className="w-full h-24 bg-slate-950 border border-slate-800 rounded-xl p-2 text-[11px] text-slate-200"
                    placeholder="When you generate content, a ready-to-paste Veo prompt will appear here. Paste it into Google Veo to create your video."
                  />
                </div>
              </div>
            </div>
          </section>
        </main>
      </div>
    </div>
  );
}
