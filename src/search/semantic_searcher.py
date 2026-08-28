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
from src.models.search_result import SearchResult
from src.search.faiss_index import FAISSIndex
import logging

logger = logging.getLogger(__name__)

class SemanticSearcher:
    
    def __init__(self,
                 embedder,
                 embedding_store,
                 chunk_store,
                 top_k,
                 threshold,
                 faiss_index_path,
                 faiss_mapping_path

    ):

        self.embedder=embedder
        self.embedding_store=embedding_store
        self.chunk_store=chunk_store
        self.top_k=top_k
        self.threshold=threshold
        self.faiss_index_path=faiss_index_path
        self.faiss_mapping_path=faiss_mapping_path

        self.faiss_index = FAISSIndex()

    def search(self,question):

        logger.info("Semantic search started")

        query_vector=self.embedder.query_embed_generator(question)

        logger.info("Query embedding generated")

        # if not embeddings:
        #     logger.warning("No embeddings found in embedding store")
        #     return []   

        # logger.info("Loaded %d embeddings", len(embeddings))

        # #FAISS
        # dimension=len(embeddings[0].vector)

        # faiss_index=FAISSIndex(dimension=dimension)

        # faiss_index.build(embeddings=embeddings)

        self.faiss_index.load(
            index_path=self.faiss_index_path,
            mapping_path=self.faiss_mapping_path
        )

        results=self.faiss_index.search(
            query_vector=query_vector,
            top_k=self.top_k
        )

        results=[
            result
            for result in results
            if result["score"]>=self.threshold
        ]

        #Normal searching

        # results=[]
        # similarity=0
        # for embedding in embeddings:
            
        #     record={}
        #     logger.info("Calculating similarity scores")

        #     similarity=cosine_similarity(
        #         query_vector,
        #         embedding.vector
        #     )

        #     record["chunk"]=embedding.chunk_id
        #     record["score"]=similarity

        #     results.append(record)
    
        # ranked=sorted(
        #     results,
        #     key=lambda item:item["score"],
        #     reverse=True
        # )
        # logger.info(
        #     "Ranked %d chunks by similarity",
        #     len(results)
        # )

        # filtered_result=[
        #     result
        #     for result in ranked
        #     if result["score"] >= self.threshold
        # ]

        # top_results=filtered_result[:self.top_k]

        # logger.info(
        #     "Retrieved %d chunks after threshold filtering",
        #     len(top_results)
        # )


        chunks=self.chunk_store.read_all()

        logger.info("Loaded %d chunks", len(chunks))

        chunk_map = {chunk.id: chunk for chunk in chunks}

        retrieved_chunks = []

        for result in results:
            chunk = chunk_map.get(result["chunk"])
            if chunk:
                retrieved_chunks.append(
                    SearchResult(
                        chunk=chunk,
                        score=result["score"]
                    )
                )

        if not retrieved_chunks:
            logger.warning("Semantic search returned no matching chunks")
            return []
            
        logger.info(
            "Semantic search completed (%d chunks returned)",
            len(retrieved_chunks)
        )

        return retrieved_chunks 

                
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
                
        
    
        

