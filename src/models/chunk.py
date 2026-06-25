# -----------------------------------------------------------------------------
# Chunk
#
# Represents a small, self-contained segment of a larger document.
#
# Chunks are the fundamental retrieval units in a Retrieval-Augmented
# Generation (RAG) system. Instead of embedding and searching entire
# documents, documents are divided into smaller chunks to improve retrieval
# accuracy and provide more relevant context to language models.
#
# Fields:
# - id          : Unique identifier for the chunk.
# - document_id : Identifier of the parent document.
# - content     : Text contained within the chunk.
#
# Design Notes:
# - Acts as the bridge between documents and vector embeddings.
# - Maintains a reference to its source document through document_id.
# - Designed as a lightweight immutable data container using @dataclass.
# -----------------------------------------------------------------------------
from dataclasses import dataclass

@dataclass
class Chunk:
    id:str
    document_id:str
    content:str

