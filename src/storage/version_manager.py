# Dataset Versioning
# Store snapshots of a dataset over time.
#
# Benefits:
# - Reproducibility
# - Auditing
# - Rollback capability
#
# Similar to version control for code.
from src.storage.jsonl_store import JSONLStore
from src.models.document import Document
import os

class DataVersionManager:
    
    def __init__(self,path):
        self.path=path
        os.makedirs(
        self.path,
        exist_ok=True
    )

    def create_version(self,documents):

        id_num=len(os.listdir(self.path))+1

        # new_path=self.path+f"version_{str(id_num)}.jsonl"
        new_path=os.path.join(self.path,f"version_{id_num}.jsonl")
        # os.path.join()
        # Safely combines directory and file names.
        #
        # Example:
        # os.path.join("data/versions", "version_1.jsonl")
        #
        # Works correctly across operating systems.
        store=JSONLStore(new_path,model_class=Document)
        store.save_many(documents=documents)

        return new_path
    
    def read_version(self,v_num):
        # new_path=self.path+f"version_{str(id_num)}.jsonl"
        new_path=os.path.join(self.path,f"version_{v_num}.jsonl")

        store=JSONLStore(new_path)

        return store.read_all()

    def list_versions(self):

        return sorted(os.listdir(self.path))
        # os.listdir()
        # Returns all files and folders inside a directory.
        #
        # Example:
        # os.listdir("data/versions")
        #
        # Output:
        # ["version_1.jsonl", "version_2.jsonl"]

# manager = DataVersionManager(
#     "data/versions/"
# )
# store=JSONLStore("data/raw/documents.jsonl")
# documents=store.read_all()
# manager.create_version(documents=documents)

# manager.list_versions()
