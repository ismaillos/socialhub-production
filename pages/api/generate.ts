
import type { NextApiRequest, NextApiResponse } from "next";

type Data = { text: string; imagePrompt: string; hashtags: string[]; };

export default async function handler(req: NextApiRequest, res: NextApiResponse<Data | { error: string }>) {
  if(req.method!=="POST"){ return res.status(405).json({ error:"Method not allowed" }); }
  const { contentType, language, theme, tone, idea } = req.body||{};
  if(!idea || typeof idea!=="string"){ return res.status(400).json({ error:"Missing idea" }); }

  const apiKey = process.env.OPENAI_API_KEY;
  if(!apiKey){ return res.status(500).json({ error:"Missing OPENAI_API_KEY env var" }); }

  let langLabel = "French"; if(language==="EN") langLabel="English"; if(language==="AR") langLabel="Modern Standard Arabic";
  const typeLabel = contentType==="carousel" ? "carousel (sequence of image + text slides)"
    : contentType==="video" ? "short video script (Reel/TikTok)"
    : "image + text social post";

  const systemPrompt = `
Type: ${typeLabel}
Language: ${langLabel}
Theme: ${theme}
Tone: ${tone}
Idea: "${idea}"
Return ONLY strict JSON:
{
  "hook": "short hook",
  "body": "2-6 short sentences (or 3-6 slides)",
  "cta": "call to action",
  "visualDescription": "clean visual description for an image model",
  "hashtags": ["word1","word2","... up to 8"]
}`.trim();

  try{
    const completion = await fetch("https://api.openai.com/v1/chat/completions",{
      method:"POST",
      headers:{ Authorization:`Bearer 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`, "Content-Type":"application/json" },
      body: JSON.stringify({
        model: "gpt-4o-mini",
        messages: [
          { role:"system", content: "You are a top-tier social media content strategist." },
          { role:"user", content: systemPrompt }
        ],
        temperature: 0.9
      })
    });

    if(!completion.ok){ const err = await completion.text(); console.error("OpenAI error:", err); return res.status(500).json({ error:"OpenAI API error" }); }

    const json = await completion.json();
    const content = json.choices?.[0]?.message?.content || "{}";

    let parsed:any;
    try{ parsed = JSON.parse(content); }
    catch{ const match = content.match(/\{[\s\S]*\}/); parsed = match? JSON.parse(match[0]) : {}; }

    const hook = parsed.hook || "";
    const body = parsed.body || "";
    const cta = parsed.cta || "";
    const text = [hook, body, cta].filter(Boolean).join("\n\n");
    const imagePrompt = parsed.visualDescription || "Digital marketing scene, creator working, clean modern style.";
    const hashtags = Array.isArray(parsed.hashtags)? parsed.hashtags : ["viralobby","ai","digitalmarketing","contentcreator"];

    return res.status(200).json({ text, imagePrompt, hashtags });
  }catch(err){
    console.error("Error calling OpenAI:", err);
    return res.status(500).json({ error:"Internal server error" });
  }
}
