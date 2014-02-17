#!/usr/bin/python3
# -*- coding: utf-8 -*-

from spyCommon import getSources

def spyList():
    sources = getSources()

    for source in sources:
        print('<%d> %s' % (source['id'], source['title']))
        print('    feedUrl: %s' % source['feedUrl'])
        print('    tags: %s' % source['tags'])
        if source['link']:
            print('    link: %s' % source['link'])
        print('    lastUpdate: %s' % source['lastUpdate'].strftime('%Y-%m-%d %H:%M:%S'))
        if source['fetchError']:
            print('    fetchError: %s' % (source['fetchError']))
        print('')

    print('%d sources in total' % len(sources))

if __name__ == '__main__':
    spyList()


