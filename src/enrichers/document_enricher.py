from src.analytics.quality_scorer import QualityScorer
class DocumentEnricher:
    
    def enricher(self,document):
        
        word_count=len(document.content.split())
        char_count=len(document.content) # len(string) returns the number of characters in the text.

        document.metadata["word_count"]=word_count
        document.metadata["char_count"]=char_count

        scorer=QualityScorer(document=document)

        scoring_info=scorer.score_document()

        document.metadata["quality_score"]=scoring_info["score"]
        document.metadata["reasons"]=scoring_info["reasons"]

        return document

        