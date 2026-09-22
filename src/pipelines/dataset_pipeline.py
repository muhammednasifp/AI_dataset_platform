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
from src.enrichers.document_enricher import DocumentEnricher
from src.models.document import Document
from src.services.chunk_service import ChunkService
from src.services.embedding_service import EmbeddingService
from src.services.faiss_service import FAISSService
from src.exceptions.collector import DocumentCollectionError
from src.exceptions.chunker import ChunkingError
from src.exceptions.embedding import EmbeddingError

import logging
logger = logging.getLogger(__name__)

class DatasetPipeline:

    def __init__(self,config):
        self.config=config
    
    def Dataset(self,urls):

        collector=DocsCollector()
        store=JSONLStore(
            self.config.jsonl_path,
            model_class=Document
        )
        chunk_builder=ChunkService(path=self.config.chunk_path)
        embedding_builder=EmbeddingService(path=self.config.embedding_path)
        faiss_builder=FAISSService(
            embeddings_path=self.config.embedding_path,
            faiss_index_path=self.config.faiss_index_path,
            faiss_mapping_path=self.config.faiss_mapping_path
        )
        validator=DocumentValidator()
        cleaner=DocumentCleaner()
        enricher_obj=DocumentEnricher()

        documents_received = len(urls)
        documents_processed = 0
        documents_failed = 0
        failed_documents=[]

        for url in urls:

            logger.info("Processing URL: %s", url)
            try:
                doc=collector.collect(url)
            
            except DocumentCollectionError as e:
                documents_failed += 1
                failed_documents.append({
                    "url": "https://bad-site.com",
                    "stage": "collection",
                    "reason": "Unable to download document"
                })
                logger.error("Failed to collect %s: %s", url, e)
                continue

            if doc is None:
                documents_failed += 1
                failed_documents.append({
                "url": url,
                "stage": "collection",
                "reason": "Document is Empty"
            })
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
                try:

                    chunk = chunk_builder.build_chunks(
                        chunk_size=self.config.chunk_size,
                        document=doc
                    )

                    logger.info(
                        "chunk Length=%s",
                        len(chunk)
                    )

                    embeddings = embedding_builder.build_embedding(
                        chunks=chunk,
                        embedding_model=self.config.embedding_model
                    )

                    logger.info(
                        "embedding Length=%s",
                        len(embeddings)
                    )
                    documents_processed=+1

                except (ChunkingError, EmbeddingError) as e:

                    documents_failed += 1
                    failed_documents.append({
                        "url": url,
                        "stage": "chunking" if isinstance(e, ChunkingError)
                                else "embedding",
                        "reason": str(e)
                    })

                    logger.error(
                        "Failed processing %s after storage: %s",
                        url,
                        e
                    )
                    continue
            else:
                documents_failed += 1
                failed_documents.append({
                    "url": url,
                    "stage": "validation",
                    "reason": "Document failed validation"
                })
                logger.warning(
                    "Document failed validation (id=%s, title='%s')",
                    doc.id,
                    doc.title
                )

        count=faiss_builder.build_index()                
        logger.info(
            "FAISS index contains %s vectors",count
        )

        return {
            "documents_received":documents_received,
            "documents_processed":documents_processed,
            "documents_failed":documents_failed,
            "failed_documents":failed_documents
        }
        
        

