
from src.storage.jsonl_store import JSONLStore
from src.models.chunk import Chunk
from src.chunkers.document_chunker import Chunker
class ChunkService:

    def __init__(self,path):

        self.chunk_store_obj=JSONLStore(path=path,model_class=Chunk)

    def build_chunks(self,document,chunk_size,rebuild=False):

        chunker_obj=Chunker(chunk_size=chunk_size)

        chunk_list=chunker_obj.chunk_document(document=document)

        if rebuild: 
            self.chunk_store_obj.replace_all(chunk_list)

        else:
            self.chunk_store_obj.save_many(chunk_list)
        


        