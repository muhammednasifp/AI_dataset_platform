import requests
from bs4 import BeautifulSoup

response = requests.get(
    "https://docs.python.org/3/tutorial/"
)

soup = BeautifulSoup(
    response.text,
    "html.parser"
)

paragraphs = soup.find_all("p")

# print(len(paragraphs))

# for paragraph in paragraphs[:5]:
#     print(paragraph.text)
#     print("-" * 50)

content=""

for paragraph in paragraphs:
    content+=paragraph.text
    content+="\n"

print(content[:1000])
print(type(content))