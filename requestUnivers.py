import csv
from config import BASEURL, REGIONSCSV, UNIVERCSV, VPO
from utils import get_html, write_csv
from bs4 import BeautifulSoup as bs
import time


def read_csv():
	listUrls = []
	with open(REGIONSCSV) as f:
		reader = csv.reader(f)
		for row in reader:
			if row[0] == "г. Москва": # TODO изменить после тестов
				listUrls.append(row[1])
				# print(row[1])
	return listUrls


def get_univer(html):
	soup = bs(html, 'lxml')
	trs = soup.find('table', class_='an').find_all('tr')

	for i, tr in enumerate(trs):
		if i > 1:
			tds = tr.find_all('td')
			# name = tds[1].find('a').text
			# url = tds[1].find('a').get('href')
			try:
				nameUniver = tds[1].find('a').text.strip()
			except:
				nameUniver = ''

			try:
				url = BASEURL + VPO + tds[1].find('a').get('href')
				id = url.split('=')[1]
			except:
				url = ''
				id = ''

			data = {'name': nameUniver, 'url': url, 'id': id}
			write_csv(UNIVERCSV, data)


def main():
	listUrls = read_csv()
	for url in listUrls:
		html = get_html(url)
		get_univer(html)


if __name__ == '__main__':
	start_time = time.process_time()
	main()
	print("--- %s seconds ---" % (time.process_time() - start_time))