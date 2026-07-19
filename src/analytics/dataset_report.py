# Reporting
# Convert analytics results into a human-readable summary.
#
# Reports help quickly understand dataset quality
# and size without inspecting raw data.
class DatasetReport:

    def __init__(self,dataset_analyzer,content_analyzer,scorer):
        self.analyzer=dataset_analyzer
        self.content_analyzer=content_analyzer
        self.scorer=scorer

    def generate_data(self):

       return {
            "total_docs":self.analyzer.total_documents(),
            "longest_doc_title": self.analyzer.longest_document().title,
            "longest_doc":self.analyzer.longest_document().metadata["word_count"],
            "shortest_doc_title": self.analyzer.shortest_document().title,
            "shortest_doc":self.analyzer.shortest_document().metadata["word_count"],
            "total_words":self.analyzer.total_words(),
            "average_words":self.analyzer.average_word_count(),
            "total_char":self.analyzer.total_char(),
            "average_char":self.analyzer.average_char_count(),
            "average_score":self.scorer.average_score(),
            "high_quality_doc":self.scorer.highest_quality()["quality_score"],
            "low_quality_doc":self.scorer.lowest_quality()["quality_score"],
            "high_quality_doc_count":self.content_analyzer.high_quality_count(),
            "low_quality_doc_count":self.content_analyzer.low_quality_count(),
            "medium_quality_count":self.content_analyzer.medium_quality_count(),
            "noisy_docs_count":len(self.content_analyzer.noisy_documents()),
            "long_docs_count":len(self.content_analyzer.long_documents()),
            "short_docs_count":len(self.content_analyzer.short_documents())
       }

    def generate_text(self):

        report_dict=self.generate_data()

        report = f"""
            ========== DATASET REPORT ==========

            DATASET OVERVIEW
            ----------------
            Total Documents      : {report_dict["total_docs"]}
            Total Words          : {report_dict["total_words"]}
            Average Words        : {round(report_dict["average_words"], 2)}

            Total Characters     : {report_dict["total_char"]}
            Average Characters   : {round(report_dict["average_char"], 2)}

            Longest Document     : {report_dict["longest_doc_title"]}
            Shortest Document    : {report_dict["shortest_doc_title"]}

            ===================================

            QUALITY ANALYSIS
            ----------------
            Average Quality Score : {round(report_dict["average_score"], 2)}

            Highest Quality Document
            Score : {report_dict["high_quality_doc"]}

            Lowest Quality Document
            Score : {report_dict["low_quality_doc"]}

            ===================================

            CONTENT DISTRIBUTION
            --------------------
            High Quality Documents   : {report_dict["high_quality_doc_count"]}
            Medium Quality Documents : {report_dict["medium_quality_count"]}
            Low Quality Documents    : {report_dict["low_quality_doc_count"]}

            Long Documents           : {report_dict["long_docs_count"]}
            Short Documents          : {report_dict["short_docs_count"]}
            Noisy Documents          : {report_dict["noisy_docs_count"]}

            ===================================
            """
    
        return report

# store=JSONLStore("data/raw/documents.jsonl")
# documents=store.read_all()
# analyzer=DatasetAnalyzer(documents=documents)
# scorer=QualityScorer(documents=documents)
# report_obj=DatasetReport(analyzer=analyzer,scorer=scorer)

# print(report_obj.generate())
