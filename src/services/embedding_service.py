from src.storage.jsonl_store import JSONLStore
from src.models.embedding import Embedding
from src.embedders.embedding_generator import EmbeddingGenerator

class EmbeddingService:

    def __init__(self,path):
        
        self.embedding_store_obj=JSONLStore(path=path,model_class=Embedding)

    def build_embedding(self,embedding_model,chunks):

        embedding_obj=EmbeddingGenerator(embedding_model=embedding_model)

        embeddings = []

        for chunk in chunks:
            embedding = embedding_obj.generate(chunk=chunk)
            self.embedding_store_obj.save_one(embedding)
            embeddings.append(embedding)

        return embeddings
    
    def rebuild_embeddings(self,embedding_model,chunks):
        
        all_embedding=[]
        embedding_obj=EmbeddingGenerator(embedding_model=embedding_model)

        for chunk in chunks:

            embedding=embedding_obj.generate(chunk=chunk)
            all_embedding.append(embedding)

        
        self.embedding_store_obj.replace_all(all_embedding)

        return len(all_embedding)

        



        
        

        
