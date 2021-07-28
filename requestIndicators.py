import csv
from config import DIR
from bs4 import BeautifulSoup as bs


def get_indicators(id, html):
    tables = bs(html, 'lxml')
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
