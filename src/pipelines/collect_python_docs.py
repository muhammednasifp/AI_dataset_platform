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

collector=DocsCollector()
store=JSONLStore("data/raw/documents.jsonl")
validator=DocumentValidator()
cleaner=DocumentCleaner()
enricher_obj=DocumentEnricher()

urls=[
    "https://docs.python.org/3/tutorial/",
    "https://www.programiz.com/python-programming",
    "https://developer.mozilla.org/en-US/docs/Glossary/Python",
    "https://codehs.com/textbook/intropython_textbook/",
    "https://coddy.tech/docs/python/input-and-print"   
]

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


# documents=store.read_all()
# print(documents[0].metadata)