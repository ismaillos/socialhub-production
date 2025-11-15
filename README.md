
# Viralobby Studio v6 — Vercel-ready env

## Setup (local)
```bash
npm install
cp .env.example .env.local
# put your OpenAI key:
# OPENAI_API_KEY=sk-...
npm run dev
```

## Deploy on Vercel
1. Settings → Environment Variables
2. Add `OPENAI_API_KEY` with your real key
3. Enable for Development, Preview, Production
4. Redeploy

APIs use: `process.env.OPENAI_API_KEY` → sent as `Authorization: Bearer ${apiKey}`.
