import re
import html
import json
import requests
from bs4 import BeautifulSoup

class BamahutExporterService:


    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'})


    def is_last_page(self, page, response):
        return page > int(re.search('var args =.*page=([0-9]+)', response.text).group(1))


    def parse_replies(self, bsn, snB):
        replies  = []
        response = self.session.get('https://forum.gamer.com.tw/ajax/moreCommend.php', params = {'bsn': bsn, 'snB': snB}).json()
        response.pop('next_snC')

        for reply in response.values():
            replies.append(
                {
                    'username' : reply['userid'],
                    'nickname' : reply['nick'],
                    'datetime' : reply['wtime'],
                    'content'  : reply['content'],
                    'comment'  : html.escape('{"content":"%s"}' % reply['content']),
                }
            )

        replies.reverse()

        return replies


    def parse_floor(self, bsn, floor):
        if (hint := floor.find('div', {'class': 'hint'})) is not None:
            return {
                'floor' : floor.find('div', {'class': 'floor'}).text,
                'hint'  : hint.text,
            }
        else:
            return {
                'floor'    : floor.find('a', {'class': 'floor tippy-gpbp'}).text,
                'username' : floor.find('a', {'class': 'userid'}).text,
                'nickname' : floor.find('a', {'class': 'username'}).text,
                'datetime' : floor.find('a', {'class': 'edittime tippy-post-info'}).get('data-mtime'),
                'content'  : floor.find('div', {'class': 'c-article__content'}),
                'replies'  : self.parse_replies(bsn, floor.get('id').replace('post_', '')),
            }


    def export(self, bsn, snA):
        page   = 0
        floors = []

        while True:
            # Get page
            page    += 1
            response = self.session.get('https://forum.gamer.com.tw/C.php', params = {'bsn': bsn, 'snA': snA, 'page': page})
            soup     = BeautifulSoup(response.text, 'html.parser')

            # Break loop when the page is last
            if self.is_last_page(page, response):
                return floors

            # Get floors
            for floor in soup.find_all('section', {'class': 'c-section', 'id': re.compile('.*')}):
                floors.append(self.parse_floor(bsn, floor))
