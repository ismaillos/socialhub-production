
module.exports = {
  content: [
    "./pages/**/*.{js,jsx,ts,tsx}",
    "./components/**/*.{js,jsx,ts,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        vl_primary: "#7C3AED",
        vl_accent: "#22C55E",
        vl_dark_bg: "#020617",
        vl_dark_panel: "#020617",
        vl_dark_panel_soft: "#020617",
        vl_dark_border: "rgba(148,163,184,0.25)"
      },
      boxShadow: {
        soft: "0 20px 60px -25px rgba(15,23,42,0.9)"
      },
      borderRadius: {
        "2xl": "1.25rem"
      }
    }
  },
  plugins: []
};
