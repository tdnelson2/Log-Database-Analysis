#!/usr/bin/env python3

import psycopg2
from functools import wraps


def connect():
    """Connect to the PostgreSQL database. Returns a database connection."""
    return psycopg2.connect("dbname=news")


def establishConnection(func):
    """
    A decorator to establish database connection
    and create a cursor.
    """
    @wraps(func)
    def wrap(*args, **kwargs):
        if len(args) != 2:
            db = connect()
            args = (db, db.cursor())
            kwargs['shouldClose'] = True
        return func(*args, **kwargs)
    return wrap


def runQuery(statement, db, c, shouldClose):
    c.execute(statement)
    rows = c.fetchall()
    if shouldClose:
        db.close
    return rows


@establishConnection
def topThreeArticles(db, c, shouldClose=False):
    """
    Returns three most popular articles in descending order.

    Returns:
      A list of tuples, each of which contains (title, total):
        title: the article's title
        total: the total number of views
    """
    return runQuery("SELECT title, total FROM popular_articles LIMIT 3;",
                    db, c, shouldClose)


@establishConnection
def popularAuthors(db, c, shouldClose=False):
    """
    Returns all authors in decending order sorted by popularity.

    Returns:
      A list of tuples, each of which contains (name, total):
        name: the author's name
        total: the total page views for all articles by the author
    """
    return runQuery("SELECT name, total FROM popular_authors;",
                    db, c, shouldClose)


@establishConnection
def requestErrorsExceedingOnePercent(db, c, shouldClose=False):
    """
    Returns days where more than 1% of requests lead to errors.

    Returns:
      A list of tuples, each of which contains (date, error_percentage):
        date: the date using Month DD, yyyy format
        error_percentage: the percentage of requests which resulted in errors
    """
    return runQuery("""SELECT
                         TO_CHAR(day, 'Month DD, yyyy') AS date,
                         TO_CHAR(error_rate*100, '9.9%') AS error_percentage
                       FROM errors_by_days
                       WHERE error_rate > 0.01;""",
                    db, c, shouldClose)


def main():
    '''Generate the report.'''
    db = connect()
    c = db.cursor()

    topArticles = topThreeArticles(db, c)
    print('Most popular three articles of all time:')
    for article in topArticles:
        print('"{}" — {} views'.format(article[0], article[1]))

    popAuthors = popularAuthors(db, c)
    print('\nMost popular article authors of all time:')
    for author in popAuthors:
        print('{} — {} views'.format(author[0], author[1]))

    errorRate = requestErrorsExceedingOnePercent(db, c)
    print('\nDays in which more than 1% of requests lead to errors:')
    for error in errorRate:
        print('{} — {} errors'
              .format(error[0], error[1])
              .replace('      ', ' '))

    db.close


if __name__ == "__main__":
    main()
