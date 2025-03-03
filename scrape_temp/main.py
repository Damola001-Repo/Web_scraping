import requests
import selectorlib
from datetime import datetime
import time


URL = 'https://programmer100.pythonanywhere.com/'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def get_source(url):
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source

def get_temperature(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)['temperature']
    return value

def get_date():
    current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    return current_time

def write_data(date, temperature):
    content = f"{date},{temperature}"
    with open('data.txt', 'a') as file:
        file.write(content + "\n")


if __name__ == '__main__':
    while True:
        source = get_source(URL)
        temperature = get_temperature(source)
        date = get_date()
        write_data(date, temperature)

        time.sleep(2)