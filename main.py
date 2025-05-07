import requests
from bs4 import BeautifulSoup

def parse_ihep_edu():
    response = requests.get("https://edu1.ihep.ac.cn/tzgg/index.shtml")
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    items = []
    for li in soup.select('.mainListbox .ulList li'):
        a = li.find('a')
        title = a.get_text(strip=True)
        link = a['href']
        items.append({'title': title, 'link': link})
        print({'title': title, 'link': link})

if __name__ == '__main__':
    data = parse_ihep_edu()
