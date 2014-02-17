#!/usr/bin/python3
# -*- coding: utf-8 -*-

from spyCommon import getSources
from urllib.request import urlopen
import feedparser_local as feedparser
import sys

def spyUpdate():
    sources = getSources()

    for source in sources:
        try:
            sys.stdout.write('<%d> %s [D] ' % (source['id'], source['feedUrl']))
            feedUrl = source['feedUrl']
            with urlopen(feedUrl) as u:
                data = u.read()

            sys.stdout.write('[P] ')
            feed = feedparser.parse(data)

            items = feed["items"]
            sys.stdout.write('[I%d] ' % len(items))

            sys.stdout.write('\u2713\n')

        except Exception as e:
            print('! Update error: %s' % e)
#            e.print_stack()
            break


if __name__ == '__main__':
    spyUpdate()


