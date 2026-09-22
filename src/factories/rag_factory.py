from src.search.hybrid_searcher import HybridSearcher
from src.search.keyword_searcher import KeywordSearcher
from src.models.chunk import Chunk
from src.models.embedding import Embedding
from src.embedders.embedding_generator import EmbeddingGenerator
from src.search.semantic_searcher import SemanticSearcher
from src.rag.context_builder import ContextBuilder
from src.rag.generator import Generator
from src.rag.prompt_builder import PromptBuilder
from src.storage.jsonl_store import JSONLStore
from src.pipelines.rag_pipeline import RAGPipeline

class  RAGFactory:
    def __init__(self,config):
        self.config=config
    def factory(self):

        embedder=EmbeddingGenerator(self.config.embedding_model)
        
        embedding_store=JSONLStore(
                self.config.embedding_path,
                model_class=Embedding
        )
        chunk_store=JSONLStore(
                self.config.chunk_path,
                model_class=Chunk
        )
        semantic_searcher=SemanticSearcher(
                embedder=embedder,
                embedding_store=embedding_store,
                chunk_store=chunk_store,
                top_k=self.config.top_k,
                threshold=self.config.retrieval_threshold,
                faiss_index_path=self.config.faiss_index_path,
                faiss_mapping_path=self.config.faiss_mapping_path
        )
        keyword_searcher=KeywordSearcher(
                chunk_store=chunk_store
        )
        hybrid_searcher=HybridSearcher(
            semantic_searcher=semantic_searcher,
            keyword_searcher=keyword_searcher,
            top_k=self.config.top_k
        )
        context_builder=ContextBuilder()
        prompt_builder=PromptBuilder()
        generator=Generator()

        rag_obj=RAGPipeline(
                searcher=hybrid_searcher,
                generator=generator,
                context_builder=context_builder,
                prompt_builder=prompt_builder
        )

        return rag_obj
