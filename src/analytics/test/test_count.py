
from src.storage.jsonl_store import JSONLStore

obj=JSONLStore("data/raw/documents.jsonl")

documents=obj.read_all()

for doc in documents:
    print(doc.title)
    print(len(doc.content.split()))
    print("-"*50)



