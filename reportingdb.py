#!/usr/bin/env python
#
# reporting.py -- implementation of a reporting system for a news company.
#

import psycopg2

DBNAME = 'news'

def on_db_connect():
    return psycopg2.connect(database=DBNAME)

def on_remove_view(view, message):
    query = 'DROP VIEW IF EXISTS {};'.format(view)
    print '{}'.format(message)
    db = on_db_connect()
    c = db.cursor()
    c.execute(query)
    db.commit()
    db.close()
    print 'DONE.\n'

def on_create_viewed_articles():
    print 'Adding articles report view...'
    query = '''\
        CREATE view viewed_articles as
        SELECT articles.title, articles.slug as slug, authors.name as author, log.count as views
        FROM (
            SELECT path, count(path) as count
            FROM log
            WHERE path LIKE '/article/%'
            AND method = 'GET'
            AND status = '200 OK'
            GROUP BY path
        ) as log
        LEFT JOIN articles ON articles.slug = split_part(log.path, '/article/', 2)
        LEFT JOIN authors ON authors.id = articles.author
        WHERE 1=1
        ORDER BY views desc;
    '''
    db = on_db_connect()
    c = db.cursor()
    c.execute(query)
    db.commit()
    db.close()
    print 'DONE.\n'

def on_create_success_by_date():
    print 'Adding aggregated list of successful requests by date...'
    query = '''\
        CREATE view success_by_date as
        SELECT a.date, a.count
        FROM (
            SELECT DATE(time) as date, count(status) as count
            FROM log
            WHERE status LIKE '404%'
            GROUP BY date
        ) as a
        WHERE 1=1
        ORDER BY date desc;
    '''
    db = on_db_connect()
    c = db.cursor()
    c.execute(query)
    db.commit()
    db.close()
    print 'DONE.\n'

def on_create_error_by_date():
    print 'Adding aggregated list of error requests by date...'
    query = '''\
        CREATE view error_by_date as
        SELECT a.date, a.count
        FROM (
            SELECT DATE(time) as date, count(status) as count
            FROM log
            WHERE status LIKE '200%'
            GROUP BY date
        ) as a
        WHERE 1=1
        ORDER BY date desc;
    '''
    db = on_db_connect()
    c = db.cursor()
    c.execute(query)
    db.commit()
    db.close()
    print 'DONE.\n'
