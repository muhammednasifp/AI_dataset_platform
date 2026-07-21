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

import logging
import requests
import uuid
from bs4 import BeautifulSoup
from src.exceptions.collector import DocumentCollectionError
from src.models.document import Document

logger = logging.getLogger(__name__)

class DocsCollector:
    
    def collect(self,url): 

        logger.info("Collecting document from %s", url)

        try:
            response = requests.get(url)

        except requests.RequestException as e:

            logger.exception(
                "Failed to download %s",
                url
            )

            raise DocumentCollectionError(
                f"Unable to download document from {url}"
            ) from e

        if response.status_code != 200:

            logger.error(
                "HTTP %d returned for %s",
                response.status_code,
                url
            )

            raise DocumentCollectionError(
                f"HTTP {response.status_code} returned for {url}"
        )
        
        logger.info("Successfully downloaded page")

        soup=BeautifulSoup(
            response.text,
            "html.parser"
        )

        if soup.title:
            title=soup.title.text
        else:
            logger.warning("Page has no title. Using default title.")
            title="untitled"

        paragraphs=soup.find_all("p")
        
        if not paragraphs:
            logger.warning(
                "No paragraph tags found in %s",
                url
            )
        

        content=""

        for paragraph in paragraphs:
            content+=paragraph.text
            content+="\n"
    
        id=str(uuid.uuid4())

        doc=Document(id=id,title=title,url=url,content=content,source="python_doc")
        
        logger.info(
            "Document created successfully (id=%s)",
             doc.id
        )

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