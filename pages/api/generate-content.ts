
import type { NextApiRequest, NextApiResponse } from "next";

type Success = {
  title: string;
  intro: string;
  body: string;
  outro: string;
  hashtags: string[];
};

type ErrorRes = { error: string };

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Success | ErrorRes>
) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { contentType, topic, keywords, audience, tone } = req.body || {};

  if (!topic || typeof topic !== "string") {
    return res.status(400).json({ error: "Missing topic / prompt." });
  }

  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) {
    return res
      .status(500)
      .json({ error: "Server misconfigured: OPENAI_API_KEY missing." });
  }

  const userPrompt = `
You are an expert AI copywriter for ${contentType || "social content"}.
Generate content in English with:
- A clear, catchy title
- A short intro paragraph
- A main body (2–4 short paragraphs or bullet points)
- A short outro with a call to action
- Up to 8 relevant hashtags (without # symbol)

Context:
- Topic / prompt: ${topic}
- Keywords: ${keywords || "none"}
- Audience: ${audience || "general"}
- Tone of voice: ${tone || "Professional"}

Return ONLY valid JSON with this shape:
{
  "title": "short title",
  "intro": "one short intro paragraph",
  "body": "main content",
  "outro": "short closing paragraph",
  "hashtags": ["tag1","tag2","tag3"]
}
`.trim();

  try {
    const openaiRes = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model: "gpt-4o-mini",
        temperature: 0.9,
        messages: [
          {
            role: "system",
            content: "You are a JSON-only API. Always respond with strictly valid JSON and nothing else."
          },
          { role: "user", content: userPrompt }
        ]
      })
    });

    if (!openaiRes.ok) {
      const text = await openaiRes.text();
      console.error("OpenAI error:", text);
      return res.status(500).json({ error: "OpenAI API error." });
    }

    const json = await openaiRes.json();
    const content = json.choices?.[0]?.message?.content ?? "{}";

    let parsed: any;
    try {
      parsed = JSON.parse(content);
    } catch {
      const match = content.match(/\{[\s\S]*\}/);
      parsed = match ? JSON.parse(match[0]) : {};
    }

    return res.status(200).json({
      title: parsed.title ?? "",
      intro: parsed.intro ?? "",
      body: parsed.body ?? "",
      outro: parsed.outro ?? "",
      hashtags: Array.isArray(parsed.hashtags) ? parsed.hashtags : []
    });
  } catch (err) {
    console.error("Generate-content API error:", err);
    return res.status(500).json({ error: "Internal server error." });
  }
}
