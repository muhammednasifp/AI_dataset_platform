
from src.storage.jsonl_store import JSONLStore
from src.models.chunk import Chunk
from src.chunkers.document_chunker import Chunker

class ChunkService:

    def __init__(self,path):

        self.chunk_store_obj=JSONLStore(path=path,model_class=Chunk)

    def build_chunks(self,document,chunk_size):

        chunker_obj=Chunker(chunk_size=chunk_size)

        chunk_list=chunker_obj.chunk_document(document=document)

        self.chunk_store_obj.save_many(chunk_list)

        return chunk_list

    def rebuild_chunks(self, documents, chunk_size):

        all_chunks = []

        chunker_obj = Chunker(chunk_size=chunk_size)

        for document in documents: 

            chunks = chunker_obj.chunk_document(
                document=document
            )

            all_chunks.extend(chunks)

        self.chunk_store_obj.replace_all(all_chunks)

        return all_chunks
        


        