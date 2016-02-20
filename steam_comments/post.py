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
        self.count = None
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

        self.count = int(re.sub(r'[^0-9]+', '', count.text))
        return self.count

    def comments(self):
        for page in self.pages():
            for c in page:
                yield c

    def pages(self):
        if self.count is None:
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

            f['comments_html'] = re.sub(r"[\n\t\r]", "", f['comments_html'])

            comments = []

            if f['comments_raw']:
                b = BeautifulSoup(f['comments_html'], 'html.parser')
                for post in b.find_all('div', class_="commentthread_comment"):
                    pid = int(re.search('comment_(?P<id>\d+)', post.attrs['id']).group('id'))
                    user_wrapper = post.find('div', class_='commentthread_comment_avatar')
                    profile_url = user_wrapper.find('a').attrs['href']
                    image_url = re.search(', (.*?) 2x', user_wrapper.find('img').attrs['srcset']).group(1)
                    text = str(post.find('div', class_='commentthread_comment_text'))
                    author = post.find('bdi').text
                    comments.append(dict(profile_url=profile_url, image_url=image_url, text=text, id=pid, author=author))

                counter += 50
                yield comments
            else:
                self.stop = True
