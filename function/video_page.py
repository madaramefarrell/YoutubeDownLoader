import re

import requests
from bs4 import BeautifulSoup

request = requests.get('https://www.youtube.com/results?search_query=pitbull')
context = request.content
soup = BeautifulSoup(context, "html.parser")
page = {}

for page_value in soup.find_all('a', {'class': True, 'data-visibility-tracking': True, 'data-sessionlink': True, 'aria-label': True,}):
    page['{}'.format(page_value.text)] = page_value.get('href')
print(page)
