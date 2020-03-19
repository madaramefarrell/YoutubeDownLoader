import requests
from bs4 import BeautifulSoup

request = requests.get('https://www.youtube.com/results?search_query=pitbull')
context = request.content

soup = BeautifulSoup(context, "html.parser")

print(soup)


