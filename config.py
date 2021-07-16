# Сайт для парсинга
# BASEURL = 'http://indicators.miccedu.ru/monitoring/2019/'
# INDEXPAGE = 'index.php?m=vpo'
# VPO = '_vpo/'

BASEURL = 'https://monitoring.miccedu.ru/'
INDEXPAGE = '?m=vpo'
YEAR = 2018
VPO = f'iam/{YEAR}/_vpo/'

# Файлы csv
REGIONSCSV = f'data/regions_{YEAR}.csv'
UNIVERCSV = f'data/univers_{YEAR}.csv'

# Директория для хранения университетов
DIR = f'data/univers/{YEAR}'