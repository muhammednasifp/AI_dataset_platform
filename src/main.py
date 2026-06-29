from src.models.document import Document
from src.storage.jsonl_store import JSONLStore
from src.pipelines.collect_python_docs import DatasetPipeline
from src.config import Config
from src.analytics.dataset_analyzer import DatasetAnalyzer
from src.storage.jsonl_store import JSONLStore
from src.analytics.quality_scorer import QualityScorer
from src.analytics.dataset_report import DatasetReport
from src.factories.rag_factory import RAGFactory

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
                #improve Later
                store=JSONLStore(config.jsonl_path,model_class=Document)
                documents=store.read_all()
                analyzer=DatasetAnalyzer(documents=documents)
                scorer=QualityScorer(documents=documents)
                report_obj=DatasetReport(analyzer=analyzer,scorer=scorer)

                print(report_obj.generate())

            case 4:
                exit()
                




