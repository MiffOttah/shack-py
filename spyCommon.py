#!/usr/bin/python
# -*- coding: utf-8 -*-

import pymysql
import sys

DB = pymysql.connect('ebreeze', 'shack-be', 'WXpn788TG29PqB9H', 'shack-be')

def getSources():
    global DB
    cursor = DB.cursor(pymysql.cursors.DictCursor)

    sWhat = 'all'
    sN = 1
    if sys.argv and len(sys.argv) >= 2:
        sWhat = sys.argv[1]
        if not sWhat: sWhat = 'all'
        if len(sys.argv) >= 3 and sys.argv[2]:
            try:
                sN = int(sys.argv[2], 10)
                if sN < 1: sN = 1
            except:
                sN = 0

    if sWhat == 'oldest':
        cursor.execute('SELECT * FROM sources ORDER BY lastUpdate ASC LIMIT %s', (sN))
    elif sWhat == 'newest':
        cursor.execute('SELECT * FROM sources ORDER BY lastUpdate DESC LIMIT %s', (sN))
    elif sWhat == 'id':
        cursor.execute('SELECT * FROM sources WHERE id = %s LIMIT 1', (sN))
    elif sWhat == 'errors':
        cursor.execute('SELECT * FROM sources WHERE fetchError IS NOT NULL')
    else:
        cursor.execute('SELECT * FROM sources ORDER BY id')

    return cursor.fetchall()


