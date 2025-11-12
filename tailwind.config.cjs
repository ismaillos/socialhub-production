
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./pages/**/*.{js,ts,jsx,tsx}", "./components/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        vl_primary: "#6C4CF7",
        vl_accent: "#00D1B2"
      },
      backgroundImage: {
        "hero-gradient":
          "radial-gradient(1200px 600px at 10% -10%, rgba(108,76,247,0.25), transparent), radial-gradient(1200px 600px at 110% 10%, rgba(0,209,178,0.25), transparent)"
      }
    }
  },
  plugins: []
};
