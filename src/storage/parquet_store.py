# Parquet
# A columnar storage format optimized for analytics.
#
# Advantages:
# - Smaller file size
# - Faster reads
# - Efficient column operations
#
# Widely used in Data Engineering and ML pipelines.

from src.storage.jsonl_store import  JSONLStore
from src.converters.document_converter import DocumentConverter
import pandas as pd
import os

class ParquetStore:
    
    def __init__(self,path):
        self.path=path

    def save_dataframe(self,df):
        directory = os.path.dirname(self.path)

        # os.path.dirname()
        # Extracts the parent directory from a file path.
        #
        # Example:
        # "data/processed/file.parquet"
        # ->
        # "data/processed"
        #
        # Useful when creating directories before
        # saving files.
        
        os.makedirs(
            directory,
            exist_ok=True
        )
       
        # os.makedirs()
        # Creates directories if they do not exist.
        #
        # exist_ok=True prevents errors if the
        # directory already exists.
        #
        # Common practice before writing files.

        df.to_parquet(
            self.path,
            index=False
        )   

    def read_dataframe(self):

        return pd.read_parquet(
            self.path
        )


# store=JSONLStore("data/raw/documents.jsonl")
# documents=store.read_all()
# ps_obj=ParquetStore('data/processed/documents.parquet')
# dc_obj=DocumentConverter(documents=documents)
# df=dc_obj.documents_to_dataframe()
# print(ps_obj.read_dataframe())
# ps_obj.save_dataframe(df=df)