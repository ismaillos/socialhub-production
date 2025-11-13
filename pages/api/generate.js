
export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }
  const { contentType, platformId, topic, audience, tone, language, keywords } = req.body || {};
  if (!topic) {
    return res.status(400).json({ error: "Missing topic" });
  }
  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) {
    return res.status(500).json({ error: "Server misconfigured: OPENAI_API_KEY missing" });
  }

  const userPrompt = `You are an expert in viral short-form content.
Create content for type: ${contentType} and platform: ${platformId}.
Language: ${language}.
Idea / hook: ${topic}
Audience: ${audience || "general"}
Tone of voice: ${tone || "Friendly"}
Extra keywords: ${keywords || "none"}

Return ONLY valid JSON like:
{
  "title": "Short hook under 80 characters",
  "body": "Full text or script, ready to paste.",
  "hashtags": ["max","8","hashtags","without","#"],
  "imagePrompt": "short description for AI image generator (no text in image)",
  "videoPrompt": "prompt to generate a 10-15s vertical video in Veo2/3, including camera moves and scenes."
}`;

  try {
    const completion = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${apiKey}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model: "gpt-4o-mini",
        temperature: 0.95,
        messages: [
          { role: "system", content: "You generate only JSON for a content creation app. No explanation, no markdown." },
          { role: "user", content: userPrompt }
        ]
      })
    });

    if (!completion.ok) {
      const txt = await completion.text();
      console.error("OpenAI error:", txt);
      return res.status(500).json({ error: "OpenAI API error" });
    }

    const json = await completion.json();
    const raw = json.choices?.[0]?.message?.content || "{}";
    let parsed;
    try {
      parsed = JSON.parse(raw);
    } catch (e) {
      const match = raw.match(/\{[\s\S]*\}/);
      parsed = match ? JSON.parse(match[0]) : {};
    }

    const title = parsed.title || "";
    const body = parsed.body || "";
    const hashtags = Array.isArray(parsed.hashtags) ? parsed.hashtags : [];
    const imagePrompt = parsed.imagePrompt || `Clean visual for ${platformId}, no text on image, about: ${topic}`;
    const videoPrompt = parsed.videoPrompt || "";

    return res.status(200).json({ title, body, hashtags, imagePrompt, videoPrompt });
  } catch (err) {
    console.error("Error calling OpenAI:", err);
    return res.status(500).json({ error: "Internal server error" });
  }
}
