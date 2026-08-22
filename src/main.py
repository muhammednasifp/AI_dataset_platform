from src.exceptions.generator import GeneratorError
from src.pipelines.dataset_pipeline import DatasetPipeline
from src.config import Config
from src.factories.rag_factory import RAGFactory
from src.pipelines.analytics_pipeline import AnalyticsPipeline
from src.pipelines.deduplicator_pipeline import DeduplicatorPipeline
from src.loger_config import setup_logging

config=Config()
setup_logging()
rag_obj = RAGFactory(config).factory()

urls=[
    "https://docs.python.org/3/tutorial/",
    "https://www.programiz.com/python-programming",
    "https://developer.mozilla.org/en-US/docs/Glossary/Python",
    "https://codehs.com/textbook/intropython_textbook/",
    "https://coddy.tech/docs/python/input-and-print"   
]

while True:

    print("\n---------AI Knowledge Platform---------\n\n")
    print(
        "1. Build Dataset\n"
        "2. Deduplicator\n"
        "3. Ask Question\n"
        "4. Print Report\n"
        "5. Exit"
    )

    choice=int(input("Enter Choice:"))
    
    match choice:
            case 1:
                obj=DatasetPipeline(config=config)
                obj.Dataset(urls=urls)
                
            case 2:
                obj=DeduplicatorPipeline(config=config)
                
                result=obj.build_duplicator()

                if result is None:
                    print("Empty Dataset!!!")

                elif result==0:
                    print("No duplicates Found!!!!")
                else:
                    print(
                        f"\nDuplicates removed : {result['duplicates_removed']}\n"
                        f"Documents after     : {result['documents_after']}\n"
                        f"Chunks created      : {result['chunks_created']}\n"
                        f"Embeddings created  : {result['embeddings_created']}"
                    )

            case 3:
                question=input("prompt:").strip()

                if not question:
                    print("Question cannot be empty.")
                    continue
                try:
                    answer = rag_obj.ask(question)

                except GeneratorError:
                    print("Unable to generate an answer. Please try again.")
                    continue

                if not answer:
                     print("Something Happend.Try Again")
                     continue
            
                print("\n")
                print("Answer:\n")
                print(answer)
                print("\n")
            
            case 4:
                pipline=AnalyticsPipeline(config=config)
                report_obj=pipline.build_report()
                if not report_obj:
                    print("Empty Report!!!")
                    continue
                result=report_obj.generate_text()
                print(result)

            case 5:
                exit()
                




