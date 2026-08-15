# -----------------------------------------------------------------------------
# Dataset Ingestion Pipeline
#
# Orchestrates the end-to-end process of building the document dataset.
#
# Pipeline Flow:
# 1. Collect documents from configured URLs.
# 2. Clean the extracted content.
# 3. Validate document quality.
# 4. Enrich documents with computed metadata.
# 5. Store valid documents in JSONL format.
#
# Design Notes:
# - Acts as the application's orchestration layer.
# - Coordinates independent pipeline components without implementing
#   their internal logic.
# - Each processing stage has a single responsibility, making the
#   pipeline modular and easy to extend.
# -----------------------------------------------------------------------------
from src.collectors.docs_collector import DocsCollector
from src.storage.jsonl_store import JSONLStore
from src.validator.document_validator import DocumentValidator
from src.cleaners.document_cleaner import DocumentCleaner
from src.cleaners.deduplicator import Deduplicator
from src.enrichers.document_enricher import DocumentEnricher
from src.models.document import Document
from src.services.chunk_service import ChunkService
from src.services.embedding_service import EmbeddingService
from src.exceptions.collector import DocumentCollectionError
import logging
logger = logging.getLogger(__name__)

class DatasetPipeline:

    def __init__(self,config):
        self.config=config
    
    def Dataset(self,urls):
        collector=DocsCollector()
        store=JSONLStore(self.config.jsonl_path,model_class=Document)
        chunk_builder=ChunkService(path=self.config.chunk_path)
        embedding_builder=EmbeddingService(path=self.config.embedding_path)
        validator=DocumentValidator()
        cleaner=DocumentCleaner()
        enricher_obj=DocumentEnricher()

        for url in urls:

            logger.info("Processing URL: %s", url)
            try:
                doc=collector.collect(url)
            
            except DocumentCollectionError as e:
                logger.error("Failed to collect %s: %s", url, e)
                continue

            if doc is None:
                continue
            
            doc=cleaner.clean(doc)

            if validator.validate(doc,threshold=self.config.validation_threshold): 

                doc=enricher_obj.enricher(doc)
                store.save_one(doc)
                logger.info(
                    "Saved document (id=%s, title='%s')",
                    doc.id,
                    doc.title
                )
                chunk=chunk_builder.build_chunks(
                    chunk_size=self.config.chunk_size,
                    document=doc
                )
                
                logger.info(
                    "chunk Length=%s",len(chunk)
                )
                
                embeddings=embedding_builder.build_embedding(
                    chunks=chunk,
                    embedding_model=self.config.embedding_model
                )

                logger.info(
                    "embedding Length=%s",len(embeddings)
                )
            
            else:
                logger.warning(
                    "Document failed validation (id=%s, title='%s')",
                    doc.id,
                    doc.title
                )
        
        

