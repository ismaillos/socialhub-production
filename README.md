
# Viralobby Studio

Viralobby Studio is a small Next.js app that helps creators, freelancers and brands generate viral-style content using AI.

- Multilingual UI: **FR / EN / AR (Modern Standard Arabic)**
- AI text generation (OpenAI Chat Completions API)
- AI image generation (OpenAI Images API with `gpt-image-1`)
- Viral templates page to start from proven content patterns

## Tech stack

- Next.js 14
- React 18
- Tailwind CSS
- TypeScript

## Getting started

```bash
npm install
cp .env.example .env.local
# edit .env.local and set:
# OPENAI_API_KEY=sk-...

npm run dev
```

Then open http://localhost:3000

## Deployment

The app is optimized for Vercel.

1. Push the code to GitHub (or upload directly in Vercel).
2. In Vercel Project Settings → Environment Variables:
   - `OPENAI_API_KEY` = your key
3. Deploy.
4. Optionally, attach a custom domain like `studio.viralobby.com`.
