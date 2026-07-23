
from src.storage.jsonl_store import JSONLStore
from src.cleaners.deduplicator import Deduplicator
from src.storage.version_manager import DataVersionManager
from src.models.document import Document
from src.services.chunk_service import ChunkService

import logging
logger=logging.getLogger(__name__)

class DeduplicatorPipeline:

    def __init__(self,config):

        self.config=config
         
    def build_duplicator(self):

        store=JSONLStore(self.config.jsonl_path,model_class=Document)
        chunk_service=ChunkService(self.config.chunk_path)

        documents=store.read_all()

        if documents is None:
            return None

        deduplicator_obj=Deduplicator(documents=documents)

        unique_docs=deduplicator_obj.remove_duplicates()

        if unique_docs == 0:

            return []
        
        version_manager=DataVersionManager(path=self.config.version_path)
        version_manager.create_version(documents=documents)

        # store.replace_all(unique_docs)

        logger.info(len(unique_docs))
        # for docs in unique_docs:
        #     chunk_service.build_chunks(
        #         document=docs,
        #         chunk_size=self.config.chunk_size,
        #         rebuild=True
        #     )









        





