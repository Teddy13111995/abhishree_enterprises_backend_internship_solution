import json
import sys

import requests
from bs4 import BeautifulSoup
import csv
import sqlite3


def main():
    url = "https://www.theverge.com/"
    page = None
    # request for web page
    try:
        page = requests.get(url)
    except Exception as e:

        error_type, error_obj, error_info = sys.exc_info()
        print('ERROR FOR LINK:', url)

        print(error_type, 'Line:', error_info.tb_lineno)

    # converting given web page to viewable content
    soup = BeautifulSoup(page.content, 'html.parser')
    # getting script for all urls
    script = soup.find_all('script')[23].text.strip()
    data = json.loads(script)
    placement_list = data['props']['pageProps']['hydration']['responses'][0]['data']['community']['frontPage'][
        'placements']

    i = 0
    conn = sqlite3.connect('test_database')
    c = conn.cursor()
    c.execute('''
              CREATE TABLE IF NOT EXISTS news_articles
              ([id] INTEGER PRIMARY KEY, [url] TEXT, [headline] TEXT, [author] TEXT, [date] TEXT)
              ''')
    with open('ddmmyyyy_verge.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "URL", "headline", "author", "date"])
        for element in placement_list:
            if element['placeable'] is not None:
                writer.writerow([i, element['placeable']['title'], element['placeable']['url'],
                                 element['placeable']['author']['fullName'], element['placeable']['publishDate'][0:10]])
                c.execute('''
                          INSERT INTO news_articles (id, URL,headline,author,date)
    
                                VALUES
                                (?,?,?,?,?)
                          ''', (i, element['placeable']['title'], element['placeable']['url'],
                                element['placeable']['author']['fullName'], element['placeable']['publishDate'][0:10]))
            else:
                continue
            i += 1
    c.close()


if __name__ == '__main__':
    main()
