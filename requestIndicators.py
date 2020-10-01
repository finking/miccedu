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
			pattern = 'Плеханов'
			if row[0].find(pattern) != -1:
				dictUniver[row[2]] = [row[0], row[1]]
			# print(f'Считываются данные для "{row[0]}"')
	return dictUniver


def get_indicators(id, name_u, html):
	tables = bs(html, 'lxml')
	# info = tables.find('table', id='info')
	# name_u = info.find('tr').find_all('td')[1].text
	print(f'Сканируется "{name_u}"')
	tables_u = tables.find_all('table', class_='napde')
	for table in tables_u:
		trs = table.find_all('tr')
		for tr in trs:
			if tr.get('class') is None:
				tds = tr.find_all('td')
				# print(f"Пункт {tds[0].text}. Наименование: {tds[1].text}. Измерение: {tds[2].text}. "
				# 	  f"Значение: {tds[3].text}.")

				data = {'item': tds[0].text,  # №п/п
						'name': tds[1].text,  # Наименование показателя
						'dimension': tds[2].text,  # Единица измерения
						'value': tds[3].text}  # Значение показателя
				indicator_csv(id, data)

	dop = tables.find('table', id= 'analis_dop')
	trs = dop.find_all('tr')
	for i, tr in enumerate(trs):
		if i>1:
			tds = tr.find_all('td')
			if len(tds) > 1:
				if len(tds) == 4:
					# print(f"Пункт {tds[0].text}. Наименование: {tds[1].text}. Измерение: {tds[2].text}. "
					# 	f"Значение: {tds[3].text}.")
					data = {'item': tds[0].text,  # №п/п
							'name': tds[1].text,  # Наименование показателя
							'dimension': tds[2].text,  # Единица измерения
							'value': tds[3].text}  # Значение показателя
					indicator_csv(name_u, data)

				elif len(tds) == 3:
					# print(f"Пункт . Наименование: {tds[0].text}. Измерение: {tds[1].text}. "
					# 	f"Значение: {tds[2].text}.")
					data = {'item': '',  # №п/п
							'name': tds[0].text,  # Наименование показателя
							'dimension': tds[1].text,  # Единица измерения
							'value': tds[2].text}  # Значение показателя
					indicator_csv(name_u, data)


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
	# start_time = time.process_time()
	main()
# print("--- %s seconds ---" % (time.process_time() - start_time))
