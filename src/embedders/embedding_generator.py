# Embedding Generation
#
# Converts text chunks into numerical vectors.
#
# Why?
# Computers cannot understand raw text semantically.
# Embeddings transform text into numbers that capture meaning.
#
# Example:
# "Python decorators modify function behavior"
#
# ↓
#
# [0.12, -0.45, 0.89, ...]
#
# Uses:
# - Semantic Search
# - Similarity Search
# - Vector Databases
# - RAG Systems
#
# Pipeline:
#
# Chunk
#   ↓
# Embedding Generator
#   ↓
# Embedding Object
#   ↓
# embeddings.jsonl
from src.exceptions.embedding import EmbeddingError
from src.models.embedding import Embedding
from sentence_transformers import SentenceTransformer
from src.storage.jsonl_store import JSONLStore
from src.models.chunk import Chunk

import logging

logger=logging.getLogger(__name__)

class EmbeddingGenerator:

    def __init__(self,embedding_model):
        logger.info("Loading embedding model: %s", embedding_model)
        try:
    
            self.model=SentenceTransformer(embedding_model)
            logger.info("Embedding model loaded successfully")
        except Exception as e:
            logger.exception("Failed to load embedding model")
            raise EmbeddingError("Unable to load embedding model.") from e

    def generate(self, chunk):

        logger.info(
            "Generating embedding for chunk (id=%s)",
            chunk.id
        )
        # generate()
        #
        # Converts a Chunk into an Embedding.
        #
        # Steps:
        # 1. Read chunk content.
        # 2. Generate vector using MiniLM.
        # 3. Convert vector to Python list.
        # 4. Create Embedding object.
        # 5. Return Embedding.

        return Embedding(
            chunk_id=chunk.id,
            vector=self.model.encode(chunk.content).tolist()
        )
    
    def query_embed_generator(self,query):

        logger.info("Generating query embedding")

        vector=self.model.encode(query).tolist()

        logger.info(
            "Query embedding generated (dimensions=%d)",
            len(vector)
        )
        
        return vector

# chunk_store=JSONLStore("data/processed/chunks.jsonl",model_class=Chunk)
# chunks = chunk_store.read_all()
# config=Config()
# embedding_store=JSONLStore(config.embedding_path,model_class=Embedding)
# generator=EmbeddingGenerator(config.embedding_model)
#  # for chunk in chunks:
#  #     embedding = generator.generate(chunk)
#  #     embedding_store.save_one(embedding)

# embeddings = embedding_store.read_all()
# print(len(embeddings))
# # print(embeddings[0].chunk_id)
# # print(len(embeddings[0].vector))






