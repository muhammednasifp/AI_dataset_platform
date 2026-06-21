# Quality Score
# A numerical estimate of document quality.
#
# Higher score = better document.

from src.storage.jsonl_store import JSONLStore

class QualityScorer:

    def score_document(self,document):

        final_score=dict()
        reasons=[]

        score = 0

        if document.metadata["word_count"] > 500:
            score += 50
            reasons.append("Word count above 500")

        if document.title:
            score += 25
            reasons.append("title exist")

        if  document.url:
            score += 25
            reasons.append("url exist")

        final_score["score"]=score
        final_score["reason"]=reasons

        return final_score
    
    def rank_document(self,documents):

        rankings=[]

        for doc in docs:
           score_info=self.score_document(doc)

           record={}
           record["docuemnt"]=doc
           record["score"]=score_info["score"]

           rankings.append(record)
        
        print(sorted(rankings,key=lambda item:item["score"],reverse=True))


store=JSONLStore("data/raw/documents.jsonl")

docs=store.read_all()

obj=QualityScorer()

obj.rank_document(docs)

# for doc in docs:

#     obj=QualityScorer(doc)
#     obj.rank_document()


        





        



        