
import type { NextApiRequest, NextApiResponse } from "next";

type Data = {
  imageUrl: string;
};

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data | { error: string }>
) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { prompt } = req.body || {};

  if (!prompt || typeof prompt !== "string") {
    return res.status(400).json({ error: "Missing prompt" });
  }

  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) {
    return res.status(500).json({ error: "Missing OPENAI_API_KEY env var" });
  }

  try {
    const response = await fetch("https://api.openai.com/v1/images/generations", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model: "gpt-image-1",
        prompt,
        n: 1,
        size: "1024x1024"
      })
    });

    if (!response.ok) {
      const txt = await response.text();
      console.error("OpenAI image error:", txt);
      return res.status(500).json({ error: "OpenAI image API error" });
    }

    const json = await response.json();
    const imageUrl = json.data?.[0]?.url;

    if (!imageUrl) {
      return res.status(500).json({ error: "No image URL returned" });
    }

    return res.status(200).json({ imageUrl });
  } catch (err) {
    console.error("Image generation error:", err);
    return res.status(500).json({ error: "Internal server error" });
  }
}
