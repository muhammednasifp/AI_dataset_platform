import requests
from bs4 import BeautifulSoup

response=requests.get("https://docs.python.org/3/tutorial/")

soup=BeautifulSoup(
    response.text,
    "html.parser"
)

#print(soup.title) look for title tag in the html
paragraphs=soup.find_all("p")

for paragraph in paragraphs:
    print(paragraph.text)

