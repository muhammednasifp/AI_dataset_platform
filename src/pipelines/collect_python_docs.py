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

class DatasetPipeline:

    def __init__(self,config):
        self.config=config
    
    def Dataset(self,urls):
        collector=DocsCollector()
        store=JSONLStore(self.config.jsonl_path)
        validator=DocumentValidator()
        cleaner=DocumentCleaner()
        enricher_obj=DocumentEnricher()

        for url in urls:

            doc=collector.collect(url)
            
            if doc:
                doc=cleaner.clean(doc)

            if validator.validate(doc): 

                doc=enricher_obj.enricher(doc)
                store.save_one(doc)
                print("saved:",doc.title)
            
            else:
                print('error page',doc.title)
        
        # chunk_store=JSONLStore(self.config.chunk_path)
        

