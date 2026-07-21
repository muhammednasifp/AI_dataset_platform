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
from src.exceptions.storage import StorageError

import logging

logger=logging.getLogger(__name__)

from src.exceptions.storage import StorageError
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
        logger.info(
            "Saving object to %s",
            self.path
        )

        try:
            data=asdict(document)
            json_string=json.dumps(data)


            with open(self.path,"a") as file:
                file.write(json_string)
                file.write("\n")
        
        except OSError as e:

            logger.exception(
                "Failed to save document to %s",
                self.path
            )

            raise StorageError(f"Failed to Save document to '{self.path}'"
            
            ) from e
            
        logger.info(
            "Object saved successfully"
        )

    def save_many(self,documents):

        logger.info(
            "Saving %d objects",
            len(documents)
        )
        for document in documents:
            self.save_one(document=document)

        logger.info(
            "Finished saving %d objects",
            len(documents)
        )

    def count(self):

        logger.info(
            "Counting records in %s",
            self.path
        )
        try:
            count=0

            with open(self.path,"r") as file:
                for line in file:
                    count=count+1
        
        except OSError as e:
            logger.exception(
                " Failed to Count document %s",
                self.path
            )
            raise StorageError(f"Failed to count records in '{self.path}'.") from e
            
        return count

    def read_all(self):
        logger.info(
            "Reading records from %s",
            self.path
        )
        try:
            documents=[]
            with open(self.path,"r") as file:
                for line in file:
                    data=json.loads(line)

                    doc=self.model_class(**data)
                    documents.append(doc)   
            
           
        except OSError as e:
              raise StorageError(
                f"Failed to read data from '{self.path}'."
            ) from e
        
        logger.info(
            "Loaded %d objects",
            len(documents)
        )   
        return documents

    def replace_all(self,documents):

        logger.info(
            "Replacing all records in %s",
            self.path
        )

        try:
            with open(self.path,"w") as file:
                for document in documents:
                    data=asdict(document)
                    json_string=json.dumps(data)
                    file.write(json_string)
                    file.write("\n")
        except OSError as e:
            raise StorageError(
                f"Failed to replace data in '{self.path}'."
            ) from e

        logger.info(
            "Successfully replaced dataset with %d objects",
            len(documents)
        )
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
