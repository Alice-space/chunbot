import requests
from bs4 import BeautifulSoup
from source.base import Source


class IHEPEDUSource(Source):
    def description(self):
        return "高能物理研究所教育处通知公告"

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
