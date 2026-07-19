from src.config import Config
from src.pipelines.analytics_pipeline import AnalyticsPipeline

class AnalyticsService:

    @staticmethod
    def get_statics():
        
        config=Config()

        pipeline_obj=AnalyticsPipeline(config=config)

        report_obj=pipeline_obj.build_report()

        return report_obj.generate_data()
    
    @staticmethod
    def get_report():
        config=Config()

        pipeline_obj=AnalyticsPipeline(config=config)

        report_obj=pipeline_obj.build_report()

        return  report_obj.generate_text()





        

