
import type { NextApiRequest, NextApiResponse } from "next";

type Data = {
  text: string;
  imagePrompt: string;
  hashtags: string[];
};

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data | { error: string }>
) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { contentType, language, theme, tone, idea } = req.body || {};

  if (!idea || typeof idea !== "string") {
    return res.status(400).json({ error: "Missing idea" });
  }

  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) {
    return res.status(500).json({ error: "Missing OPENAI_API_KEY env var" });
  }

  let langLabel = "French";
  if (language === "EN") langLabel = "English";
  if (language === "AR") langLabel = "Modern Standard Arabic";

  const contentTypeLabel =
    contentType === "carousel"
      ? "carousel (sequence of image + text slides)"
      : contentType === "video"
      ? "short video script (Reel/TikTok)"
      : "image + text social post";

  const systemPrompt = `
Tu es un expert en contenu viral pour TikTok, Reels, Instagram et autres réseaux sociaux.

Type de contenu : ${contentTypeLabel}
Langue : ${langLabel}
Thème : ${theme}
Ton : ${tone}
Idée décrite par l'utilisateur : "${idea}"

Ta mission :
- Produire un contenu court, percutant et adapté à la plateforme.
- Respecter strictement la langue demandée (pas de mélange de langues).
- Pour un carousel, pense en séquence de slides claires.

Retourne UNIQUEMENT un JSON valide de la forme :

{
  "hook": "Phrase d'accroche très courte, qui arrête le scroll.",
  "body": "Développement du message en 2 à 6 phrases courtes (ou 3 à 6 slides pour un carrousel).",
  "cta": "Un appel à l'action clair.",
  "visualDescription": "Description simple d'un visuel qu'on peut générer avec une IA d'image.",
  "hashtags": ["mot1","mot2","mot3","... jusqu'à 8 max"]
}
`;

  try {
    const completion = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model: "gpt-4o-mini",
        messages: [
          { role: "system", content: systemPrompt },
          { role: "user", content: "Génère uniquement le JSON, sans explication." }
        ],
        temperature: 0.9
      })
    });

    if (!completion.ok) {
      const errText = await completion.text();
      console.error("OpenAI error:", errText);
      return res.status(500).json({ error: "OpenAI API error" });
    }

    const json = await completion.json();
    const content = json.choices?.[0]?.message?.content || "{}";

    let parsed: any;
    try {
      parsed = JSON.parse(content);
    } catch {
      const match = content.match(/\{[\s\S]*\}/);
      parsed = match ? JSON.parse(match[0]) : {};
    }

    const hook = parsed.hook || "";
    const body = parsed.body || "";
    const cta = parsed.cta || "";

    const text = [hook, body, cta].filter(Boolean).join("\n\n");

    const imagePrompt =
      parsed.visualDescription ||
      "Digital marketing scene, analytics dashboard, creator working on laptop, clean modern style.";

    const hashtags = Array.isArray(parsed.hashtags)
      ? parsed.hashtags
      : ["viralobby", "ai", "digitalmarketing", "contentcreator"];

    return res.status(200).json({
      text,
      imagePrompt,
      hashtags
    });
  } catch (err) {
    console.error("Error calling OpenAI:", err);
    return res.status(500).json({ error: "Internal server error" });
  }
}
