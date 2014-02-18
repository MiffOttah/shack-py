#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime
from dateutil.parser import parse
from urllib.request import urlopen

import feedparser_local as feedparser
import html
import pdb
import spyCommon
import sys
import traceback

def spyUpdate():
    sources = spyCommon.getSources()

    for source in sources:
        try:
            print('<{0}> {1}'.format(source['id'], source['feedUrl']))
            feedUrl = source['feedUrl']
            with urlopen(feedUrl) as u:
                data = u.read()

            feed = feedparser.parse(data)

            #with open('feed.json', 'w') as dbgjson:
            #    json.dump(feed['feed'], dbgjson)

            feedLink = None
            for l in feed['feed']['links']:
                if l['rel'] == 'alternate':
                    feedLink = l['href']
                    break

            source['title'] = source['overrideTitle'] if source['overrideTitle'] else feed['feed']['title']

            updateSourceAttributes(
                                   source['id'],
                                   source['title'],
                                   feedLink)
    
            items = feed["entries"]
            for item in items:
                updateItem(source, item)
                break


        except Exception as e:
            print('! Update error: {0}'.format(repr(e)))
            try: traceback.print_exc()
            except: print("No stack trace!") 
            break

def updateSourceAttributes(sourceid, newtitle, newlink):
    cursor = spyCommon.getDBcursor()
    cursor.execute('UPDATE sources SET title = %s, link = %s WHERE id = %s', (newtitle, newlink, sourceid))

def updateItem(source, item):
    sid = source['id']

    itemtoenter = {}

    try:
        itemtoenter['title'] = item['title']
    except:
        itemtoenter['title'] = source['title']

    itemtoenter['guid'] = item['link'] if source['ignoreGuid'] else item['guid']
    itemtoenter['link'] = item['link']
    itemtoenter['publishedAt'] = parse(item['published'])

    if source['linkOnlyFeed']:
        itemtoenter['content'] = mkLofContent(itemtoenter['link'])
    elif len(item['content']) > 0:
        itemtoenter['content'] = item['content'][0]['value']
    else:
        itemtoenter['content'] = item['summary']

    print(itemtoenter)

def makeLofContent(url):
    urlescaped = html.escape(url)
    return '<p class="shack-be_linkonlyfeed"><a href="{0}">{0}</a></p>'.format(urlescaped)


if __name__ == '__main__':
    spyUpdate()


