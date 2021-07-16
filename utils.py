import requests
import csv


def get_html(url):
    r = requests.get(url)
    if r.ok:
        # r.encoding = 'cp1251'
        return r.text
    print(r.status_code)


def write_csv(filename, data):
    with open(filename, 'a', newline='', encoding='cp1251') as f:
        writer = csv.writer(f)
        try:
            writer.writerow((data['name'], data['url'], data['id']))
        except:
            writer.writerow((data['name'], data['url']))

