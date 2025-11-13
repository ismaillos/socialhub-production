
import Link from "next/link";
import { useRouter } from "next/router";

const links = [
  { href: "/dashboard", label: "Dashboard", icon: "🏠" },
  { href: "/create", label: "Create", icon: "✨" },
  { href: "/review", label: "Review", icon: "📝" },
  { href: "/library", label: "Library", icon: "🗂️" },
  { href: "/analytics", label: "Analytics", icon: "📊" }
];

export default function Sidebar() {
  const router = useRouter();
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="flex items-center gap-3">
          <div className="h-9 w-9 rounded-2xl bg-gradient-to-tr from-vl_primary to-vl_accent grid place-items-center text-sm font-bold">
            VL
          </div>
          <div className="flex flex-col leading-tight">
            <span className="text-sm font-semibold">Viralobby</span>
            <span className="text-[11px] text-slate-400">AI Studio</span>
          </div>
        </div>
      </div>
      <nav className="sidebar-nav">
        {links.map((link) => {
          const active = router.pathname === link.href;
          return (
            <Link
              key={link.href}
              href={link.href}
              className={`sidebar-link ${active ? "sidebar-link-active" : ""}`}
            >
              <span className="text-lg">{link.icon}</span>
              <span>{link.label}</span>
            </Link>
          );
        })}
      </nav>
      <div className="px-4 pb-4 pt-2 border-t border-slate-800 text-xs text-slate-400 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="h-8 w-8 rounded-full bg-slate-800 grid place-items-center text-xs">
            JD
          </div>
          <div>
            <div className="text-[11px] font-medium text-slate-100">John Doe</div>
            <div className="text-[10px] text-slate-500">john.doe@example.com</div>
          </div>
        </div>
        <span className="text-slate-500 text-lg">⋮</span>
      </div>
    </aside>
  );
}
