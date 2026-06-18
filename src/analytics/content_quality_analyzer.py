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

            if document.metadata["word_count"]<threshold:
                short_docs.append(document)
        return short_docs

    def long_documents(self,thresold=500):

        long_docs=[]

        for document in self.documents:
            if document.metadata["word_count"]>=thresold:
                long_docs.append(document)

        return long_docs

    def noisy_documents(self):
        pass    


store=JSONLStore("data/raw/documents.jsonl")

docs=store.read_all()

obj=ContentQualityAnalyzer(docs)

print(obj.short_documents())

long_doc=obj.long_documents()

print(long_doc[0].metadata["word_count"])
print(long_doc[1].metadata["word_count"])