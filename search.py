#!/usr/bin/env python2

from BeautifulSoup import BeautifulSoup
import re
import json
import requests


_show_data = None
pattern = re.compile(r'S(\d\d)E(\d\d)|(\d+)x(\d+)')


def shows_url():
    return ''.join(['h', 't', 't', 'p', 's', ':', '/', '/', 'e', 'z', 't', 'v',
                    '.', 'a', 'g', '/', 'j', 's', '/', 's', 'e', 'a', 'r', 'c',
                    'h', '_', 's', 'h', 'o', 'w', 's', '1', '.', 'j', 's'])


def search_url():
    return ''.join(['h', 't', 't', 'p', 's', ':', '/', '/', 'e', 'z', 't', 'v',
                    '.', 'a', 'g', '/', 's', 'e', 'a', 'r', 'c', 'h', '/', '?',
                    'q', '1', '=', '&', 'q', '2', '=', '{', '}', '&', 's', 'e',
                    'a', 'r', 'c', 'h', '=', 'S', 'e', 'a', 'r', 'c', 'h'])


def show_data():
    global _show_data
    if _show_data:
        return _show_data
    show_data_request = requests.get(shows_url())
    json_data = show_data_request.text.split('[', 1)[1].split(']')[0]
    data = '{"data": [' + json_data + ']}'
    _show_data = json.loads(data)['data']
    return _show_data


def get_magnet_links(name, exact):
    show_id = -1
    for show in show_data:
        if exact and show['text'].lower() == name.lower():
            show_id = show['id']
            break
        elif not exact and show['text'].lower().find(name.lower()) != -1:
            show_id = show['id']
            break
    else:
        return {}
    r = requests.get(search_url().format(show_id))
    result = {}
    soup = BeautifulSoup(r.text)
    for link in soup.findAll('a'):
        attrs = dict(link.attrs)
        if not attrs.get('href'):
            continue
        if attrs.get('class', '') != 'magnet':
            continue
        title = attrs.get('title', '')
        if title.find('HDTV') == -1 or title.find('720') != -1:
            continue
        season, episode = ' '.join(pattern.findall(title)[0]).strip().split()
        season = ('0' + season.lstrip('0'))[-2:]
        episode = ('0' + episode.lstrip('0'))[-2:]
        season = result.setdefault(season, {})
        episode = season.setdefault(episode, [])
        episode.append(attrs['href'])
    return result


if __name__ == '__main__':
    from pprint import pprint
    import sys

    links = get_magnet_links(sys.argv[1], len(sys.argv) > 2 and
                             sys.argv[2] == 'exact')
    pprint(links)
