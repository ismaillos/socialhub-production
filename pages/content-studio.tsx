
"use client";
import React, { useState } from "react";

type ContentType = "blog" | "carousel" | "image";

type GeneratedResult = {
  title: string;
  intro: string;
  body: string;
  outro: string;
  hashtags: string[];
};

export default function ContentCreationStudio() {
  const [activeType, setActiveType] = useState<ContentType>("blog");
  const [topic, setTopic] = useState("");
  const [keywords, setKeywords] = useState("");
  const [audience, setAudience] = useState("");
  const [tone, setTone] = useState("Professional");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<GeneratedResult | null>(null);

  const handleGenerate = async () => {
    if (!topic.trim()) {
      setError("Please enter a topic / prompt.");
      return;
    }
    setError(null);
    setLoading(true);
    setResult(null);

    try {
      const res = await fetch("/api/generate-content", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          contentType: activeType,
          topic,
          keywords,
          audience,
          tone
        })
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.error || "Unexpected API error.");
        return;
      }
      setResult(data as GeneratedResult);
    } catch (err) {
      console.error(err);
      setError("Network error while calling the AI backend.");
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    if (!result) return;
    const full = [
      result.title,
      "",
      result.intro,
      "",
      result.body,
      "",
      result.outro,
      "",
      result.hashtags.map((h) => `#${h}`).join(" ")
    ].join("\n");
    navigator.clipboard.writeText(full).catch(() => {});
  };

  return (
    <div className="min-h-screen bg-[#0C111B] text-slate-100 flex">
      {/* SIDEBAR */}
      <aside className="w-64 bg-[#0C111B] border-r border-slate-800 flex flex-col">
        <div className="h-16 flex items-center px-6 border-b border-slate-800">
          <div className="h-9 w-9 rounded-lg bg-emerald-500 grid place-items-center text-sm font-semibold">
            VL
          </div>
          <div className="ml-3">
            <p className="text-sm font-semibold">Viralobby</p>
            <p className="text-[11px] text-slate-400">Content Studio</p>
          </div>
        </div>

        <nav className="flex-1 px-4 py-4 space-y-2 text-sm">
          <MenuItem label="Create Content" icon="✨" active />
          <MenuItem label="History" icon="🕒" />
          <MenuItem label="My Projects" icon="📁" />
          <MenuItem label="Analytics" icon="📊" />
        </nav>

        <div className="border-t border-slate-800 px-4 py-3 flex items-center gap-3 text-xs">
          <div className="h-9 w-9 rounded-full bg-slate-700 grid place-items-center">
            JD
          </div>
          <div>
            <p className="font-medium">John Doe</p>
            <p className="text-slate-400">john.doe@example.com</p>
          </div>
        </div>
      </aside>

      {/* MAIN AREA */}
      <main className="flex-1 flex flex-col">
        <header className="h-16 border-b border-slate-800 flex items-center px-8">
          <h1 className="text-xl font-semibold tracking-tight">
            Content Creation Studio
          </h1>
        </header>

        <div className="flex-1 grid grid-cols-1 xl:grid-cols-2">
          {/* LEFT FORM */}
          <section className="px-10 py-8 border-r border-slate-800">
            {/* Step 1 */}
            <div className="mb-8">
              <h2 className="text-xs uppercase tracking-wide text-slate-400 font-semibold mb-3">
                1. Choose Content Type
              </h2>

              <div className="flex gap-4">
                <TypeButton
                  label="Blog Post"
                  active={activeType === "blog"}
                  onClick={() => setActiveType("blog")}
                />
                <TypeButton
                  label="Carousel"
                  active={activeType === "carousel"}
                  onClick={() => setActiveType("carousel")}
                />
                <TypeButton
                  label="Image Blog"
                  active={activeType === "image"}
                  onClick={() => setActiveType("image")}
                />
              </div>
            </div>

            {/* Step 2 */}
            <div className="space-y-6">
              <h2 className="text-xs uppercase tracking-wide text-slate-400 font-semibold">
                2. Blog Post Details
              </h2>

              {/* Topic */}
              <div className="space-y-1">
                <label className="text-xs text-slate-300">Topic / Prompt</label>
                <textarea
                  placeholder="e.g., 'Write a blog post about the top 5 digital marketing trends for 2024'"
                  className="w-full h-32 px-3 py-2 rounded-lg bg-[#111827] border border-slate-700 text-sm text-slate-200 placeholder-slate-500 outline-none focus:ring-2 focus:ring-emerald-500/40"
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                />
              </div>

              {/* Keywords */}
              <div className="space-y-1">
                <label className="text-xs text-slate-300">Keywords</label>
                <input
                  placeholder="e.g., AI, SEO trends, video content, automation"
                  className="w-full px-3 py-2 rounded-lg bg-[#111827] border border-slate-700 text-sm text-slate-200 placeholder-slate-500 outline-none focus:ring-2 focus:ring-emerald-500/40"
                  value={keywords}
                  onChange={(e) => setKeywords(e.target.value)}
                />
              </div>

              {/* Audience + Tone */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-xs text-slate-300">
                    Target Audience <span className="text-slate-500 ml-1">(Optional)</span>
                  </label>
                  <input
                    placeholder="e.g. Small business owners"
                    className="w-full px-3 py-2 rounded-lg bg-[#111827] border border-slate-700 text-sm text-slate-200 placeholder-slate-500 outline-none focus:ring-2 focus:ring-emerald-500/40"
                    value={audience}
                    onChange={(e) => setAudience(e.target.value)}
                  />
                </div>

                <div>
                  <label className="text-xs text-slate-300">Tone of Voice</label>
                  <select
                    className="w-full px-3 py-2 rounded-lg bg-[#111827] border border-slate-700 text-sm text-slate-200 outline-none focus:ring-2 focus:ring-emerald-500/40"
                    value={tone}
                    onChange={(e) => setTone(e.target.value)}
                  >
                    <option>Professional</option>
                    <option>Friendly</option>
                    <option>Bold</option>
                    <option>Playful</option>
                    <option>Educational</option>
                  </select>
                </div>
              </div>
            </div>

            {error && (
              <p className="mt-4 text-xs text-red-400 bg-red-950/40 border border-red-900 rounded-lg px-3 py-2">
                {error}
              </p>
            )}

            {/* Generate button */}
            <div className="mt-10">
              <button
                onClick={handleGenerate}
                disabled={loading}
                className="w-full py-3 rounded-lg bg-emerald-500 text-slate-900 font-semibold text-sm flex items-center justify-center gap-2 hover:bg-emerald-400 transition disabled:opacity-60 disabled:cursor-not-allowed"
              >
                ✨ {loading ? "Generating..." : "Generate Blog Post"}
              </button>
            </div>
          </section>

          {/* RIGHT RESULT PANEL */}
          <section className="px-10 py-8">
            <header className="flex items-center justify-between mb-6">
              <h2 className="text-sm font-semibold">Generated Content</h2>

              <div className="flex items-center gap-4 text-xs text-slate-400">
                <button
                  onClick={handleCopy}
                  disabled={!result}
                  className="hover:text-white flex items-center gap-1 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  📋 Copy
                </button>
                <button className="hover:text-white flex items-center gap-1">
                  ⬇ Export
                </button>
              </div>
            </header>

            <div className="border border-slate-800 rounded-2xl bg-[#0F1624] h-[80vh] p-6 overflow-y-auto">
              {result ? (
                <article className="space-y-3 text-sm text-slate-100">
                  <h3 className="text-base font-semibold">{result.title}</h3>
                  {result.intro && <p>{result.intro}</p>}
                  {result.body && (
                    <p className="whitespace-pre-wrap">{result.body}</p>
                  )}
                  {result.outro && <p>{result.outro}</p>}
                  {result.hashtags?.length > 0 && (
                    <p className="text-xs text-emerald-400 font-medium">
                      {result.hashtags.map((h) => `#${h}`).join(" ")}
                    </p>
                  )}
                </article>
              ) : (
                <div className="h-full grid place-items-center text-center">
                  <div className="max-w-xs space-y-3">
                    <div className="h-12 w-12 rounded-full border border-emerald-500 grid place-items-center text-2xl text-emerald-500 mx-auto">
                      ✨
                    </div>
                    <p className="text-sm font-semibold">
                      Your AI-powered content will appear here
                    </p>
                    <p className="text-xs text-slate-400 leading-relaxed">
                      Fill out the details on the left and click
                      {" "}
                      <span className="text-white font-semibold">
                        "Generate Blog Post"
                      </span>
                      {" "}
                      to see the magic happen.
                    </p>
                  </div>
                </div>
              )}
            </div>
          </section>
        </div>
      </main>
    </div>
  );
}

interface MenuItemProps {
  label: string;
  icon: string;
  active?: boolean;
}

function MenuItem({ label, icon, active }: MenuItemProps) {
  return (
    <div
      className={`flex items-center gap-3 px-3 py-2 rounded-md cursor-pointer text-sm 
      ${
        active
          ? "bg-[#111827] text-white"
          : "text-slate-300 hover:bg-[#111827]/60"
      }`}
    >
      <span>{icon}</span>
      <span>{label}</span>
    </div>
  );
}

interface TypeButtonProps {
  label: string;
  active: boolean;
  onClick: () => void;
}

function TypeButton({ label, active, onClick }: TypeButtonProps) {
  return (
    <button
      onClick={onClick}
      className={`flex-1 px-4 py-3 rounded-xl border text-left transition 
      ${
        active
          ? "border-emerald-500 bg-[#111827] text-white"
          : "border-slate-700 bg-[#111827]/40 text-slate-300 hover:border-slate-500"
      }`}
    >
      <p className="font-medium">{label}</p>
      <p className="text-[11px] text-slate-400 mt-1">
        {label === "Blog Post" &&
          "Generate full blog posts from a single prompt."}
        {label === "Carousel" &&
          "Create multi-slide viral content for social media."}
        {label === "Image Blog" && "Create short posts with a hero image."}
      </p>
    </button>
  );
}
