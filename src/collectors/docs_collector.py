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