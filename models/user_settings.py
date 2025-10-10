
from sqlmodel import SQLModel, Field
from typing import Optional

class UserSettings(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    facebook_token: Optional[str]
    instagram_token: Optional[str]
    youtube_token: Optional[str]
    tiktok_token: Optional[str]
    n8n_webhook_url: Optional[str]
    encrypted: bool = True
