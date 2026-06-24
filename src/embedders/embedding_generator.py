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
from src.models.embedding import Embedding
from sentence_transformers import SentenceTransformer
from src.storage.jsonl_store import JSONLStore
from src.models.chunk import Chunk

class EmbeddingGenerator:

    def __init__(self):
       self.model=SentenceTransformer("all-MiniLM-L6-v2")

    def generate(self, chunk):
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

        vector=self.model.encode(query).tolist()
        
        return vector

# chunk_store=JSONLStore("data/processed/chunks.jsonl",model_class=Chunk)
# chunks = chunk_store.read_all()

# embedding_store=JSONLStore("data/processed/embeddings.jsonl",model_class=Embedding)
# # generator=EmbeddingGenerator()
# # for chunk in chunks:
# #     embedding = generator.generate(chunk)
# #     embedding_store.save_one(embedding)

# embeddings = embedding_store.read_all()

# # print(len(embeddings))
# # print(embeddings[0].chunk_id)
# # print(len(embeddings[0].vector))






