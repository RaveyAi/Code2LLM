# src/code2llm/services/base_vector_db.py
from abc import ABC, abstractmethod
from typing import List, Dict

class BaseVectorDatabase(ABC):
    """向量数据库抽象基类"""

    @abstractmethod
    def delete_by_repo(self, repo_name: str) -> int:
        """删除指定仓库的所有数据"""
        pass

    @abstractmethod
    def upsert_chunks(self, chunks: List[Dict]) -> int:
        """插入或更新代码块"""
        pass

    @abstractmethod
    def semantic_search(self, query: str, top_k: int = 5) -> List[Dict]:
        """执行语义搜索"""
        pass
