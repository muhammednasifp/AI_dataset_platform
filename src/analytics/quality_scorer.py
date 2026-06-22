# Quality Score
# A numerical estimate of document quality.
#
# Higher score = better document.

from src.storage.jsonl_store import JSONLStore

class QualityScorer:

    def __init__(self,document=None,documents=None):
        self.document=document
        self.documents=documents

    def score_document(self):
        final_score=dict()
        reasons=[]

        score = 0

        if self.document.metadata["word_count"] > 500:
            score += 50
            reasons.append("Word count above 500")

        if self.document.title:
            score += 25
            reasons.append("title exist")

        if  self.document.url:
            score += 25
            reasons.append("url exist")

        final_score["score"]=score
        final_score["reasons"]=reasons

        return final_score
    
    def rank_document(self):

        rankings=[]

        for doc in self.documents:
           score=doc.metadata["quality_score"]

           record={}
           record["document"]=doc
           record["quality_score"]=score

           rankings.append(record)
        
        return sorted(rankings,key=lambda item:item["quality_score"],reverse=True)
    
    def average_score(self):

        total=0
        for doc in self.documents:

            total+=doc.metadata["quality_score"]
        
        return total/len(self.documents)

    def highest_quality(self):

        ranked=self.rank_document()

        return ranked[0]
    
    def lowest_quality(self):
        ranked=self.rank_document()

        return ranked[-1]

    def filter_high_quality(self):
        
        filterd_docs=[]
        ranked=self.rank_document()

        for item in ranked:

            if item["quality_score"]>=80:
                
                filterd_docs.append(item)

        return filterd_docs

# store=JSONLStore("data/raw/documents.jsonl")

# docs=store.read_all()


        





        



        