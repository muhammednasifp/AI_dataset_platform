import pandas as pd
#Eg:-
# data=[
#     {'name':'nasif','age':20},
#     {"name": "Alice", "age": 22}
# ]

# df=pd.DataFrame(data=data) # Pandas DataFrame
# print(df)
# Pandas DataFrame
# A table-like data structure.
#
# Similar to:
# - Excel spreadsheet
# - SQL table
#
# Rows = records
# Columns = attributes

#output:-
#     name  age
# 0  nasif   20
# 1  Alice   22

from src.storage.jsonl_store import  JSONLStore
from dataclasses import asdict

store=JSONLStore("data/raw/documents.jsonl")

documents=store.read_all()

document_dict=[]

for documnet in documents:
    document_dict.append(asdict(documnet))

for document in document_dict:
    document["word_count"]=document["metadata"]["word_count"]
    document["char_count"]=document["metadata"]["char_count"]

# Flattened DataFrame
#
# Nested metadata fields are promoted to columns.
#
#Eg:-
#[[1, 2], [3, 4]] into a single flat list [1, 2, 3, 4].

df=pd.DataFrame(document_dict)

# Object -> DataFrame Pipeline
#
# Document Object
#       ↓
# asdict()
#       ↓
# Dictionary
#       ↓
# DataFrame Row
#
# Common Data Engineering pattern.


# print(df)

print(df["word_count"].mean())
print(df["word_count"].max())
print(df["word_count"].min())
print(df["word_count"].count())

# Aggregation Functions
#
# mean()  -> Average
# max()   -> Maximum
# min()   -> Minimum
# count() -> Number of records
#

# print(df[df["word_count"] == df["word_count"].max()])

# print(df.loc[df["word_count"].idxmax()])
# print(df.loc[df["word_count"].idxmin()])

# idxmax()
# Returns the index of the largest value
# in a column.
#
#idxmin
#Returns the index of the smallest value
# Useful for retrieving the complete row
#
#loc[]
#returns the entire row.
#


df.to_parquet(
    "data/processed/documents.parquet",
    index=False
)
# to_parquet()
# Saves a DataFrame to a Parquet file.
#
# DataFrame
#      ↓
# Parquet File
#
# Used for efficient storage and analytics.
# index=False
# Prevents the DataFrame index from being
# saved to the Parquet file.


df2=pd.read_parquet(
    "data/processed/documents.parquet"
)
# read_parquet()
# Reads a Parquet file into a DataFrame.
#
# Parquet File
#      ↓
# DataFrame

print(df2)







