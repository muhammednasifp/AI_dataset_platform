# -----------------------------------------------------------------------------
# ContentQualityAnalyzer
#
# Analyzes dataset quality by identifying documents that may require review.
#
# This class performs simple rule-based quality checks such as:
# - Detecting unusually short documents.
# - Detecting unusually long documents.
# - Detecting documents containing common "noise" keywords.
#
# These checks help evaluate the overall quality of a dataset before it is
# used for downstream AI tasks such as embedding generation, semantic search,
# or Retrieval-Augmented Generation (RAG).
#
# Design Notes:
# - Operates on an in-memory list of Document objects.
# - Uses configurable thresholds to support different datasets.
# - Does not modify documents; it only identifies and returns matching ones.
# - Intended as a lightweight quality analysis component within the analytics
#   layer of the dataset pipeline.
# -----------------------------------------------------------------------------
from src.storage.jsonl_store import JSONLStore

class ContentQualityAnalyzer:

    def __init__(self,documents):
        
        self.documents=documents

    def short_documents(self,threshold=100):
                            # Threshold
                            # A configurable limit used to classify documents.
                            # Different datasets may require different thresholds.
        short_docs=[]

        for document in self.documents:

            if document.metadata["word_count"]<=threshold:
                short_docs.append(document)
        return short_docs

    def long_documents(self,threshold=500):

        long_docs=[]

        for document in self.documents:
            if document.metadata["word_count"]>=threshold:
                long_docs.append(document)

        return long_docs

    def noisy_documents(self,threshold=3):

        noise_doc=[]
        noise_keywords = [
            "company",
            "support",
            "resources",
            "languages",
            "blog"
        ]   
        
        for document in self.documents:
            count=0
            content=document.content.lower()

            for keyword in noise_keywords:
                if keyword in content:
                    count+=1

            if count>=threshold:
                noise_doc.append(document)
            

        return noise_doc

# store=JSONLStore("data/raw/documents.jsonl")

# docs=store.read_all()

# obj=ContentQualityAnalyzer(docs)

# print(obj.short_documents())

# long_doc=obj.long_documents()

# print(long_doc[0].metadata["word_count"])
# print(long_doc[1].metadata["word_count"])

# noise_doc=obj.noisy_documents()

# print(len(noise_doc))