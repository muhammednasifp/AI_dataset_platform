# -----------------------------------------------------------------------------
# RAGPipeline
#
# Orchestrates the end-to-end Retrieval-Augmented Generation (RAG) workflow.
#
# Pipeline Flow:
# 1. Retrieve the most relevant chunks using semantic search.
# 2. Build a context from the retrieved chunks.
# 3. Construct a prompt using the user question and retrieved context.
# 4. Generate an answer using the language model.
#
# Design Notes:
# - Acts as the orchestration layer for the RAG system.
# - Coordinates independent components without implementing their internal
#   logic.
# - Uses dependency injection to remain modular and easily testable.
# - Can be extended with reranking, caching, conversation memory,
#   citations, and multiple retrieval strategies.
# -----------------------------------------------------------------------------
from src.models.chunk import Chunk
from src.models.embedding import Embedding
from src.embedders.embedding_generator import EmbeddingGenerator
from src.search.semantic_searcher import SemanticSearcher
from src.rag.context_builder import ContextBuilder
from src.rag.generator import Generator
from src.rag.prompt_builder import PromptBuilder
from src.storage.jsonl_store import JSONLStore


class RAGPipeline:

    def __init__(self,generator,searcher,context_builder,prompt_builder):
        
        self.searcher=searcher
        self.generator=generator
        self.context_builder=context_builder
        self.prompt_builder=prompt_builder
        
    def ask(self,question):

        chunks=self.searcher.search(question)
        context=self.context_builder.build(chunks)
        prompt=self.prompt_builder.build(question,context)

        result=self.generator.generate(prompt)

        return result

question=input("prompt:")
embedder=EmbeddingGenerator()
embedding_store=JSONLStore(
        "data/processed/embeddings.jsonl",
        model_class=Embedding
)
chunk_store=JSONLStore(
        "data/processed/chunks.jsonl",
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


answer=rag_obj.ask(question=question)

print("Answer:\n")
print(answer)

