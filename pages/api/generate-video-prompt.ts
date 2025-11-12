
import type { NextApiRequest, NextApiResponse } from "next";
type Data = { prompt: string } | { error: string; details?: string };
export default async function handler(req: NextApiRequest, res: NextApiResponse<Data>) {
  if (req.method !== "POST") return res.status(405).json({ error: "Method not allowed" });
  const { script, theme, tone } = req.body || {};
  if (!script || typeof script !== "string") return res.status(400).json({ error: "Missing 'script' in body" });
  const prompt = `GOAL: Generate a short vertical video (9:16) optimized for TikTok/Reels/Shorts.
STYLE: Theme=${theme||"marketing"}, Tone=${tone||"inspirant"}, modern Moroccan creative studio vibe, high contrast lighting.
TECH: Aspect 9:16, Duration 10–15s, mp4/webm, safe top area for title and lower area for hashtags (no burned text).
SCRIPT:
${script}
SCENES:
1) 1–3s: Establishing shot (creative workspace / Casablanca)
2) 3–8s: Close-ups of hands/laptop/phone, AI workflow
3) 8–12s: Productivity visuals (charts, satisfied users)
4) 12–15s: Outro with subtle movement
CAMERA: smooth dolly, shallow DOF. COLOR: neutral + violet/teal accents.`;
  return res.status(200).json({ prompt });
}
