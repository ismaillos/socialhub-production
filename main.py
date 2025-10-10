
import os
import uvicorn
from fastapi import FastAPI, Request, UploadFile, Form
from auth import facebook
from utils.media_handler import post_to_facebook

app = FastAPI()

@app.get("/auth/facebook")
async def login(request: Request):
    return await facebook.facebook_login(request)

@app.get("/auth/facebook/callback")
async def callback(request: Request):
    token, user = await facebook.facebook_callback(request)
    return {"token": token, "user": user}

@app.post("/post/facebook")
async def fb_post(token: str = Form(...), message: str = Form(...), media: UploadFile = None):
    return await post_to_facebook(eval(token), message, media)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
