import csv
from config import UNIVERCSV, DIR
from utils import get_html
from bs4 import BeautifulSoup as bs
import time


def read_csv():
    dictUniver = {}
    with open(UNIVERCSV) as f:
        reader = csv.reader(f)
        for row in reader:
            patterns = ['Плеханов', 'Государственный университет управления', 'Высшая школа экономики', 'Финансовый','народного']
            for pattern in patterns:
                if row[0].find(pattern) != -1:
                    dictUniver[row[2]] = [row[0], row[1]]
        # print(f'Считываются данные для "{row[0]}"')
    return dictUniver


def get_indicators(id, name_u, html):
    tables = bs(html, 'lxml')
    print(f'Сканируется "{name_u}"')
    tables_u = tables.find_all('table', class_='napde')
    for table in tables_u:
        trs = table.find_all('tr')
        for tr in trs:
            if tr.get('class') is None:
                tds = tr.find_all('td')
                data = {'item': tds[0].text,  # №п/п
                        'name': tds[1].text,  # Наименование показателя
                        'dimension': tds[2].text,  # Единица измерения
                        'value': tds[3].text.replace(',', '.').replace(' ', '')}  # Значение показателя
                # 'value': tds[3].text.strip()}  # Значение показателя
                indicator_csv(id, data)

    dop = tables.find('table', id= 'analis_dop')
    trs = dop.find_all('tr')
    for i, tr in enumerate(trs):
        if i>1:
            tds = tr.find_all('td')
            if len(tds) > 1:
                if len(tds) == 4:
                    data = {'item': tds[0].text,  # №п/п
                            'name': tds[1].text,  # Наименование показателя
                            'dimension': tds[2].text,  # Единица измерения
                            'value': tds[3].text.replace(',', '.').replace(' ', '')}  # Значение показателя
                    # 'value': tds[3].text}  # Значение показателя
                    indicator_csv(id, data)

                elif len(tds) == 3:
                    data = {'item': '',  # №п/п
                            'name': tds[0].text,  # Наименование показателя
                            'dimension': tds[1].text,  # Единица измерения
                            'value': tds[2].text}  # Значение показателя
                    indicator_csv(id, data)


def indicator_csv(filename, data):
    with open(f'{DIR}/{filename}.csv', 'a', newline='', ) as f:
        writer = csv.writer(f)
        writer.writerow((data['item'],
                         data['name'],
                         data['dimension'],
                         data['value']))


def main():
    dictUniver = read_csv()
    for id, value in dictUniver.items():
        html = get_html(value[1])
        get_indicators(id, value[0], html)


if __name__ == '__main__':
    start_time = time.process_time()
    main()
    print("--- %s seconds ---" % (time.process_time() - start_time))
