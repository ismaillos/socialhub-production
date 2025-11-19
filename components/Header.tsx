
import Link from "next/link";
export default function Header(){
  return (
    <header className="sticky top-0 z-30 border-b bg-white/80 backdrop-blur">
      <div className="container py-3 flex items-center justify-between">
        <Link href="/" className="text-base sm:text-lg font-semibold text-vl_primary">Viralobby Studio</Link>
        <nav className="flex items-center gap-4 text-sm">
          <Link href="/create" className="text-slate-700 hover:text-vl_primary">Create</Link>
          <Link href="/templates" className="text-slate-700 hover:text-vl_primary">Templates</Link>
        </nav>
      </div>
    </header>
  );
}
