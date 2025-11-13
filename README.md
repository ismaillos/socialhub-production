
# Viralobby Studio – Full App (B version)

- Next.js 14 + React 18 + Tailwind CSS
- Beautiful dark UI inspired by your screenshots
- Working content generator connected to OpenAI:
  - `/api/generate` → text + hashtags + imagePrompt + Veo2/3 videoPrompt
  - `/api/generate-image` → AI image (1024x1024)
- Screens:
  - `/dashboard` (also `/`) – overview
  - `/create` – main studio (Reel / Image / Carousel)
  - `/review` – sample review view
  - `/library` – templates & assets
  - `/analytics` – placeholder

## Setup

1. Install dependencies:

```bash
npm install
```

2. Set your OpenAI API key:

```bash
export OPENAI_API_KEY=sk-xxx   # macOS / Linux
setx OPENAI_API_KEY "sk-xxx"   # Windows PowerShell (then restart)
```

3. Dev:

```bash
npm run dev
```

→ Open http://localhost:3000/create

4. Deploy (Vercel / cPanel Node):

- Add env var `OPENAI_API_KEY`
- Run:

```bash
npm install
npm run build
npm start
```
