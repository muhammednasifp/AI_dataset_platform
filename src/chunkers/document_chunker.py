# Chunking
#
# Splits a document into smaller pieces.
#
# Useful for:
# - Embeddings
# - Semantic Search
# - RAG Systems
from src.exceptions.chunker import ChunkingError
from src.models.chunk import Chunk
from src.storage.jsonl_store import  JSONLStore

import logging

logger=logging.getLogger(__name__)

class Chunker:
    
    def __init__(self,chunk_size):
        
        self.chunk_size=chunk_size

    def chunk_document(self,document):

        try:

            logger.info("Starting chunking for document (id=%s)", document.id)

            chunk_list=[]

            for i in range(0,len(document.content),self.chunk_size):

                content=document.content[i:i+self.chunk_size]

                if not document.content:
                    logger.error(
                        "Chunking failed: document (id=%s) has no content",
                        document.id,
                    )
                    raise ChunkingError("Document has no content.")
                chunk_number = (i // self.chunk_size) + 1

                chunk_obj = Chunk(
                id=f"{document.id}_chunk_{chunk_number}",
                document_id=document.id,
                content=content
            )
                chunk_list.append(chunk_obj)

        except Exception as e:

            logger.exception(
                "Unexpected error while chunking document (id=%s)",
                document.id,
            )
            raise ChunkingError("Failed to chunk document.") from e

        logger.info(
            "Chunking completed (id=%s, chunks=%d)",
            document.id,
            len(chunk_list),
        )

        return chunk_list
    
    def save_chunks(self, chunks, store):

        logger.info("Saving %d chunks", len(chunks))

        for chunk in chunks:
            store.save_one(chunk)

        logger.info("Chunks saved successfully")


        
# chunk_store=JSONLStore("data/processed/chunks.jsonl",model_class=Chunk)

# print(len(chunk_store.read_all()))




    

