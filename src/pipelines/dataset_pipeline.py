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

import logging
logger = logging.getLogger(__name__)

class DatasetPipeline:

    def __init__(self,config):
        self.config=config
    
    def Dataset(self,urls):
        collector=DocsCollector()
        store=JSONLStore(self.config.jsonl_path,model_class=Document)
        chunk_store=ChunkService(self.config.chunk_path)
        validator=DocumentValidator()
        cleaner=DocumentCleaner()
        enricher_obj=DocumentEnricher()

        for url in urls:

            logger.info("Processing URL: %s", url)

            doc=collector.collect(url)
            
            if doc is None:
                logger.error("Failed to collect document from %s", url)
                continue

            doc=cleaner.clean(doc)

            if validator.validate(doc,threshold=self.config.validation_threshold): 

                doc=enricher_obj.enricher(doc)
                store.save_one(doc)
                chunk_store.build_chunks(chunk_size=self.config.chunk_size ,document=doc)
                
                logger.info(
                    "Saved document (id=%s, title='%s')",
                    doc.id,
                    doc.title
                )
            
            else:
                logger.warning(
                    "Document failed validation (id=%s, title='%s')",
                    doc.id,
                    doc.title
                )
            
        

