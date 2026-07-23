from src.pipelines.dataset_pipeline import DatasetPipeline
from src.config import Config
from src.factories.rag_factory import RAGFactory
from src.pipelines.analytics_pipeline import AnalyticsPipeline
from src.pipelines.deduplicator_pipeline import DeduplicatorPipeline
from src.loger_config import setup_logging
config=Config()
setup_logging()
urls=[
    "https://docs.python.org/3/tutorial/",
    "https://www.programiz.com/python-programming",
    "https://developer.mozilla.org/en-US/docs/Glossary/Python",
    "https://codehs.com/textbook/intropython_textbook/",
    "https://coddy.tech/docs/python/input-and-print"   
]

while True:

    print("---------AI Knowledge Platform---------\n\n")
    print("1.Build Dataset\n2.Deduplicator\n3.Compare Versions\n4.Ask Question\n5.Exit")

    choice=int(input("Enter Choice:"))
    
    match choice:

            case 1:
                obj=DatasetPipeline(config=config)
                obj.Dataset(urls=urls)
                
            case 2:
                obj=DeduplicatorPipeline(config=config)
                
                if obj.build_duplicator()==[]:
                     print("No duplicates found")
                else:
                     print("Deduplication is completed")
            
            case 3:
              pass

            case 4:
                question=input("prompt:")
                obj=RAGFactory(config)
                rag_obj=obj.factory()
                answer=rag_obj.ask(question=question)

                if answer is None:
                     print("Something Happend.Try Again")
            
                print("\n")
                print("Answer:\n")
                print(answer)
                print("\n")
            
            case 5:
                pipline=AnalyticsPipeline(config=config)
                report_obj=pipline.build_report()
                print(report_obj.generate_text())

            case 6:
                exit()
                




