
module.exports = {
  content: ["./pages/**/*.{js,ts,jsx,tsx}", "./components/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: { vl_primary:"#6C4CF7", vl_accent:"#00D1B2", vl_ink:"#0F172A", vl_bg:"#F6F7FB" },
      boxShadow: { soft:"0 20px 50px -20px rgba(15,23,42,0.25)" },
      backgroundImage: {"hero-gradient":"radial-gradient(1000px 500px at 0% -10%, rgba(108,76,247,0.18), transparent), radial-gradient(1000px 500px at 100% 0%, rgba(0,209,178,0.18), transparent)"}
    }
  },
  plugins: []
};
