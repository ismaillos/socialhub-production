
export default function Topbar({ title, subtitle, right }) {
  return (
    <header className="topbar">
      <div>
        <h1 className="text-sm font-semibold text-slate-50">{title}</h1>
        {subtitle && (
          <p className="text-xs text-slate-500 mt-0.5">{subtitle}</p>
        )}
      </div>
      <div className="flex items-center gap-3">
        {right}
      </div>
    </header>
  );
}
