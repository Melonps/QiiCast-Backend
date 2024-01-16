from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi import FastAPI
from pydantic import BaseModel  # リクエストbodyを定義するために必要
from pathlib import Path
from typing import Tuple
from lib.inference.inference import InferenceEngine
from lib.interact_qiita.qiita_api import request_page
import uvicorn

# FastAPIアプリケーションの初期化
app = FastAPI()

# CORSミドルウェアの設定
origins = [
    "http://localhost:3000",
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:8502/",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# InferenceEngineの初期化
infer = InferenceEngine()
infer._initialize_processor("nobo_model")
# infer._initialize_processor("ik_model")

# ルートエンドポイントへのGETリクエストに対するハンドラ
@app.get("/")
async def get():
    """
    ダミーのハローワールドレスポンスを返すエンドポイント
    """
    return "Hello World"

# /get_article エンドポイントへのGETリクエストに対するハンドラ
@app.get("/get_article")
async def get_article(tag: str, num_articles: int = 1):
    """
    Qiitaの記事情報を取得し、推論エンジンを使用して各記事の評価を予測するエンドポイント
    :param tag: 取得したい記事のタグ
    :param num_articles: 取得する記事の数（デフォルトは1）
    :return: 記事情報と推論結果のリストをJSON形式で返す
    """
    response_data = []
    meta_data_articles = request_page(tag, num_articles)

    for each_article in meta_data_articles:
        # 推論エンジンを使用して記事の評価を予測
        inference_result = infer.predict("nobo_model", each_article)
        
        # レスポンスデータに記事情報と推論結果を追加
        response_data.append(
            {
                "title": each_article["title"],
                "url": each_article["url"],
                "rating": inference_result,
                "created_at": each_article["created_at"],
                "user": each_article["user"],
            }
        )
    return response_data
