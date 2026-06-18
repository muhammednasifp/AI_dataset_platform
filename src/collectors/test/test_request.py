import requests

response=requests.get("https://docs.python.org/3/tutorial/")

if response.status_code==200:
    print(response.text[:500])