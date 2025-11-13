
import Sidebar from "@/components/Sidebar";
import Topbar from "@/components/Topbar";

export default function LibraryPage() {
  return (
    <div className="app-shell">
      <Sidebar />
      <div className="main-area">
        <Topbar
          title="Library"
          subtitle="Templates, assets and past generated content."
          right={
            <button className="btn-primary text-xs rounded-full px-3 py-1.5">
              + Upload asset
            </button>
          }
        />

        <div className="page-body p-6 space-y-6">
          <section className="flex flex-wrap items-center justify-between gap-3">
            <div className="flex flex-wrap gap-2 text-xs">
              <button className="btn-ghost px-3 py-1.5 rounded-full">
                Filter
              </button>
              <button className="btn-ghost px-3 py-1.5 rounded-full">
                Sort by date
              </button>
            </div>
            <div className="relative w-full sm:w-80">
              <input
                className="input pl-8 pr-3 py-2 text-xs"
                placeholder="Search templates or assets…"
              />
              <span className="absolute left-2 top-1.5 text-slate-500 text-sm">
                🔍
              </span>
            </div>
          </section>

          <section className="grid sm:grid-cols-3 lg:grid-cols-5 gap-4">
            {[
              { label: "Reel templates", files: "15 layouts" },
              { label: "Carousel frames", files: "22 layouts" },
              { label: "Image posts", files: "40 layouts" },
              { label: "Brand assets", files: "Logo, colors, fonts" },
              { label: "New collection", files: "Create" }
            ].map((folder) => (
              <div
                key={folder.label}
                className="card-light p-4 flex flex-col justify-between cursor-pointer hover:shadow-soft"
              >
                <div className="h-8 w-12 rounded-xl bg-slate-800 mb-3" />
                <div>
                  <p className="text-xs font-medium text-slate-50">
                    {folder.label}
                  </p>
                  <p className="text-[11px] text-slate-400">{folder.files}</p>
                </div>
              </div>
            ))}
          </section>

          <section className="space-y-3">
            <h2 className="text-sm font-semibold text-slate-50">Recent generated content</h2>
            <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
              {[
                { type: "Reel script", name: "AI helps teachers save time", when: "2 days ago" },
                { type: "Carousel", name: "5 ways to use SDG4 in class", when: "4 days ago" },
                { type: "Image post", name: "Welcome back to school", when: "1 week ago" },
                { type: "Reel script", name: "Behind the scenes at Amaly", when: "2 weeks ago" }
              ].map((file) => (
                <div key={file.name} className="card-light p-3 space-y-2">
                  <div className="h-16 rounded-lg bg-slate-800 mb-1" />
                  <div className="badge-pill bg-slate-900 text-slate-200 border border-slate-700 inline-block">
                    {file.type}
                  </div>
                  <p className="text-[11px] font-medium text-slate-50 truncate">
                    {file.name}
                  </p>
                  <p className="text-[10px] text-slate-500">{file.when}</p>
                </div>
              ))}
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}
