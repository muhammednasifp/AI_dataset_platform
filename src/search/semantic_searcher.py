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
from src.rag.context_builder import ContextBuilder
from src.rag.prompt_builder import PromptBuilder

import logging

logger = logging.getLogger(__name__)

class SemanticSearcher:
    
    def __init__(self,embedder,embedding_store,chunk_store):

        self.embedder=embedder
        self.embedding_store=embedding_store
        self.chunk_store=chunk_store

    def search(self,question):

        logger.info("Semantic search started")

        query_vector=self.embedder.query_embed_generator(question)

        logger.info("Query embedding generated")

        embeddings=self.embedding_store.read_all()
        if not embeddings:
            logger.warning("No embeddings found in embedding store")
            return []

        logger.info("Loaded %d embeddings", len(embeddings))

        results=[]
        similarity=0
        for embedding in embeddings:
            
            record={}
            logger.info("Calculating similarity scores")

            similarity=cosine_similarity(
                query_vector,
                embedding.vector
            )

            record["chunk"]=embedding.chunk_id
            record["score"]=similarity

            results.append(record)
        
        
        ranked=sorted(
            results,
            key=lambda item:item["score"],
            reverse=True
        )
        logger.info(
            "Ranked %d chunks by similarity",
            len(results)
        )

        top_results=ranked[:3]
        logger.info(
            "Selected top %d chunks",
            len(top_results)
        )

        chunks=self.chunk_store.read_all()
        logger.info("Loaded %d chunks", len(chunks))


        chunk_map = {chunk.id: chunk for chunk in chunks}

        list_chunk = []

        for result in top_results:
            chunk = chunk_map.get(result["chunk"])
            if chunk:
                list_chunk.append(chunk)

        if not list_chunk:
            logger.warning("Semantic search returned no matching chunks")
            
        logger.info(
            "Semantic search completed (%d chunks returned)",
            len(list_chunk)
        )
        return list_chunk

                
# embedder=EmbeddingGenerator()
# embedding_store=JSONLStore(
#     "data/processed/embeddings.jsonl",
#     model_class=Embedding
# )
# chunk_store=JSONLStore("data/processed/chunks.jsonl",model_class=Chunk)
# context_builder=ContextBuilder()
# prompt_builder=PromptBuilder()
# searcher=SemanticSearcher(
#         embedder=embedder,
#         embedding_store=embedding_store,
#         chunk_store=chunk_store
# )

# question="what is python"
# results = searcher.search(
#     question=question
# )


# context=context_builder.build(results)
# prompt=prompt_builder.build(context=context,question=question)
                
        
    
        

