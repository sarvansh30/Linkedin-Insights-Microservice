from pydantic import BaseModel
from datetime import datetime
from typing import List,Optional

class Comment(BaseModel):
    comment_id:str
    user_id:str
    content:str


class Post(BaseModel):
    likes:int
    comments:list[Comment]
    content:str


class Page(BaseModel):
    page_id:str
    title:str
    url:str
    description:str
    profile_picture:Optional[str] =None
    followers: int
    website: Optional[str]=None
    industry:Optional[str]=None
    headcount:Optional[int]=None
    posts: Optional[List[Post]] =None
    scraped_at: datetime
    
class PageSummary(BaseModel):
    title: str
    profile_picture: Optional[str] = None
    description: Optional[str] = None
    followers: int