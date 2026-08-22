from src.search.faiss_index import FAISSIndex

vectors = [
    [1.0, 0.0, 0.0],
    [0.0, 1.0, 0.0],
    [0.9, 0.1, 0.0]
]

index = FAISSIndex(dimension=3)

print("Vectors indexed:", index.build(vectors))

scores, indices = index.search(
    query_vector=[1.0, 0.0, 0.0],
    top_k=2
)

print("Scores:", scores)
print("Indices:", indices)