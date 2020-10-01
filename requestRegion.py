# -*- coding: utf-8 -*-
from utils import get_html, write_csv
from bs4 import BeautifulSoup
import csv
import re
import time
from config import BASEURL, INDEXPAGE, REGIONSCSV


def get_regions(html):
	soup = BeautifulSoup(html, 'lxml')
	regions = soup.find('table', id='tregion').find_all('p')
	for region in regions:
		if region.get('class') is None:
			try:
				nameRegion = region.text.strip()
			except:
				nameRegion = ''

			try:
				url = BASEURL + region.find('a').get('href')
			except:
				url = ''

			data = {'name': nameRegion, 'url': url}
			write_csv(REGIONSCSV, data)


def main():
	html = get_html(BASEURL + INDEXPAGE)
	get_regions(html)


# try:
# 	pattern = 'Next'
# 	url = base_url + soup.find('div', class_='cmc-button-group').find('a', text=re.compile(pattern)).get('href')
# except:
# 	break


if __name__ == '__main__':
	start_time = time.process_time()
	main()
	print("--- %s seconds ---" % (time.process_time() - start_time))
