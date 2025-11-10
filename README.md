
# Viralobby Studio (v2)

Viralobby Studio est une application Next.js qui permet de générer du contenu viral en FR / EN / AR avec l’IA.

Fonctionnalités :
- Types de contenu : Vidéo courte (Reel/TikTok), Post image + texte, Carrousel
- Génération IA structurée (hook + body + CTA + description de visuel + hashtags)
- Génération d’image avec l’API d’images OpenAI (`gpt-image-1`)
- Interface trilingue : Français, Anglais, Arabe standard moderne
- Page Templates pour démarrer avec des modèles prêts à l’emploi

## Stack

- Next.js 14
- React 18
- Tailwind CSS
- TypeScript
- API OpenAI (Chat + Images)

## Installation

```bash
npm install
cp .env.example .env.local
# puis édite .env.local et configure :
# OPENAI_API_KEY=sk-...

npm run dev
```

Application disponible sur : http://localhost:3000

## Backend IA : comment ça fonctionne ?

- Le frontend appelle l’API interne Next.js `/api/generate`.
- Cette route construit un prompt structuré avec :
  - type de contenu (vidéo / post / carrousel)
  - langue (FR / EN / AR)
  - thème
  - ton
  - idée utilisateur
- Elle appelle l’API OpenAI **Chat Completions** (modèle `gpt-4o-mini`) et demande un JSON strict :
  - `hook`, `body`, `cta`, `visualDescription`, `hashtags[]`
- Le backend recombine `hook + body + cta` en un `text` final qui est envoyé au frontend, avec :
  - une proposition de visuel (`imagePrompt`)
  - une liste de hashtags

Pour l’image :
- Le frontend appelle `/api/generate-image` avec le `imagePrompt`.
- Cette route appelle l’API OpenAI **Images** (`gpt-image-1`) et renvoie une URL d’image.
- Le frontend affiche l’image et propose de la télécharger.

Tu peux déployer ce projet sur Vercel ou dans n’importe quel environnement Node.js.
