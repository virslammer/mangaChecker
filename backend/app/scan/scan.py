
import requests 
import shutil 
import os
import re
from requests_html import HTMLSession


URL_LIST = ["http://www.nettruyen.com/truyen-tranh/tu-la-kiem-ton-28123"]
MANGA_LIST = [
    {
        "manga_name":"tu la kiem ton",
        "last_chapter":0
    }
] 
class Scan():
    SESSION = HTMLSession()
    def __init__(self,last_chapter=0,url=None):
        self.url = url
        self.last_chapter = last_chapter # Shouldn't contain space
        self._r = self.SESSION.get(self.url)
        
        if self._r.status_code != 200:
            print(self._r.status_code)
            raise ValueError("Url error")

    def get_chapter_links(self):
        # OUTPUT >> return a list of chapter links
        # txt = "103 - http://www.nettruyen.com/truyen-tranh/tu-la-kiem-ton/chap-37/564699"
        # chapter_index = re.search(r"(chap-)(\d*)", txt)
        # if chapter_index:

        #     print(chapter_index.group(2))
        # else:
        #     print('chapter_index = none')
        chapter_class_list = self._r.html.find('.col-xs-5.chapter')
        list_links = [str(chapter.links.pop()) for chapter in chapter_class_list]
        result = {}
        for link in list_links:
            #txt = "103 - http://www.nettruyen.com/truyen-tranh/tu-la-kiem-ton/chap-37/564699"
            chapter_index = re.search(r"(chap-)(\d*)", link)
            if chapter_index:
                if int(chapter_index.group(2)) > self.last_chapter:
                    result[int(chapter_index.group(2))] = link 
            

        # for index,chapter in enumerate(chapter_class_list):
        #     if index > self.last_chapter:
        #         links.append(chapter.links)
        return result

s = Scan(last_chapter=140,url=URL_LIST[0])
chap_list = s.get_chapter_links()

for k,v in chap_list.items():
    print(str(k) + " - " + v)