from src.analytics.dataset_analyzer import DatasetAnalyzer
from src.analytics.content_quality_analyzer import ContentQualityAnalyzer
from src.storage.jsonl_store import JSONLStore
from src.analytics.quality_scorer import QualityScorer
from src.analytics.dataset_report import DatasetReport
from src.models.document import Document
from src.storage.jsonl_store import JSONLStore
class AnalyticsPipeline:

    def __init__(self,config):
        
        self.config=config

    def build_report(self):
        
        store=JSONLStore(
            self.config.jsonl_path,
            model_class=Document
        )

        documents=store.read_all()

        dataset_analyzer=DatasetAnalyzer(documents=documents)

        content_analyzer=ContentQualityAnalyzer(documents=documents)

        scorer=QualityScorer(documents=documents)

        report_obj=DatasetReport(dataset_analyzer=dataset_analyzer,content_analyzer=content_analyzer,scorer=scorer)

        return report_obj