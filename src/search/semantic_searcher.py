# Semantic Search
#
# Retrieves chunks based on meaning
# rather than exact keyword matching.
#
# Uses embeddings and similarity scores.
from src.models.embedding import Embedding
from src.models.chunk import Chunk
from src.embedders.embedding_generator import EmbeddingGenerator
from src.storage.jsonl_store import JSONLStore
from src.utils.similarity import cosine_similarity

class SemanticSearcher:
    
    def __init__(self,embedder,embedding_store,chunk_store):

        self.embedder=embedder
        self.embedding_store=embedding_store
        self.chunk_store=chunk_store

    def search(self,question):


        query_vector=self.embedder.query_embed_generator(question)

        embeddings=self.embedding_store.read_all()

        best_score=-1
        best_chunk_id=None
        similarity=0
        for embedding in embeddings:

            similarity=cosine_similarity(
                query_vector,
                embedding.vector
            )

            if similarity>best_score:
                best_score=similarity
                best_chunk_id=embedding.chunk_id
        
        chunks=self.chunk_store.read_all()

        chunk_content=''
        for chunk in chunks:
            if best_chunk_id==chunk.id:
                chunk_content=chunk.content
                break
    
        
        return chunk
    
embedder=EmbeddingGenerator()
embedding_store=JSONLStore("data/processed/embeddings.jsonl",model_class=Embedding)
chunk_store=JSONLStore("data/processed/chunks.jsonl",model_class=Chunk)

search=SemanticSearcher(
            embedder=embedder,
            embedding_store=embedding_store,
            chunk_store=chunk_store
            )

search.search("what is python")


                
        
    
        

