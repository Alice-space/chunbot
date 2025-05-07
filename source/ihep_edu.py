import requests
from bs4 import BeautifulSoup
from base import Source

class IHEPEDUSource(Source):
    def get_list(self) -> dict[str, str]:
        resp = requests.get("https://edu1.ihep.ac.cn/tzgg/index.shtml")
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        items = {}
        for li in soup.select(".mainListbox .ulList li"):
            a = li.find("a")
            title = a.get_text(strip=True)
            link = a["href"]
            if link.startswith("/"):
                link = "https://edu1.ihep.ac.cn" + link
            items[title] = link
        return items

    def get_detail(self, url):
        return super().get_detail(url)

if __name__ == "__main__":
    ihep_edu = IHEPEDUSource()
    print(ihep_edu.get_list())