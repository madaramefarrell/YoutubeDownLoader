import re

import requests
from bs4 import BeautifulSoup

request = requests.get('https://www.youtube.com/results?search_query=pitbull')
context = request.content
soup = BeautifulSoup(context, "html.parser")

for element in soup.find_all('a', {'rel': "spf-prefetch"}):

    img_value = element.get('href').split('=')[1]
    all_img = soup.find_all('img', {"alt": True, "width": True, "height": True, "onload": True, "data-ytimg": True})
    img = re.findall("https://i.ytimg.com/vi/{}/[\S]+".format(img_value), str(all_img))
    img = str(img).strip("[\"\']")
    video_img = img.replace("&amp;", "&")
    print(video_img)
