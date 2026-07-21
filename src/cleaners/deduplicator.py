# Deduplication
# The process of detecting and removing
# duplicate records from a dataset.
#
# Improves data quality and reduces storage.

class Deduplicator:
    
    def __init__(self,documents):

        self.documents=documents
    
    def remove_duplicates(self):

        seen_urls=set()
        unique_docs=[]

        for document in self.documents:

            if document.url not in seen_urls:
                seen_urls.add(document.url)
                unique_docs.append(document)


        before = len(self.documents)

        after = len(unique_docs)

        removed = before - after

        if removed==0:
            return 0
        
        return unique_docs

        
         

# store=JSONLStore("data/raw/documents.jsonl")
# documents=store.read_all()

# obj=Deduplicator(documents=documents)
# docs=obj.remove_duplicates()

# store.replace_all(docs)