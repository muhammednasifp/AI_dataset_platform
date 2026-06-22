
from src.storage.jsonl_store import JSONLStore

class DatasetAnalyzer:
    
    def __init__(self,documents):
        
        self.documents=documents

    def total_documents(self):
        
        return len(self.documents)
    
    def total_words(self):

        total=0
        for doc in self.documents:
            total+=len(doc.content.split())
        
        return total
           
    def average_word_count(self):

        return self.total_words()/len(self.documents)
    
    def longest_document(self):

        longest_doc=None
        max_words=0

        for doc in self.documents:
            no_words=len(doc.content.split())

            if no_words>max_words:
                longest_doc=doc
                max_words=no_words
        
        return longest_doc
    

    def shortest_document(self):

        shortest_doc=None
        min_words=1e99

        for doc in self.documents:
            no_words=len(doc.content.split())
            if no_words<min_words:
                shortest_doc=doc
                min_words=no_words
        
        return shortest_doc
    
      
# store=JSONLStore("data/raw/documents.jsonl")
# documents=store.read_all()  
# obj=DatasetAnalyzer(documents=documents)

# total_doc=obj.total_documents()
# print(total_doc)

# total_word=obj.total_words()
# print(total_word)

# avg=obj.average_word_count()
# print(avg)

# longest_doc=obj.longest_document()
# print(longest_doc.title)

# shortest_doc=obj.shortest_document()
# print(shortest_doc.title)