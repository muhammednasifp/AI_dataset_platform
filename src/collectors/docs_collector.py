# -----------------------------------------------------------------------------
# DocsCollector
#
# Collects documents from web pages and converts them into structured Document
# objects for the dataset pipeline.
#
# Responsibilities:
# - Downloads HTML content from a given URL.
# - Extracts the page title.
# - Extracts paragraph text as the main document content.
# - Assigns a unique identifier to each document.
# - Creates a standardized Document object for downstream processing.
#
# Design Notes:
# - Acts as the data ingestion layer of the pipeline.
# - Keeps web scraping separate from validation, cleaning, and storage.
# - Returns a Document object on success or None if the request fails.
# - Can be extended to support multiple websites, content extraction rules,
#   retries, request timeouts, and metadata collection.
# -----------------------------------------------------------------------------
import requests
import uuid
from bs4 import BeautifulSoup
from src.models.document import Document

class DocsCollector:
    
    def collect(self,url):
        response=requests.get(url)

        if response.status_code!=200:
            return None
        
        soup=BeautifulSoup(
            response.text,
            "html.parser"
        )

        if soup.title:
            title=soup.title.text
        else:
            title="untitled"
        
        paragraphs=soup.find_all("p")

        content=""

        for paragraph in paragraphs:
            content+=paragraph.text
            content+="\n"
    
        id=str(uuid.uuid4())

        doc=Document(id=id,title=title,url=url,content=content,source="python_doc")
        
        return doc

# col=DocsCollector()

# doc=col.collect(
#     "https://docs.python.org/3/tutorial/"
# )

# print(doc.id)
# print(doc.title)
# print(doc.url)
# print(doc.content)
# print(doc.source)