
from src.storage.jsonl_store import JSONLStore
from src.cleaners.deduplicator import Deduplicator
from src.storage.version_manager import DataVersionManager
from src.models.document import Document
from src.services.chunk_service import ChunkService
from src.services.embedding_service import EmbeddingService

import logging
logger=logging.getLogger(__name__)

class DeduplicatorPipeline:

    def __init__(self,config):

        self.config=config
         
    def build_duplicator(self):

        logger.info("Deduplication Started")

        store=JSONLStore(self.config.jsonl_path,model_class=Document)
        chunk_service=ChunkService(self.config.chunk_path)
        embedding_service=EmbeddingService(self.config.embedding_path)

        documents=store.read_all()

        if not documents:
            logger.warning("Dataset is empty")
            return None
        
        deduplicator_obj=Deduplicator(documents=documents)

        unique_docs=deduplicator_obj.remove_duplicates()

        duplicates_removed=len(documents) - len(unique_docs)
        if duplicates_removed==0:
            logger.info("No duplicates found")
            return 0
        
        version_manager=DataVersionManager(path=self.config.version_path)

        version_manager.create_version(documents=documents)

        store.replace_all(unique_docs)

        logger.info(len(unique_docs))

        chunks=chunk_service.rebuild_chunks(
            documents=unique_docs,
            chunk_size=self.config.chunk_size,
        )

        logger.info("Deduplication Ended")
        embedding_count=embedding_service.rebuild_embeddings(
            chunks=chunks,
            embedding_model=self.config.embedding_model
        )

        return{
            "duplicates_removed": duplicates_removed,
            "documents_after": len(unique_docs),
            "chunks_created": len(chunks),
            "embeddings_created": embedding_count
        }
        











        





