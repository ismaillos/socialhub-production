
export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }
  const { topic } = req.body || {};
  if (!topic) {
    return res.status(400).json({ error: "Missing topic" });
  }
  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) {
    return res.status(500).json({ error: "Server misconfigured: OPENAI_API_KEY missing" });
  }

  const userPrompt = `Generate a short social media caption and 5 hashtags for: ${topic}. Return JSON { "title": "...", "body": "...", "hashtags": ["..."] }`;

  try {
    const completion = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${apiKey}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model: "gpt-4o-mini",
        messages: [
          { role: "system", content: "You output only JSON, no explanation." },
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
    } catch {
      const match = raw.match(/\{[\s\S]*\}/);
      parsed = match ? JSON.parse(match[0]) : {};
    }

    return res.status(200).json(parsed);
  } catch (err) {
    console.error("Error calling OpenAI:", err);
    return res.status(500).json({ error: "Internal server error" });
  }
}
