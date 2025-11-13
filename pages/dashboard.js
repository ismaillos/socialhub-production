
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
                desc: "Generate hooks, scripts and prompts for Veo2/3.",
                href: "/create"
              },
              {
                title: "Carousels",
                desc: "Multi-slide storytelling for Instagram / LinkedIn.",
                href: "/create"
              },
              {
                title: "Image Posts",
                desc: "Idea + caption + AI visual in one go.",
                href: "/create"
              },
              {
                title: "Blog / Long-form",
                desc: "Turn ideas into SEO-ready articles.",
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

          <section className="card-light p-4">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-sm font-semibold text-slate-50">Recent Drafts</h2>
              <button className="text-xs text-slate-400 hover:text-slate-200">View All</button>
            </div>
            <div className="overflow-x-auto">
              <table className="min-w-full text-xs">
                <thead>
                  <tr className="text-slate-500 border-b border-slate-800">
                    <th className="text-left py-2 pr-4 font-medium">Title</th>
                    <th className="text-left py-2 pr-4 font-medium">Type</th>
                    <th className="text-left py-2 pr-4 font-medium">Platform</th>
                    <th className="text-left py-2 pr-4 font-medium">Last edited</th>
                    <th className="text-left py-2 font-medium">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                  {[
                    {
                      title: "AI for small businesses",
                      type: "Reel Script",
                      platform: "Instagram / TikTok",
                      edited: "2 hours ago",
                      status: "Draft"
                    },
                    {
                      title: "5 mistakes in digital marketing",
                      type: "Carousel",
                      platform: "Instagram",
                      edited: "Yesterday",
                      status: "Ready"
                    },
                    {
                      title: "Weekly LinkedIn story",
                      type: "Image Post",
                      platform: "LinkedIn",
                      edited: "3 days ago",
                      status: "Draft"
                    },
                    {
                      title: "Full guide: Content system",
                      type: "Blog",
                      platform: "Website",
                      edited: "5 days ago",
                      status: "In Review"
                    }
                  ].map((row) => (
                    <tr key={row.title} className="text-slate-300">
                      <td className="py-2 pr-4">{row.title}</td>
                      <td className="py-2 pr-4">{row.type}</td>
                      <td className="py-2 pr-4">{row.platform}</td>
                      <td className="py-2 pr-4">{row.edited}</td>
                      <td className="py-2">
                        <span className="badge-pill bg-slate-900 text-slate-300 border border-slate-700">
                          {row.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}
