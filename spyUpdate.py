#!/usr/bin/python3
# -*- coding: utf-8 -*-

from spyCommon import getSources
from urllib.request import urlopen
import feedparser_local as feedparser
import sys
import pdb

def spyUpdate():
    sources = getSources()

    for source in sources:
        try:
            sys.stdout.write('<%d> %s' % (source['id'], source['feedUrl']))
            feedUrl = source['feedUrl']
            with urlopen(feedUrl) as u:
                data = u.read()

            feed = feedparser.parse(data)

            pdb.set_trace()

            updateSourceAttributes(
                                   source['id'],
                                   source['overrideTitle'] if source['overrideTitle'] else feed['title'],
                                   feed['link'])

            items = feed["items"]
            for item in items:
                updateItem(source, item)
                break

            sys.stdout.write(' ✓\n')

        except Exception as e:
            print('! Update error: %s' % repr(e))
            try: e.print_stack()
            except: print("No stack trace!") 
            break

def updateSourceAttributes(sourceid, newtitle, newlink):
    cursor = spyCommon.getDBcursor()
    cursor.execute('UPDATE sources SET title = %s, link = %s WHERE id = %s', newtitle, newlink, sourceid)

def updateItem(source, item):
    sid = source['id']

    itemtoenter = {}

    try:
        itemtoenter['title'] = item['title']
    except:
        print(item['feed']['title'])
        itemtoenter['title'] = item['feed']['title']

    itemtoenter['guid'] = item['url'] if source['ignoreGuid'] else item['guid']
    # itemtoenter['link'] = item['link']

    print(itemtoenter)


if __name__ == '__main__':
    spyUpdate()


