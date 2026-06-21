from dataclasses import asdict
import pandas as pandas_obj

class DocumentConverter:

    def __init__(self,documents):
        self.documents=documents
    
    def  documents_to_dataframe(self):
        document_dict=[]

        for documnet in self.documents:
            document_dict.append(asdict(documnet))

        for document in document_dict:
            document["word_count"]=document["metadata"]["word_count"]
            document["char_count"]=document["metadata"]["char_count"]

        df=pandas_obj.DataFrame(document_dict)

        return df
