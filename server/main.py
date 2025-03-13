import json
from fastapi import FastAPI, HTTPException
from modelClasses import Page, PageSummary
from database import pages_collection
from bson import ObjectId
from scraper import linkedin_scraper
from typing import Optional, List
import redis
from ai_summary import generate_company_summary

app = FastAPI(title="Linkedin insights microservice")

redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

CACHE_EXPIRE_SECONDS = 360 

@app.get('/pages/{page_id}', response_model=Page)
async def get_page(page_id: str):
    cache_key = f"page:{page_id}"
    cached_page = redis_client.get(cache_key)
    if cached_page:
        print("cache hit")
        return json.loads(cached_page)
    
    page = pages_collection.find_one({"page_id": page_id})
    if page is not None:
        page.pop("_id", None)
        redis_client.setex(cache_key, CACHE_EXPIRE_SECONDS, json.dumps(page, default=str))
        return page

    try:
        page_data = linkedin_scraper(page_id)
        if page_data:
            pages_collection.insert_one(page_data)
            redis_client.setex(cache_key, CACHE_EXPIRE_SECONDS, json.dumps(page_data, default=str))
            return page_data
        else:
            raise HTTPException(status_code=404, detail="Page not found")
    except Exception as e:
        if "Page not found" in str(e):
            raise HTTPException(status_code=404, detail="Page not found")
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")

@app.get("/pages", response_model=List[PageSummary])
async def find_pages(
    name: Optional[str] = None,
    industry: Optional[str] = None,
    min_followers: Optional[int] = None,
    max_followers: Optional[int] = None,
    limit: int = 10,
    offset: int = 0
):
    query = {}
    if name:
        query["title"] = {"$regex": name, "$options": "i"}
    if industry:
        query["industry"] = industry
    if min_followers is not None or max_followers is not None:
        query["followers"] = {}
        if min_followers is not None:
            query["followers"]["$gte"] = min_followers
        if max_followers is not None:
            query["followers"]["$lte"] = max_followers
    pages_cursor = (
        pages_collection.find(query, {"posts": 0, "last_scraped": 0})
        .sort("followers", -1)
        .skip(offset)
        .limit(limit)
    )
    pages = []
    for page in pages_cursor:
        page["_id"] = str(page["_id"])
        if "followers" in page:
            if isinstance(page["followers"], str):
                try:
                    page["followers"] = int(page["followers"].replace(",", ""))
                except ValueError:
                    page["followers"] = 0
            elif page["followers"] is None:
                page["followers"] = 0
        pages.append(page)
    return pages

@app.get('/ai-summary/{page_id}')
async def ai_summary(page_id: str):
    cache_key = f"ai-summary:{page_id}"
    cached_summary = redis_client.get(cache_key)
    if cached_summary:
        return json.loads(cached_summary)
    
    company_data = pages_collection.find_one({"page_id": page_id})
    if not company_data:
        raise HTTPException(status_code=404, detail="Page not found")
    company_data.pop("_id", None)
    
    try:
        summary_response = generate_company_summary(company_data)
        redis_client.setex(cache_key, CACHE_EXPIRE_SECONDS, json.dumps(summary_response, default=str))
        return summary_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summary generation failed: {str(e)}")
