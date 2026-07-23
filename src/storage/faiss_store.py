# Vector Index
#
# Stores embeddings in a structure
# optimized for similarity search.
#
# Used to quickly find semantically
# similar chunks.

from src.storage.jsonl_store import JSONLStore
from src.models.embedding import Embedding
class FAISStore:

    def __init__(self):
        self.chunk_ids = []
        self.vectors=[]
    
    def build_index(self,embedding):

        for embedding in embedding:

            self.chunk_ids.append(embedding.chunk_id)
            self.vectors.append(embedding.vector)
        
        print(len(self.vectors))
        print(len(self.vectors[0]))

        
        return self
# faiss=FAISStore()


# embedding_store=JSONLStore("data/processed/embeddings.jsonl",model_class=Embedding)
# embedding=embedding_store.read_all()

# faiss.build_index(embedding=embedding)
