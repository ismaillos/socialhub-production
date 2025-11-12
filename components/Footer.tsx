
const Footer = () => (
  <footer className="border-t bg-white/70 backdrop-blur">
    <div className="container py-5 text-xs text-slate-500 flex flex-col sm:flex-row items-center justify-between gap-2">
      <div>© {new Date().getFullYear()} Viralobby Studio · Casablanca</div>
      <div>Contact: <a className="text-vl_primary hover:underline" href="mailto:contact@viralobby.com">contact@viralobby.com</a></div>
    </div>
  </footer>
);
export default Footer;
