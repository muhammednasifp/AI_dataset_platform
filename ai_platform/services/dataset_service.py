from src.config import Config
from src.pipelines.collect_python_docs import DatasetPipeline
class DatasetService:
    
    @staticmethod
    def build(urls,chunk_size,top_k):
        urls = [
            url.strip()
            for url in urls.splitlines()
            if url.strip()
        ]
        print(urls)
        if not urls:
            return{
            "success":False,
            "message":"Invalid URLs"
        }
        config=Config(top_k=int(top_k),chunk_size=int(chunk_size))

        pipeline_obj=DatasetPipeline(config=config)

        try:

            pipeline_obj.Dataset(urls=urls)

            return{
                "success":True,
                "message":"Dataset Build Completed"
            }
        except  Exception as e:

             return {
                "success": False,
                "message": "Failed to build the dataset.",
                "error": str(e)
            }
