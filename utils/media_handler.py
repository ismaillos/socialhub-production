
import aiohttp

async def post_to_facebook(token, message, media_file):
    url = "https://graph.facebook.com/v18.0/me/photos"
    data = aiohttp.FormData()
    data.add_field('caption', message)
    data.add_field('access_token', token)
    if media_file:
        data.add_field('source', media_file.file, filename=media_file.filename, content_type=media_file.content_type)

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as resp:
            return await resp.json()

async def post_to_instagram(token, message, media_file):
    # This would normally require a container creation + publish
    return {"status": "stub", "platform": "instagram", "note": "Instagram API requires container flow"}

async def post_to_tiktok(token, message, media_file):
    return {"status": "stub", "platform": "tiktok", "note": "Requires TikTok OpenAPI and client credentials"}

async def post_to_youtube(token, message, media_file):
    # Upload a video via YouTube Data API (multipart)
    url = "https://www.googleapis.com/upload/youtube/v3/videos?part=snippet,status"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    metadata = {
        "snippet": {
            "title": message,
            "description": message,
            "tags": ["upload", "api"]
        },
        "status": {
            "privacyStatus": "unlisted"
        }
    }

    data = aiohttp.FormData()
    data.add_field('snippet', str(metadata["snippet"]))
    data.add_field('status', str(metadata["status"]))
    if media_file:
        data.add_field('video', media_file.file, filename=media_file.filename, content_type=media_file.content_type)

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data, headers=headers) as resp:
            return await resp.json()
