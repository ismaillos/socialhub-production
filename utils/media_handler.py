
import aiohttp
import os

async def post_to_facebook(token, message, media_file):
    # Replace PAGE_ID with actual page ID from user data
    page_id = 'YOUR_PAGE_ID'  # To be dynamically managed per user

    upload_url = f'https://graph.facebook.com/v18.0/{page_id}/photos'

    data = aiohttp.FormData()
    data.add_field('caption', message)
    data.add_field('access_token', token['access_token'])
    if media_file:
        data.add_field('source', media_file.file, filename=media_file.filename, content_type=media_file.content_type)

    async with aiohttp.ClientSession() as session:
        async with session.post(upload_url, data=data) as resp:
            return await resp.json()
