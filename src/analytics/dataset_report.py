from src.analytics.dataset_analyzer import DatasetAnalyzer
from src.storage.jsonl_store import JSONLStore
# Reporting
# Convert analytics results into a human-readable summary.
#
# Reports help quickly understand dataset quality
# and size without inspecting raw data.
class DatasetReport:

    def __init__(self,analyzer):
        self.analyzer=analyzer
    
    def generate(self):

        total_docs=self.analyzer.total_documents()
        total_words=self.analyzer.total_words()
        average_words=self.analyzer.average_word_count()
        longest_doc=self.analyzer.longest_document()
        shortest_doc=self.analyzer.shortest_document()

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
        """
        # round(value, digits)
        # Rounds a floating-point number to a fixed
        # number of decimal places.
        #
        # Example:
        # round(473.2333, 2)
        # -> 473.23
        return report

# store=JSONLStore("data/raw/documents.jsonl")
# documents=store.read_all()
# analyzer=DatasetAnalyzer(documents=documents)

# report_obj=DatasetReport(analyzer=analyzer)

# print(report_obj.generate())
