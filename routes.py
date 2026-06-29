from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import ArticleSchema, UpdateArticleModel, LoginRequest
from database import article_collection, user_collection
import bcrypt

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
from bson.objectid import ObjectId

router = APIRouter()

def article_helper(article) -> dict:
    return {
        "id": str(article["_id"]),
        "title": article["title"],
        "summary": article.get("summary", ""),
        "content": article["content"],
        "category": article["category"],
        "image_url": article.get("image_url", ""),
        "keywords": article.get("keywords", []),
        "is_published": article.get("is_published", True),
        "created_at": article.get("created_at")
    }

@router.post("/login", response_description="Admin login")
async def login(req: LoginRequest = Body(...)):
    user = await user_collection.find_one({"username": req.username})
    if user and verify_password(req.password, user["password"]):
        return {"token": f"token_for_{user['username']}"}
    raise HTTPException(status_code=401, detail="Sai tên đăng nhập hoặc mật khẩu")

@router.get("", response_description="Get all articles")
async def get_articles(category: str = None, search: str = None):
    print("category", category)
    print("search", search)

    query = {}
    if category:
        query["category"] = category
    if search:
        query["title"] = {"$regex": search, "$options": "i"}
        
    articles = []
    async for article in article_collection.find(query).sort("created_at", -1):
        articles.append(article_helper(article))
    return articles

@router.get("/{id}", response_description="Get a single article")
async def get_article(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    article = await article_collection.find_one({"_id": ObjectId(id)})
    if not article:
        article = await article_collection.find_one({"_id": id})
    if article:
        return article_helper(article)
    raise HTTPException(status_code=404, detail="Article not found")

@router.post("", response_description="Add new article")
async def add_article(article: ArticleSchema = Body(...)):
    article_dict = article.model_dump(by_alias=True)
    if "_id" in article_dict:
        del article_dict["_id"]
    
    new_article = await article_collection.insert_one(article_dict)
    created_article = await article_collection.find_one({"_id": new_article.inserted_id})
    return article_helper(created_article)

@router.put("/{id}", response_description="Update an article")
async def update_article(id: str, req: UpdateArticleModel = Body(...)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    req = {k: v for k, v in req.model_dump().items() if v is not None}
    
    if len(req) >= 1:
        update_result = await article_collection.update_one({"_id": ObjectId(id)}, {"$set": req})
        if update_result.matched_count == 0:
            update_result = await article_collection.update_one({"_id": id}, {"$set": req})
            
        if update_result.modified_count == 1 or update_result.matched_count == 1:
            updated_article = await article_collection.find_one({"_id": ObjectId(id)}) or await article_collection.find_one({"_id": id})
            if updated_article:
                return article_helper(updated_article)
                
    existing_article = await article_collection.find_one({"_id": ObjectId(id)}) or await article_collection.find_one({"_id": id})
    if existing_article:
        return article_helper(existing_article)
    raise HTTPException(status_code=404, detail="Article not found")

@router.delete("/{id}", response_description="Delete an article")
async def delete_article(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    delete_result = await article_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return {"message": "Article deleted successfully"}
        
    delete_result = await article_collection.delete_one({"_id": id})
    if delete_result.deleted_count == 1:
        return {"message": "Article deleted successfully"}
        
    raise HTTPException(status_code=404, detail="Article not found")
