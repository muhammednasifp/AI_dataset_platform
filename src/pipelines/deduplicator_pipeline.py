
from src.storage.jsonl_store import JSONLStore
from src.cleaners.deduplicator import Deduplicator
from src.storage.version_manager import DataVersionManager
from src.models.document import Document
class DeduplicatorPipeline:

    def __init__(self,version_path,jsonl_path,):
        self.version_path=version_path
        self.jsonl_path=jsonl_path
    def build_duplicator(self):

        store=JSONLStore(self.jsonl_path,model_class=Document)

        documents=store.read_all()

        if documents is None:
            return None

        deduplicator_obj=Deduplicator(documents=documents)

        unique_docs=deduplicator_obj.remove_duplicates()

        if unique_docs is 0:
                return []
        
        version_manager=DataVersionManager(path=self.version_path)

        version_manager.create_version(documents=documents)

        store.replace_all(unique_docs)





