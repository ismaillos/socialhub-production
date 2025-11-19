
# Viralobby Studio v7 (MVP)

This is a minimal, clean Next.js 14 + Tailwind app with:

- Layout (Sidebar + Topbar)
- `/dashboard` and `/create` pages
- `/api/generate` wired to OpenAI (JSON output)
- `@/` path alias configured via `jsconfig.json`

## Local setup

```bash
npm install
export OPENAI_API_KEY=sk-xxxx   # macOS / Linux
# or setx OPENAI_API_KEY "sk-xxxx" on Windows, then restart terminal
npm run dev
```

Open: http://localhost:3000/create

## Deploy (Vercel / cPanel Node)

- Add env var `OPENAI_API_KEY`
- Build & start:

```bash
npm install
npm run build
npm start
```
