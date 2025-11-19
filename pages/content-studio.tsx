
"use client";
import React, { useState } from "react";

export default function ContentStudio() {
  const [type, setType] = useState("blog");
  const [topic, setTopic] = useState("");
  const [keywords, setKeywords] = useState("");
  const [audience, setAudience] = useState("");
  const [tone, setTone] = useState("Professional");

  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const generate = async () => {
    if (!topic) return;

    setLoading(true);
    setResult(null);

    try {
      const res = await fetch("/api/generate-content", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ contentType: type, topic, keywords, audience, tone })
      });

      const data = await res.json();
      if (!res.ok) {
        console.error("API error:", data);
      }
      setResult(data);
    } catch (err) {
      console.error("Network error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    if (!result) return;
    const full = [
      result.title || "",
      "",
      result.intro || "",
      "",
      result.body || "",
      "",
      result.outro || "",
      "",
      (result.hashtags || []).map((h: string) => `#${h}`).join(" ")
    ].join("\n");
    navigator.clipboard.writeText(full).catch(() => {});
  };

  return (
    <div className="flex min-h-screen bg-[#F1F5F9]">
      {/* SIDEBAR */}
      <aside className="w-64 bg-white border-r border-gray-200 p-6 flex flex-col">
        <div className="flex items-center mb-10">
          <div className="h-10 w-10 rounded-lg bg-blue-600 text-white grid place-items-center text-lg font-bold">
            VL
          </div>
          <h1 className="ml-3 text-lg font-semibold text-gray-800">Viralobby</h1>
        </div>

        <SidebarItem label="Dashboard" />
        <SidebarItem label="Create Content" active />
        <SidebarItem label="Projects" />
        <SidebarItem label="Content Library" />
        <SidebarItem label="Analytics" />
        <SidebarItem label="Settings" />

        <div className="mt-auto pt-6 border-t border-gray-200 flex items-center">
          <div className="h-9 w-9 rounded-full bg-gray-300" />
          <div className="ml-3">
            <p className="font-medium text-sm">John Doe</p>
            <p className="text-xs text-gray-500">john@example.com</p>
          </div>
        </div>
      </aside>

      {/* MAIN */}
      <main className="flex-1 p-10">
        {/* HEADER */}
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-2xl font-semibold text-gray-800">Create Content</h1>
          <div className="h-10 w-10 bg-gray-300 rounded-full" />
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
          {/* LEFT FORM */}
          <div className="bg-white rounded-2xl shadow p-8 border border-gray-100 space-y-6">
            <h2 className="text-gray-700 font-semibold text-sm">1. Content Type</h2>

            <div className="flex gap-3">
              <TypeOption label="Blog Post" value="blog" current={type} set={setType} />
              <TypeOption label="Carousel" value="carousel" current={type} set={setType} />
              <TypeOption label="Image Post" value="image" current={type} set={setType} />
            </div>

            <h2 className="text-gray-700 font-semibold text-sm pt-4">2. Content Details</h2>

            <InputArea
              label="Topic / Prompt"
              value={topic}
              set={setTopic}
              placeholder="Write about digital marketing trends…"
            />
            <Input
              label="Keywords"
              value={keywords}
              set={setKeywords}
              placeholder="AI, SEO, automation…"
            />

            <div className="grid grid-cols-2 gap-4">
              <Input
                label="Audience"
                value={audience}
                set={setAudience}
                placeholder="Small business owners…"
              />
              <Select
                label="Tone"
                value={tone}
                set={setTone}
                options={["Professional", "Friendly", "Bold", "Playful"]}
              />
            </div>

            <button
              onClick={generate}
              className="w-full py-3 bg-blue-600 text-white rounded-xl font-medium hover:bg-blue-500 transition disabled:opacity-60"
              disabled={loading}
            >
              {loading ? "Generating…" : "Generate Content"}
            </button>
          </div>

          {/* RIGHT RESULT */}
          <div className="bg-white rounded-2xl shadow p-8 border border-gray-100 flex flex-col">
            <div className="flex justify-between mb-4">
              <h2 className="text-gray-700 font-semibold text-sm">Generated Content</h2>
              <div className="flex gap-3 text-sm text-gray-500">
                <button
                  onClick={handleCopy}
                  disabled={!result}
                  className="hover:text-gray-700 disabled:opacity-40"
                >
                  Copy
                </button>
                <button className="hover:text-gray-700">Export</button>
              </div>
            </div>

            <div className="flex-1 h-[75vh] overflow-auto border border-gray-200 rounded-xl p-6 bg-gray-50">
              {!result && (
                <div className="text-center text-gray-500 mt-20">
                  <div className="h-12 w-12 rounded-full bg-blue-100 text-blue-600 grid place-items-center mx-auto mb-4 text-xl">
                    ✨
                  </div>
                  <p className="font-medium">Content will appear here</p>
                  <p className="text-xs mt-1 text-gray-500">
                    Fill the form on the left and click “Generate Content”.
                  </p>
                </div>
              )}

              {result && (
                <div className="space-y-4 text-sm text-gray-800">
                  {result.title && (
                    <h3 className="text-xl font-semibold text-gray-900">
                      {result.title}
                    </h3>
                  )}
                  {result.intro && <p>{result.intro}</p>}
                  {result.body && (
                    <p className="whitespace-pre-line">{result.body}</p>
                  )}
                  {result.outro && <p>{result.outro}</p>}
                  {Array.isArray(result.hashtags) && result.hashtags.length > 0 && (
                    <p className="text-blue-600 font-semibold">
                      {result.hashtags.map((h: string) => `#${h} `)}
                    </p>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

function SidebarItem({ label, active = false }: { label: string; active?: boolean }) {
  return (
    <div
      className={`px-4 py-2 rounded-lg mb-2 text-sm cursor-pointer transition 
      ${active ? "bg-blue-100 text-blue-600 font-medium" : "text-gray-600 hover:bg-gray-100"}
      `}
    >
      {label}
    </div>
  );
}

function TypeOption({
  label,
  value,
  current,
  set
}: {
  label: string;
  value: string;
  current: string;
  set: (v: string) => void;
}) {
  const active = current === value;
  return (
    <button
      onClick={() => set(value)}
      className={`flex-1 py-3 rounded-xl border text-sm transition
      ${active ? "border-blue-500 bg-blue-50 text-blue-600" : "border-gray-200 bg-white text-gray-600"}
      `}
    >
      {label}
    </button>
  );
}

function Input({
  label,
  value,
  set,
  placeholder
}: {
  label: string;
  value: string;
  set: (v: string) => void;
  placeholder?: string;
}) {
  return (
    <div className="space-y-1">
      <p className="text-xs font-medium text-gray-600">{label}</p>
      <input
        className="w-full px-3 py-2 border border-gray-300 rounded-lg bg-white text-gray-800 focus:ring-2 focus:ring-blue-300 outline-none text-sm"
        value={value}
        onChange={(e) => set(e.target.value)}
        placeholder={placeholder}
      />
    </div>
  );
}

function InputArea({
  label,
  value,
  set,
  placeholder
}: {
  label: string;
  value: string;
  set: (v: string) => void;
  placeholder?: string;
}) {
  return (
    <div className="space-y-1">
      <p className="text-xs font-medium text-gray-600">{label}</p>
      <textarea
        className="w-full h-32 px-3 py-2 border border-gray-300 rounded-lg bg-white text-gray-800 focus:ring-2 focus:ring-blue-300 outline-none text-sm"
        value={value}
        onChange={(e) => set(e.target.value)}
        placeholder={placeholder}
      />
    </div>
  );
}

function Select({
  label,
  value,
  set,
  options
}: {
  label: string;
  value: string;
  set: (v: string) => void;
  options: string[];
}) {
  return (
    <div className="space-y-1">
      <p className="text-xs font-medium text-gray-600">{label}</p>
      <select
        className="w-full px-3 py-2 border border-gray-300 rounded-lg bg-white text-gray-800 focus:ring-2 focus:ring-blue-300 outline-none text-sm"
        value={value}
        onChange={(e) => set(e.target.value)}
      >
        {options.map((o) => (
          <option key={o}>{o}</option>
        ))}
      </select>
    </div>
  );
}
