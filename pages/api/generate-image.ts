
import type { NextApiRequest, NextApiResponse } from "next";

type Data = { imageUrl: string } | { error: string; details?: string };

export default async function handler(req: NextApiRequest, res: NextApiResponse<Data>) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed, use POST" });
  }

  const { prompt } = req.body || {};
  if (!prompt || typeof prompt !== "string") {
    return res.status(400).json({ error: "Missing prompt in body" });
  }

  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) {
    console.error("❌ OPENAI_API_KEY is missing");
    return res.status(500).json({ error: "Server configuration error", details: "OPENAI_API_KEY is not set" });
  }

  try {
    const response = await fetch("https://api.openai.com/v1/images/generations", {
      method: "POST",
      headers: { Authorization: `Bearer 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`, "Content-Type": "application/json" },
      body: JSON.stringify({ model: "gpt-image-1", prompt, n: 1, size: "1024x1024" })
    });

    if (!response.ok) {
      const txt = await response.text();
      console.error("❌ OpenAI image error:", txt);
      return res.status(500).json({ error: "OpenAI image API error", details: txt });
    }

    const json = await response.json();
    const imageUrl = json?.data?.[0]?.url;
    if (!imageUrl) {
      console.error("❌ No image URL in response:", json);
      return res.status(500).json({ error: "No image URL returned by OpenAI" });
    }

    return res.status(200).json({ imageUrl });
  } catch (err:any) {
    console.error("❌ Image generation error:", err);
    return res.status(500).json({ error: "Internal server error", details: err?.message || "Unknown error" });
  }
}
