from src.search.faiss_index import FAISSIndex
from src.storage.jsonl_store import JSONLStore
from src.models.embedding import Embedding
class FAISSService:

    def __init__(self,embeddings_path,faiss_index_path,faiss_mapping_path):
       self.embedding_store=JSONLStore(
           path=embeddings_path,
           model_class=Embedding
       )
       self.faiss_index_path=faiss_index_path
       self.faiss_mapping_path=faiss_mapping_path

    def build_index(self):

        embeddings=self.embedding_store.read_all()

        if not embeddings:
            return 0

        dimension = len(embeddings[0].vector)

        faiss_index = FAISSIndex(
            dimension=dimension
        )

        count = faiss_index.build(
            embeddings=embeddings
        )

        faiss_index.save(
            self.faiss_index_path,
            self.faiss_mapping_path
        )

        return count


