
import Sidebar from "@/components/Sidebar";
import Topbar from "@/components/Topbar";

export default function AnalyticsPage() {
  return (
    <div className="app-shell">
      <Sidebar />
      <div className="main-area">
        <Topbar
          title="Analytics"
          subtitle="Soon: see which ideas and formats perform best."
          right={null}
        />
        <div className="page-body p-6">
          <div className="card-light p-6 text-sm text-slate-300">
            <p>
              In a next step, this page can connect to Meta, TikTok, YouTube or your own
              database to show performance dashboards: views, saves, CTR, watch time, etc.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
