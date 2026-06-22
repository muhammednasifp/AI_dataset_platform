# Chunking
#
# Splits a document into smaller pieces.
#
# Useful for:
# - Embeddings
# - Semantic Search
# - RAG Systems
from src.models.chunk import Chunk
from src.storage.jsonl_store import  JSONLStore
class Chunker:
    
    def __init__(self,chunk_size=200):
        
        self.chunk_size=chunk_size

    def chunk_document(self,document):

        chunk_list=[]

        for i in range(0,len(document.content),self.chunk_size):    
            content=document.content[i:i+self.chunk_size]

            chunk_number = (i // self.chunk_size) + 1

            chunk_obj = Chunk(
            id=f"{document.id}_chunk_{chunk_number}",
            document_id=document.id,
            content=content
        )
            chunk_list.append(chunk_obj)

        return chunk_list
    
    def save_chunks(self, chunks, store):

        for chunk in chunks:
            store.save_one(chunk)


        
# chunk_store=JSONLStore("data/processed/chunks.jsonl",model_class=Chunk)

# print(len(chunk_store.read_all()))




    

