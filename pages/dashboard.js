
import Sidebar from "@/components/Sidebar";
import Topbar from "@/components/Topbar";
import Link from "next/link";

export default function DashboardPage() {
  return (
    <div className="app-shell">
      <Sidebar />
      <div className="main-area">
        <Topbar
          title="Content Studio"
          subtitle="Central hub for your AI-generated content."
          right={
            <button className="btn-primary text-xs px-3 py-1.5 rounded-full">
              + New Project
            </button>
          }
        />
        <div className="page-body p-6 space-y-6">
          <section className="grid md:grid-cols-4 gap-4">
            {[
              {
                title: "Viral Reels / Shorts",
                desc: "Hooks, scripts and Veo prompts.",
                href: "/create"
              },
              {
                title: "Carousels",
                desc: "Multi-slide storytelling for Instagram / LinkedIn.",
                href: "/create"
              },
              {
                title: "Image Posts",
                desc: "Caption + AI visual idea.",
                href: "/create"
              },
              {
                title: "Long-form",
                desc: "Turn ideas into full articles.",
                href: "/create"
              }
            ].map((card) => (
              <Link
                key={card.title}
                href={card.href}
                className="card-light p-4 flex flex-col justify-between hover:shadow-soft hover:border-vl_primary/50 transition"
              >
                <div>
                  <h2 className="text-sm font-semibold text-slate-50">
                    {card.title}
                  </h2>
                  <p className="mt-1 text-xs text-slate-400">{card.desc}</p>
                </div>
                <span className="mt-3 text-[11px] text-vl_primary font-medium">
                  Open →
                </span>
              </Link>
            ))}
          </section>
        </div>
      </div>
    </div>
  );
}
