import requests
from bs4 import BeautifulSoup

request = requests.get('https://www.youtube.com/results?search_query=pitbull')
context = request.content

soup = BeautifulSoup(context, "html.parser")

for element in soup.find_all('a', {'rel': "spf-prefetch"}):

    video_title = element.get('title')
    video_link= element.get('href')
    print(video_title)
    print("https://www.youtube.com/{}".format(video_link))
