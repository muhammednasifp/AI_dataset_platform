# -----------------------------------------------------------------------------
# DocumentConverter
#
# Converts a collection of Document objects into a pandas DataFrame for
# analytics, reporting, and data processing.
#
# Responsibilities:
# - Convert Document dataclass instances into dictionaries.
# - Extract useful metadata into top-level DataFrame columns.
# - Produce a tabular representation suitable for analysis with pandas.
#
# Design Notes:
# - Acts as a bridge between the application's object model and the pandas
#   ecosystem.
# - Keeps data conversion separate from analytics and storage.
# - Can be extended to flatten additional metadata fields or export to
#   formats such as CSV or Parquet.
# -----------------------------------------------------------------------------
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
