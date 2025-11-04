
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

  const systemPrompt = `
You are Viralobby Studio, a top-tier AI content creator specialized in AI-powered digital marketing content.

Language: ${langLabel}
Content type: ${contentType} (short video or image+text post)
Theme: ${theme}
Tone: ${tone}
User idea: "${idea}"

Return ONLY a JSON object with:
{
  "text": "full caption or video script in the target language",
  "imagePrompt": "short description of visual concept to generate",
  "hashtags": ["hashtag1","hashtag2",...]
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
          { role: "user", content: "Generate the JSON object only, no explanation." }
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

    const text = parsed.text || "No text generated.";
    const imagePrompt =
      parsed.imagePrompt ||
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
