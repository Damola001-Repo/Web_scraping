import os
import requests
import selectorlib
import sqlite3
from smtplib import SMTP_SSL
# from threading import Thread

URL = 'https://programmer100.pythonanywhere.com/tours/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

connection = sqlite3.connect('db2.db')

def scrape(url):
    response = requests.get(url=url, headers=HEADERS)
    source = response.text
    return source

def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)['tours']
    return value

def store(extracted):
    row = extracted.split(',')
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    print('Done storing')
    connection.commit()

def send_email(message):
    host = 'smtp.gmail.com'
    port = 465
    username = 'damolabalogun79@gmail.com'
    password = os.getenv('PASSWORD2')
    receiver = 'damolabalogun79@gmail.com'
    with SMTP_SSL(host, port) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)
    print('Email sent')

def read(extracted):
    row = extracted.split(',')
    row = [item.strip() for item in row]
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
    rows = cursor.fetchall()
    return rows

if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)

        if extracted != "No upcoming tours":
            row = read(extracted)
            print(row)
            if not  row:
                store(extracted)
                send_email(extracted)