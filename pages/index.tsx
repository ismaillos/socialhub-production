
import Link from "next/link";
export default function Home(){
  return (
    <div className="min-h-[70vh] bg-hero-gradient grid place-items-center">
      <div className="text-center space-y-5">
        <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight">Viralobby Studio</h1>
        <p className="text-slate-600 max-w-2xl mx-auto">Générez un post, une image et un <b>video prompt</b> prêt à coller dans Google Veo 2/3. Aperçus par plateforme et hashtags mis en avant.</p>
        <div className="flex gap-3 justify-center">
          <Link href="/create" className="vl-btn vl-btn-primary">🚀 Créer maintenant</Link>
          <Link href="/templates" className="vl-btn vl-btn-ghost">📚 Templates</Link>
        </div>
      </div>
    </div>
  );
}
