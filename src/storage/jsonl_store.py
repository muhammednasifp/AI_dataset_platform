# -----------------------------------------------------------------------------
# JSONLStore
#
# Provides a generic storage interface for reading and writing dataclass
# objects in JSON Lines (JSONL) format.
#
# Responsibilities:
# - Persist individual or multiple objects as JSONL records.
# - Read stored records back into dataclass instances.
# - Count stored records.
# - Replace the entire dataset with a new collection of objects.
#
# Design Notes:
# - Generic storage component that works with any dataclass model.
# - Uses dependency injection to reconstruct objects via the supplied
#   model_class.
# - Stores one JSON object per line for efficient streaming and incremental
#   updates.
# - Separates persistence logic from business logic, allowing the same
#   storage implementation to be reused across Documents, Chunks,
#   Embeddings, and future models.
# -----------------------------------------------------------------------------
import json
import os
from dataclasses import asdict


class JSONLStore:
    
    def __init__(self,path,model_class):

        self.path=path
        self.model_class = model_class
        directory = os.path.dirname(path)

        os.makedirs(
            directory,
            exist_ok=True
        )
    
    def save_one(self,document): 
        data=asdict(document)
        json_string=json.dumps(data)

        with open(self.path,"a") as file:
            file.write(json_string)
            file.write("\n")

    def save_many(self,documents):
        for document in documents:
            self.save_one(document=document)

    def count(self):
        count=0

        with open(self.path,"r") as file:
            for line in file:
                count=count+1
        
        return count

    def read_all(self):
        documents=[]
        with open(self.path,"r") as file:
            for line in file:
                data=json.loads(line)

                doc=self.model_class(**data)
                documents.append(doc)      
        return documents

    def replace_all(self,documents):

        with open(self.path,"w") as file:
            for document in documents:
                data=asdict(document)
                json_string=json.dumps(data)
                file.write(json_string)
                file.write("\n")
    # replace_all()
    #
    # Replaces the entire dataset with a new
    # collection of documents.
    #
    # Uses write mode ("w") to clear existing
    # contents before writing new records.
    #
    # Common use cases:
    # - Deduplication
    # - Dataset cleaning
    # - Dataset rebuilding

# store=JSONLStore("data/raw/documents.jsonl")
# docs=[
#     Document(id="1",
#     title="Python Basics",
#     url="https://example.com",
#     content="Python intro",
#     source="python_docs"
#     ),
#     Document(id="2",
#     title="Python Basics",
#     url="https://example.com",
#     content="Python intro",
#     source="python_docs"
#     ),
#     Document(id="3",
#     title="Python Basics",
#     url="https://example.com",
#     content="Python intro",
#     source="python_docs"
#     )
# ]

# #store.save_many(docs)
# #store.count()
# documents=store.read_all()
# print(documents)
