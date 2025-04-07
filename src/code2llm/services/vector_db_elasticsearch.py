# src/code2llm/services/vector_db_elasticsearch.py
from typing import List, Dict

from elasticsearch import Elasticsearch, helpers
from sentence_transformers import SentenceTransformer
from src.code2llm.services.base_vector_db import BaseVectorDatabase
from src.code2llm.config import VectorDBConfig
import logging

class ElasticsearchVectorDB(BaseVectorDatabase):
    def __init__(self, config: VectorDBConfig):
        self.config = config
        self.es = Elasticsearch([config.es_host])
        self.embedder = SentenceTransformer(config.embedding_model)
        self.index = config.index_name
        self.logger = logging.getLogger("code2llm.elasticsearch")

    def delete_by_repo(self, repo_name: str) -> int:
        """删除 Elasticsearch 数据"""
        response = self.es.delete_by_query(
            index=self.index,
            body={"query": {"term": {"metadata.repo": repo_name}}}
        )
        return response.get("deleted", 0)

    def upsert_chunks(self, chunks: List[Dict]) -> int:
        """向 Elasticsearch 插入数据"""
        embeddings = self.embedder.encode([c["content"] for c in chunks], convert_to_numpy=True)
        actions = [
            {"_op_type": "index", "_index": self.index, "_source": {**chunk, self.config.embedding_field: embedding.tolist()}}
            for chunk, embedding in zip(chunks, embeddings)
        ]
        helpers.bulk(self.es, actions)
        return len(actions)

    def semantic_search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Elasticsearch 语义搜索"""
        query_embedding = self.embedder.encode(query).tolist()
        response = self.es.search(index=self.index, size=top_k, query={
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": f"cosineSimilarity(params.query_vector, '{self.config.embedding_field}') + 1.0",
                    "params": {"query_vector": query_embedding}
                }
            }
        })
        return [{"content": hit["_source"]["content"], "metadata": hit["_source"]["metadata"]} for hit in response["hits"]["hits"]]
