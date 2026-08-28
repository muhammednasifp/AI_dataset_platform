from src.search.keyword_searcher import KeywordSearcher
from src.search.semantic_searcher import SemanticSearcher
from src.storage.jsonl_store import JSONLStore
from src.models.chunk import Chunk
from src.config import Config
from src.models.embedding import Embedding
from src.models.chunk import Chunk
from src.embedders.embedding_generator import EmbeddingGenerator
from src.storage.jsonl_store import JSONLStore
from src.models.search_result import SearchResult
config=Config()

class HybridSearcher:

    def __init__(self,
        semantic_searcher,
        keyword_searcher,
        top_k
    ):
        self.semantic_searcher=semantic_searcher
        self.keyword_searcher=keyword_searcher
        self.top_k=top_k

    def search(self,question):

        semantic_results = (
            self.semantic_searcher.search(question)
        )

        keyword_results = (
            self.keyword_searcher.search(question)
        )


        semantic_results=self._normalize_scores(
            semantic_results
        )
        keyword_results=self._normalize_scores(
            keyword_results
        )

        combined=self._combine_scores(
            semantic_results,
            keyword_results
        )

        results=[]

        for chunk_id,data in combined.items():

            final_score=self._calculate_final_score(
                semantic_score=data["semantic_score"],
                keyword_score=data["keyword_score"]
            )

            results.append(
                SearchResult(
                    chunk=data["chunk"],
                    score=final_score
                )
            )

        results.sort(
            key=lambda result:result.score,
            reverse=True
        )

        return results[:self.top_k]
    
    def _normalize_scores(self,results):

        if not results:
            return []

        scores=[
            result.score
            for result in results
        ]

        min_score=min(scores)
        max_score=max(scores)

        if max_score == min_score:

            return [
                {
                    **result,
                    "normalized_score": 1.0
                }
                for result in results
            ]

        normalized_results = []

        for result in results:
            normalized_score = (
                (result.score - min_score)
                /
                (max_score - min_score)
            )

            normalized_results.append(
                (result,normalized_score)
            )

        return normalized_results   

    def _combine_scores(
        self,
        semantic_results,
        keyword_results,
    ):
        
        combined={}

        for result,normalized_score in semantic_results:

            chunk_id=result.chunk.id

            combined[chunk_id]={
                "chunk":result.chunk,
                "semantic_score":normalized_score,
                "keyword_score":0.0
            }

        for result, normalized_score in keyword_results:

            chunk_id=result.chunk.id

            if chunk_id not in combined:

                combined[chunk_id]={
                    "chunk":result.chunk,
                    "semantic_score":0.0,
                    "keyword_score": normalized_score
                }
            else:

                combined[chunk_id]["keyword_score"]=(
                    normalized_score
                )

        return combined


    def _calculate_final_score(
        self,
        semantic_score,
        keyword_score,
        alpha=0.7
    ):

        return(
            alpha * semantic_score
            +
            ( 1 - alpha ) * keyword_score
        )
    
# chunk_store=JSONLStore(config.chunk_path,model_class=Chunk)
# embedder=EmbeddingGenerator(config.embedding_model)
# embedding_store=JSONLStore(
#    config.embedding_path,
#     model_class=Embedding
# )
# semantic_searcher=SemanticSearcher(
#     embedder=embedder,
#     embedding_store=embedding_store,
#     chunk_store=chunk_store,
#     top_k=config.top_k,
#     threshold=config.retrieval_threshold,
#     faiss_index_path=config.faiss_index_path,
#     faiss_mapping_path=config.faiss_mapping_path
# )
# chunks=chunk_store.read_all()

# keyword_searcher=KeywordSearcher(
#     chunks=chunks
# )
# hybrid=HybridSearcher(
#     semantic_searcher=semantic_searcher,
#     keyword_searcher=keyword_searcher
# )
# results=hybrid.search("what is python")

# for result in results:

#     print(
#         result.chunk.id,
#         result.score
#     )