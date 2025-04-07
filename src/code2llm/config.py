# src/code2llm/config.py
from pydantic import BaseModel
from typing import Optional


class VectorDBConfig(BaseModel):
    db_type: str = "elasticsearch"  # 允许选择数据库类型：elasticsearch, faiss, chroma
    es_host: Optional[str] = "http://localhost:9200"
    index_name: str = "code_embeddings"
    embedding_model: str = "all-MiniLM-L6-v2"
    embedding_field: str = "embedding"

    faiss_index_path: Optional[str] = "data/faiss.index"  # FAISS存储路径
    chroma_db_path: Optional[str] = "data/chroma"  # ChromaDB 存储路径
