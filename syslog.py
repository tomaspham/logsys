#!/usr/bin/env python3

import psycopg2

# 1. What are the most popular three articles of all time?
top_articles_sql = """
                        SELECT articles.title, COUNT(*) AS counter
                        FROM log, articles
                        WHERE log.status='200 OK'
                        AND articles.slug = SUBSTR(log.path, 10)
                        GROUP BY articles.title
                        ORDER BY counter DESC LIMIT 3;
                     """

# 2. Who are the most popular article authors of all time?
top_authors_sql = """ SELECT authors.name, COUNT(*) AS counter 
                FROM articles, authors, log 
                WHERE log.status='200 OK'
                AND authors.id = articles.author
                AND articles.slug = SUBSTR(log.path, 10)
                GROUP BY authors.name
                ORDER BY counter DESC;
            """

# 3. On which days did more than 1% of requests lead to errors?
request_errors_sql = """
                    SELECT time, percentage_fail
                    FROM vw_percentage_counter
                    WHERE percentage_fail > 1;
                """


# Run Sql
def run_sql(sql):
    connector = psycopg2.connect(database="news")
    cursor = connector.cursor()
    cursor.execute(sql)
    records = cursor.fetchall()
    connector.close()
    return records


# Generate output
def generate_title(title):
    print("\n" + title + "\n")


# Generate top three articles
def top_articles():
    articles = run_sql(top_articles_sql)
    generate_title("Top 3 articles")

    for title, num in articles:
        print(" \"{}\" -- {} views".format(title, num))


# Generate top authors
def top_authors():
    authors = run_sql(top_authors_sql)
    generate_title("Top authors")

    for name, num in authors:
        print(" {} -- {} views".format(name, num))


# Generate days with more than 1% bad requests
def error_days():
    error_days = run_sql(request_errors_sql)
    generate_title("Days with more than one percentage of bad requests")

    for day, percentage_fail in error_days:
        print("""{0:%B %d, %Y} -- {1:.2f} % errors""".format(day, percentage_fail))


if __name__ == '__main__':
    top_articles()
    top_authors()
    error_days()
