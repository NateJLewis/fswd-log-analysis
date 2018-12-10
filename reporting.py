#!/usr/bin/env python
#
# reporting.py -- implementation of a reporting system for a news company.
#

from reportingdb import *

def on_print_title(title):
    print '{title}'.format(title=title)

def on_print_separator():
    print '------------------------------------------------'

def get_top_three_articles():
    """
    Question 1 -
    Return the top three articles of all time.
    """
    query = '''\
        SELECT title, views
        FROM viewed_articles
        ORDER BY views desc
        LIMIT 3;
    '''
    db = on_db_connect()
    c = db.cursor()
    c.execute(query)
    data = c.fetchall()
    db.close()
    on_print_title('\nBelow are the top three most popular articles of all time.')
    on_print_separator()
    for (title, views) in data:
        print '  * {title} - {views} views'.format(title=title, views=views)


def get_top_article_authors():
    """
    Question 2 -
    Return the top article authors of all time.
    """
    query = '''\
        SELECT log.author, log.views
        FROM (
            SELECT author, sum(views) as views
            FROM viewed_articles
            GROUP BY author
        ) as log
        ORDER BY log.views desc
        LIMIT 5;
    '''
    db = on_db_connect()
    c = db.cursor()
    c.execute(query)
    data = c.fetchall()
    db.close()
    on_print_title('\nBelow are the top article authors of all time.')
    on_print_separator()
    for (author, views) in data:
        print '  * {author} - {views} views'.format(author=author, views=views)

def get_request_error_stats():
    """
    Question 3 -
    Show the days where the request errors are more than 1% of the views
    """
    query = '''\
        SELECT a.date, ((b.count * 100 / (b.count + a.count)) ) as percent
        FROM success_by_date as a
        LEFT JOIN error_by_date as b
        ON a.date = b.date
        WHERE b.count > 0
        ORDER BY percent desc
        LIMIT 5;
    '''
    db = on_db_connect()
    c = db.cursor()
    c.execute(query)
    data = c.fetchall()
    db.close()
    on_print_title('\nBelow are the top article authors of all time.')
    on_print_separator()
    for (date, percent) in data:
        print '  * {date} - {percent} percent\n'.format(date=date, percent=percent)

if __name__ == '__main__':
    on_remove_view('viewed_articles', 'Removing articles report view...')
    on_remove_view('success_by_date', 'Removing view of success requests by date...')
    on_remove_view('error_by_date', 'Removing view of error requests by date...')
    on_create_viewed_articles()
    on_create_success_by_date()
    on_create_error_by_date()
    get_top_three_articles()
    get_top_article_authors()
    get_request_error_stats()
    print "\nReporting completed"
