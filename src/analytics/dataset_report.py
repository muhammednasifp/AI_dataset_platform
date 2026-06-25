# Reporting
# Convert analytics results into a human-readable summary.
#
# Reports help quickly understand dataset quality
# and size without inspecting raw data.
from src.analytics.dataset_analyzer import DatasetAnalyzer
from src.storage.jsonl_store import JSONLStore
from src.analytics.quality_scorer import QualityScorer
class DatasetReport:

    def __init__(self,analyzer,scorer):
        self.analyzer=analyzer
        self.scorer=scorer
    
    
    def generate(self):

        total_docs=self.analyzer.total_documents()
        total_words=self.analyzer.total_words()
        average_words=self.analyzer.average_word_count()
        longest_doc=self.analyzer.longest_document()
        shortest_doc=self.analyzer.shortest_document()
        average_score=self.scorer.average_score()
        high_quality_doc=self.scorer.highest_quality()
        low_quality_doc=self.scorer.lowest_quality()

        report=f"""
        ========== DATASET REPORT ==========

        Total Documents : {total_docs}
        Total Words     : {total_words}
        Average Words   : {round(average_words, 2)}
        

        Longest Document:
        {longest_doc.title}

        Shortest Document:
        {shortest_doc.title}

        ====================================

        Average Score:
        {average_score}

        Highest Quality:
        {high_quality_doc["document"]}
        Score:
        {high_quality_doc["quality_score"]}

        Lowest Quality:
        {low_quality_doc["document"]}
        Score:
        {low_quality_doc["quality_score"]}

        """
        # round(value, digits)
        # Rounds a floating-point number to a fixed
        # number of decimal places.
        #
        # Example:
        # round(473.2333, 2)
        # -> 473.23

        return report

store=JSONLStore("data/raw/documents.jsonl")
documents=store.read_all()
analyzer=DatasetAnalyzer(documents=documents)
scorer=QualityScorer(documents=documents)
report_obj=DatasetReport(analyzer=analyzer,scorer=scorer)

print(report_obj.generate())
