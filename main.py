from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router as ArticleRouter

app = FastAPI(title="Tech News API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ArticleRouter, tags=["Articles"], prefix="/api/articles")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to Tech News API"}
