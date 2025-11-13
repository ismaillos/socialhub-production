
import Link from "next/link";
import Layout from "../components/Layout";
export default function Home(){
  return (
    <Layout>
      <section className="grid md:grid-cols-2 gap-8 items-center">
        <div className="space-y-6">
          <span className="vl-chip border-vl_primary/30 bg-white/70 text-vl_primary">
            <span className="w-2 h-2 rounded-full bg-vl_primary inline-block" />
            UX-first · AI Social Studio
          </span>
          <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight leading-tight">
            Create viral content with <span className="text-transparent bg-clip-text bg-gradient-to-r from-vl_primary to-vl_accent">clarity</span>.
          </h1>
          <p className="text-slate-600 max-w-xl">
            Describe your idea, pick a content type, and let the AI craft the script, visual prompt, and hashtags — with platform-safe previews.
          </p>
          <div className="flex gap-3">
            <Link href="/create" className="vl-btn vl-btn-primary">🚀 Create content</Link>
            <Link href="/templates" className="vl-btn vl-btn-ghost">📚 Templates</Link>
          </div>
        </div>
        <div className="vl-card p-5">
          <div className="text-sm text-slate-500 mb-2">Example result</div>
          <div className="rounded-2xl border border-slate-200 bg-white p-4">
            <div className="h-40 bg-slate-100 rounded-xl mb-3 grid place-items-center text-slate-400">Visual</div>
            <div className="text-xs">
              <div className="font-semibold mb-1">Script</div>
              <p>Hook + body + CTA… Generated to match platform format.</p>
              <div className="mt-2 font-semibold">#hashtags</div>
              <p>#viralobby #ai #contentcreator</p>
            </div>
          </div>
        </div>
      </section>
    </Layout>
  );
}
