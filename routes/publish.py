import requests
from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import JSONResponse
from db.database import SessionLocal
from db.models import Token
from services.publish_meta import fb_post_photo, fb_post_video, ig_publish_single, ig_publish_carousel
from services.token_fresh import ensure_fresh
router=APIRouter(prefix='/publish', tags=['Publish'])
@router.post('/facebook')
def facebook(payload:dict=Body(...)):
    message=payload.get('message'); image_url=payload.get('image_url'); video_url=payload.get('video_url'); account_id=payload.get('account_id')
    with SessionLocal() as s:
        q=s.query(Token).filter(Token.platform=='facebook')
        if account_id: q=q.filter(Token.account_id==account_id)
        t=q.first()
        if not t or not t.page_access_token or not t.page_id: raise HTTPException(404,'Facebook page not connected')
        if image_url: return JSONResponse(fb_post_photo(t.page_id,t.page_access_token,message,image_url))
        if video_url: return JSONResponse(fb_post_video(t.page_id,t.page_access_token,message,video_url))
        raise HTTPException(400,'Provide image_url or video_url')
@router.post('/instagram')
def instagram(payload:dict=Body(...)):
    caption=payload.get('caption') or payload.get('message'); image_url=payload.get('image_url'); carousel_urls=payload.get('carousel_urls') or []; account_id=payload.get('account_id')
    with SessionLocal() as s:
        q=s.query(Token).filter(Token.platform=='instagram')
        if account_id: q=q.filter(Token.account_id==account_id)
        t=q.first()
        if not t or not t.page_access_token or not t.business_id: raise HTTPException(404,'Instagram business account not connected')
        if image_url and not carousel_urls: return JSONResponse(ig_publish_single(t.business_id,t.page_access_token,caption,image_url))
        if carousel_urls: return JSONResponse(ig_publish_carousel(t.business_id,t.page_access_token,caption,carousel_urls))
        raise HTTPException(400,'Provide image_url or carousel_urls')
@router.post('/youtube')
def youtube(payload:dict=Body(...)):
    account_id=payload.get('account_id'); title=payload.get('title'); description=payload.get('description',''); tags=payload.get('tags',[]); privacy=payload.get('privacyStatus','unlisted'); video_url=payload.get('video_url')
    if not title: raise HTTPException(400,'title is required')
    if not video_url: raise HTTPException(400,'video_url is required')
    t=ensure_fresh('youtube', account_id)
    if not t or not t.access_token: raise HTTPException(404,'YouTube account not connected or no access_token')
    try:
        vr=requests.get(video_url, timeout=120, stream=True); vr.raise_for_status(); video_bytes=vr.content
    except Exception as e: raise HTTPException(400,f'Failed to download video_url: {e}')
    meta={'snippet':{'title':title,'description':description,'tags':tags,'categoryId':'22'},'status':{'privacyStatus':privacy}}
    init_url='https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status'
    init_headers={'Authorization':f'Bearer {t.access_token}','Content-Type':'application/json; charset=UTF-8','X-Upload-Content-Length':str(len(video_bytes)),'X-Upload-Content-Type':'video/*'}
    init_res=requests.post(init_url, headers=init_headers, json=meta, timeout=60)
    if init_res.status_code not in (200,201): return JSONResponse(status_code=init_res.status_code, content={'error':init_res.text})
    upload_url=init_res.headers.get('Location')
    if not upload_url: raise HTTPException(500,'No resumable upload URL returned by YouTube')
    put_headers={'Authorization':f'Bearer {t.access_token}','Content-Length':str(len(video_bytes)),'Content-Type':'video/*'}
    put_res=requests.put(upload_url, headers=put_headers, data=video_bytes, timeout=600)
    if put_res.status_code not in (200,201): return JSONResponse(status_code=put_res.status_code, content={'error':put_res.text})
    return JSONResponse(put_res.json())
@router.post('/tiktok')
def tiktok(payload:dict=Body(...)):
    account_id=payload.get('account_id'); caption=payload.get('caption',''); video_url=payload.get('video_url')
    t=ensure_fresh('tiktok', account_id)
    if not t or not t.access_token: raise HTTPException(404,'TikTok account not connected or no access_token')
    try:
        vr=requests.get(video_url, timeout=120, stream=True); vr.raise_for_status(); video_bytes=vr.content
    except Exception as e: raise HTTPException(400,f'Failed to download video_url: {e}')
    init_url='https://open-api.tiktok.com/share/video/upload/init/'
    init_res=requests.post(init_url, headers={'Authorization':f'Bearer {t.access_token}'}, json={'source':'UPLOAD'}, timeout=30)
    if init_res.status_code!=200: return JSONResponse(status_code=init_res.status_code, content={'step':'init','error':init_res.text})
    upload_url=init_res.json().get('data',{}).get('upload_url')
    if not upload_url: return JSONResponse(status_code=500, content={'step':'init','error':'No upload_url returned'})
    files={'video':('upload.mp4', video_bytes, 'video/mp4')}
    up_res=requests.post(upload_url, files=files, timeout=600)
    if up_res.status_code!=200: return JSONResponse(status_code=up_res.status_code, content={'step':'upload','error':up_res.text})
    video_id=up_res.json().get('data',{}).get('video_id')
    if not video_id: return JSONResponse(status_code=500, content={'step':'upload','error':'No video_id returned'})
    publish_url='https://open-api.tiktok.com/share/video/publish/'
    pb_res=requests.post(publish_url, headers={'Authorization':f'Bearer {t.access_token}'}, json={'video_id':video_id,'text':caption}, timeout=30)
    if pb_res.status_code!=200: return JSONResponse(status_code=pb_res.status_code, content={'step':'publish','error':pb_res.text})
    return JSONResponse(pb_res.json())
