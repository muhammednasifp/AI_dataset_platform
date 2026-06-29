from src.models.chunk import Chunk
from src.models.embedding import Embedding
from src.embedders.embedding_generator import EmbeddingGenerator
from src.search.semantic_searcher import SemanticSearcher
from src.rag.context_builder import ContextBuilder
from src.rag.generator import Generator
from src.rag.prompt_builder import PromptBuilder
from src.storage.jsonl_store import JSONLStore
from src.pipelines.rag_pipeline import RAGPipeline

class RAGFactory:
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
        context_builder=ContextBuilder()
        prompt_builder=PromptBuilder()
        searcher=SemanticSearcher(
                embedder=embedder,
                embedding_store=embedding_store,
                chunk_store=chunk_store
        )
        generator=Generator()

        rag_obj=RAGPipeline(
                searcher=searcher,
                generator=generator,
                context_builder=context_builder,
                prompt_builder=prompt_builder
        )

        return rag_obj
