import requests
def fb_post_photo(page_id:str, page_token:str, message:str|None, image_url:str):
    url=f'https://graph.facebook.com/{page_id}/photos'
    data={'url':image_url,'caption':message or '','published':'true','access_token':page_token}
    return requests.post(url,data=data,timeout=30).json()
def fb_post_video(page_id:str, page_token:str, description:str|None, video_url:str):
    url=f'https://graph.facebook.com/{page_id}/videos'
    data={'file_url':video_url,'description':description or '','access_token':page_token}
    return requests.post(url,data=data,timeout=120).json()
def ig_publish_single(ig_business_id:str, page_token:str, caption:str|None, image_url:str):
    create=requests.post(f'https://graph.facebook.com/v19.0/{ig_business_id}/media',data={'image_url':image_url,'caption':caption or '','access_token':page_token},timeout=30).json()
    if 'id' not in create: return {'step':'create','error':create}
    publish=requests.post(f'https://graph.facebook.com/v19.0/{ig_business_id}/media_publish',data={'creation_id':create['id'],'access_token':page_token},timeout=30).json()
    return {'create':create,'publish':publish}
def ig_publish_carousel(ig_business_id:str, page_token:str, caption:str|None, image_urls:list[str]):
    children=[]
    for u in image_urls:
        r=requests.post(f'https://graph.facebook.com/v19.0/{ig_business_id}/media',data={'image_url':u,'is_carousel_item':'true','access_token':page_token},timeout=30).json()
        if 'id' not in r: return {'step':'child','error':r}
        children.append(r['id'])
    create=requests.post(f'https://graph.facebook.com/v19.0/{ig_business_id}/media',data={'caption':caption or '','children':','.join(children),'media_type':'CAROUSEL','access_token':page_token},timeout=30).json()
    if 'id' not in create: return {'step':'create','error':create}
    publish=requests.post(f'https://graph.facebook.com/v19.0/{ig_business_id}/media_publish',data={'creation_id':create['id'],'access_token':page_token},timeout=30).json()
    return {'children':children,'create':create,'publish':publish}
