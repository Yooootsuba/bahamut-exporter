
import re
import requests
import responses
from pytest import raises
from unittest import TestCase
from bs4 import BeautifulSoup
from bahamutexporter.main import BamahutExporterTest
from bahamutexporter.core.service import BamahutExporterService

def test_bahamutexporter():
    # test bahamutexporter without any subcommands or arguments
    with BamahutExporterTest() as app:
        app.run()
        assert app.exit_code == 0


def test_bahamutexporter_debug():
    # test that debug mode is functional
    argv = ['--debug']
    with BamahutExporterTest(argv=argv) as app:
        app.run()
        assert app.debug is True


@responses.activate
def test_bahamutexporterservice_is_last_page():
    with open('tests/fixtures/bsn60111-snA121565.html') as f:
        responses.add(
            method = responses.GET,
            url    = 'https://forum.gamer.com.tw/C.php',
            match  = [responses.matchers.query_string_matcher('bsn=60111&snA=121565&page=1')],
            body   = f.read()
        )

        f.seek(0)

        responses.add(
            method = responses.GET,
            url    = 'https://forum.gamer.com.tw/C.php',
            match  = [responses.matchers.query_string_matcher('bsn=60111&snA=121565&page=2')],
            body   = f.read()
        )

    service  = BamahutExporterService()

    response = requests.get('https://forum.gamer.com.tw/C.php', params = {'bsn': '60111', 'snA': '121565', 'page': '1'})
    assert service.is_last_page(1, response) is False

    response = requests.get('https://forum.gamer.com.tw/C.php', params = {'bsn': '60111', 'snA': '121565', 'page': '2'})
    assert service.is_last_page(2, response) is True


@responses.activate
def test_bahamutexporterservice_parse_replies():
    with open('tests/fixtures/bsn60111-snB362133.json') as f:
        responses.add(
            method = responses.GET,
            url    = 'https://forum.gamer.com.tw/ajax/moreCommend.php',
            match  = [responses.matchers.query_string_matcher('bsn=60111&snB=362133')],
            body   = f.read()
        )

        responses.add(
            method = responses.GET,
            url    = 'https://forum.gamer.com.tw/ajax/moreCommend.php',
            match  = [responses.matchers.query_string_matcher('bsn=60111&snB=362139')],
            body   = '{"next_snC": 0}'
        )

    service = BamahutExporterService()

    TestCase().assertListEqual(
        service.parse_replies('60111', '362133'),
        [
            {
                'nickname' : 'Yotsuba',
                'datetime' : '2022-01-03 10:54:29',
                'content'  : '2',
            },
            {
                'nickname' : 'Yotsuba',
                'datetime' : '2022-01-03 10:54:32',
                'content'  : '3',
            },
        ]
    )

    TestCase().assertListEqual(
        service.parse_replies('60111', '362139'),
        []
    )


@responses.activate
def test_bahamutexporterservice_parse_floor():
    with open('tests/fixtures/bsn60111-snA121565.html') as f:
        responses.add(
            method = responses.GET,
            url    = 'https://forum.gamer.com.tw/C.php',
            match  = [responses.matchers.query_string_matcher('bsn=60111&snA=121565&page=1')],
            body   = f.read()
        )

    with open('tests/fixtures/bsn60111-snB362133.json') as f:
        responses.add(
            method = responses.GET,
            url    = 'https://forum.gamer.com.tw/ajax/moreCommend.php',
            match  = [responses.matchers.query_string_matcher('bsn=60111&snB=362133')],
            body   = f.read()
        )

    service  = BamahutExporterService()
    response = requests.get('https://forum.gamer.com.tw/C.php', params = {'bsn': '60111', 'snA': '121565', 'page': '1'})
    soup     = BeautifulSoup(response.text, 'html.parser')

    TestCase().assertDictEqual(
        service.parse_floor('60111', soup.find('section', {'class': 'c-section', 'id': re.compile('.*')})),
        {
            'floor'    : '樓主',
            'username' : 'happy819tw',
            'nickname' : 'Yotsuba',
            'datetime' : '2022-01-02 12:08:51',
            'content'  : '1',
            'replies'  : [
                {
                    'nickname' : 'Yotsuba',
                    'datetime' : '2022-01-03 10:54:29',
                    'content'  : '2',
                },
                {
                    'nickname' : 'Yotsuba',
                    'datetime' : '2022-01-03 10:54:32',
                    'content'  : '3',
                },
            ]
        }
    )


@responses.activate
def test_bahamutexporterservice_export():
    with open('tests/fixtures/bsn60111-snA121565.html') as f:
        responses.add(
            method = responses.GET,
            url    = 'https://forum.gamer.com.tw/C.php',
            match  = [responses.matchers.query_string_matcher('bsn=60111&snA=121565&page=1')],
            body   = f.read()
        )

        f.seek(0)

        responses.add(
            method = responses.GET,
            url    = 'https://forum.gamer.com.tw/C.php',
            match  = [responses.matchers.query_string_matcher('bsn=60111&snA=121565&page=2')],
            body   = f.read()
        )

    with open('tests/fixtures/bsn60111-snB362133.json') as f:
        responses.add(
            method = responses.GET,
            url    = 'https://forum.gamer.com.tw/ajax/moreCommend.php',
            match  = [responses.matchers.query_string_matcher('bsn=60111&snB=362133')],
            body   = f.read()
        )

        responses.add(
            method = responses.GET,
            url    = 'https://forum.gamer.com.tw/ajax/moreCommend.php',
            match  = [responses.matchers.query_string_matcher('bsn=60111&snB=362139')],
            body   = '{"next_snC": 0}'
        )

    service = BamahutExporterService()

    TestCase().assertListEqual(
        service.export('60111', '121565'),
        [
            {
                'floor'    : '樓主',
                'username' : 'happy819tw',
                'nickname' : 'Yotsuba',
                'datetime' : '2022-01-02 12:08:51',
                'content'  : '1',
                'replies'  : [
                    {
                        'nickname' : 'Yotsuba',
                        'datetime' : '2022-01-03 10:54:29',
                        'content'  : '2',
                    },
                    {
                        'nickname' : 'Yotsuba',
                        'datetime' : '2022-01-03 10:54:32',
                        'content'  : '3',
                    },
                ]
            },
            {
                'floor' : '2 樓',
                'hint'  : '此文章已由原作者(happy819tw)刪除',
            },
            {
                'floor'    : '3 樓',
                'username' : 'happy819tw',
                'nickname' : 'Yotsuba',
                'datetime' : '2022-01-02 14:49:22',
                'content'  : '4',
                'replies'  : [],
            },
        ]
    )
