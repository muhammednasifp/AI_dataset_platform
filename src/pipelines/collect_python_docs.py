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

# for url in urls:

#     doc=collector.collect(url)
    
#     if doc:
#         doc=cleaner.clean(doc)

#     if validator.validate(doc): 

#         doc=enricher_obj.enricher(doc)
#         store.save_one(doc)
#         print("saved:",doc.title)
       
#     else:
#         print('error page',doc.title)
        
# documents=store.read_all()
# print(documents[0].metadata)