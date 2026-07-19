from src.pipelines.dataset_pipeline import DatasetPipeline
from src.config import Config
from src.factories.rag_factory import RAGFactory
from src.pipelines.analytics_pipeline import AnalyticsPipeline
config=Config()
urls=[
    "https://docs.python.org/3/tutorial/",
    "https://www.programiz.com/python-programming",
    "https://developer.mozilla.org/en-US/docs/Glossary/Python",
    "https://codehs.com/textbook/intropython_textbook/",
    "https://coddy.tech/docs/python/input-and-print"   
]

while True:

    print("---------AI Knowledge Platform---------\n\n")
    print("1.Build Dataset\n2.Ask Questions(RAG)\n3.Get Report\n4.Exit\n")

    choice=int(input("Enter Choice:"))
    
    match choice:

            case 1:
                obj=DatasetPipeline()
                obj.Dataset(urls=urls)
            
            case 2:
                question=input("prompt:")
                obj=RAGFactory(config)
                rag_obj=obj.factory()
                answer=rag_obj.ask(question=question)

                print("\n")
                print("Answer:\n")
                print(answer)
                print("\n")
            
            case 3:
                pipline=AnalyticsPipeline(config=config)
                report_obj=pipline.build_report()
                print(report_obj.generate_text())

            case 4:
                exit()
                




