
from dataclasses import dataclass

@dataclass
class Config:
    #STORAGE
    jsonl_path:str="data/raw/documents.jsonl"
    parquet_path:str="data/processed/documents.parquet"
    chunk_path:str="data/processed/chunks.jsonl"
    embedding_path:str="data/processed/embeddings.jsonl"
    version_path:str="data/versions/"
    faiss_index_path:str="data/processed/faiss.index"
    faiss_mapping_path = "data/processed/faiss_chunk_ids.json"

    #CHUNKING
    chunk_size:int=200

    #MODELS
    ollama_model:str="phi3"
    embedding_model:str="all-MiniLM-L6-v2"

    #VALUES
    top_k:int=5
    retrieval_threshold = 0.40
    validation_threshold:int=100


