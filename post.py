from __future__ import unicode_literals
import logging
import requests
import re
import json
from bs4 import BeautifulSoup


class Post(object):
    stop = False

    def __init__(self, url="https://steamcommunity.com/groups/ns2rus/discussions/0/527273452871150509/"):
        self.url = url
        self.content = requests.get(url).content
        self.soup = BeautifulSoup(self.content, 'html.parser')
        self.prepare()

    def prepare(self):
        self.extended_data = re.search(r',"extended_data":"(.+)","oldestfirst"', self.content).group(1).replace("\\", "")
        self.session_id = re.search(r'g_sessionID = "(.+)";', self.content).group(1)

    def count_comments(self):
        try:
            wrapper = self.soup.find_all("div", class_="forum_paging_summary")[0]
            count = wrapper.find_all("span")[2]
        except IndexError, e:
            logging.error("Cant grab total comments. Url: %s. Error: %s" % (self.url, e))
            return 0

        if not wrapper or not count:
            return 0

        self.count = int(count.text)
        return self.count

    def comments(self):
        for page in self.pages():
            for c in page:
                yield c

    def pages(self):
        """
        Return json array
        comments_html: steam style html comments list
        comments_raw: dict of comments
            "527273452871477112": {
                "text": "Comment text",
                "author": "Comment author"
            }
        """
        if not self.count:
            self.count_comments()
        counter = 0
        while not self.stop:
            wrapper = self.soup.find_all("span", class_="commentthread_pagelinks")[0]
            id1, id2, id3 = wrapper.get('id').split('_')[2:5]
            query = {
                "start": counter,
                "totalcount": self.count,
                "count": 50,
                "sessionid": self.session_id,
                "extended_data": str(self.extended_data).replace('u"', '"'),
                "oldestfirst": False,
                "include_raw": True,
                "feature2": id3
            }

            url = "http://steamcommunity.com/comment/ForumTopic/render/%s/%s/" % (id1, id2)
            f = json.loads(requests.post(url, query).content)

            ordering = map(int, re.findall(r'id="comment\_(?P<id>\d+)"', f['comments_html']))
            f['comments_html'] = re.sub(r"[\n\t\r]", "", f['comments_html'])

            comments = []

            if f['comments_raw']:
                for pk, c in f['comments_raw'].items():
                    c['id'] = int(pk)

                    comments.append(c)
                    # Comment id cant be ordering key;D


                comments.sort(key=lambda x: ordering.index(x['id']))

                counter += 50
                yield comments
            else:
                self.stop = True
