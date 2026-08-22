import json
import faiss
import numpy as np

class FAISSIndex:

    def __init__(self,dimension):

        self.dimension = dimension

        self.index = faiss.IndexFlatIP(
            dimension
        )
        self.chunk_ids=[]

    def build(self,embeddings):

        vectors = np.array(
            [embedding.vector for embedding in embeddings],
            dtype="float32"
        )

        self.chunk_ids=[
            embedding.chunk_id
            for embedding in embeddings
        ]

        faiss.normalize_L2(vectors)

        self.index.add(vectors)

        return self.index.ntotal

    def search(self, query_vector, top_k):

        query_vector = np.array(
            [query_vector],
            dtype="float32"
        )

        faiss.normalize_L2(query_vector)

        scores, indices = self.index.search(
            query_vector,
            top_k
        )

        results=[]

        for score,index in zip(
            scores[0],
            indices[0]
        ):
            if index ==-1:
                continue


            results.append({
                "chunk":self.chunk_ids[index],
                "score":float(score)
            })

        return results

    def save(self, index_map,mapping_path):

        faiss.write_index(
            self.index,
            index_map
        )

        with open(mapping_path, "w") as file:
            json.dump(
                self.chunk_ids,
                file
            )