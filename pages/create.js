
import { useState } from "react";
import Sidebar from "@/components/Sidebar";

export default function CreatePage() {
  const [topic, setTopic] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    if (!topic.trim()) return;
    setLoading(true);
    try {
      const res = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic })
      });
      const data = await res.json();
      if (!res.ok) {
        alert(data.error || "Error");
        return;
      }
      setResult(JSON.stringify(data, null, 2));
    } catch (e) {
      console.error(e);
      alert("Network error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <Sidebar />
      <div className="flex-1 flex flex-col bg-slate-950">
        <header className="topbar">
          <div>
            <h1 className="text-sm font-semibold text-slate-50">Create (MVP)</h1>
            <p className="text-xs text-slate-500 mt-0.5">
              Simple test screen wired to /api/generate.
            </p>
          </div>
        </header>
        <main className="page-body p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
          <section className="card-dark p-5 space-y-3">
            <textarea
              className="textarea"
              placeholder="Describe your idea…"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
            />
            <button
              onClick={handleGenerate}
              disabled={loading || !topic.trim()}
              className="btn-primary w-full"
            >
              {loading ? "Generating…" : "Generate"}
            </button>
          </section>
          <section className="card-dark p-5">
            <pre className="text-xs whitespace-pre-wrap text-slate-200">
              {result || "Result will appear here."}
            </pre>
          </section>
        </main>
      </div>
    </div>
  );
}
