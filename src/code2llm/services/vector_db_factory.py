# src/code2llm/services/vector_db_factory.py
from src.code2llm.config import VectorDBConfig
from src.code2llm.services.vector_db_elasticsearch import ElasticsearchVectorDB
# from src.code2llm.services.vector_db_faiss import FAISSVectorDB
def get_vector_db(config: VectorDBConfig):
    if config.db_type == "elasticsearch":
        return ElasticsearchVectorDB(config)
    elif config.db_type == "faiss":
        # return FAISSVectorDB(config)
        raise ValueError(f"不支持的数据库类型: {config.db_type}")
    else:
        raise ValueError(f"不支持的数据库类型: {config.db_type}")
