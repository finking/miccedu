import pandas as pd
import matplotlib.pyplot as plt
from config import DIR, UNIVERCSV

universID = [60, 209, 1766, 1767, 1783]
universAbbs = {
	60: 'ГУУ',
	209: 'РЭУ',
	1766: 'ВШЭ',
	1767: 'Фин.Универ',
	1783: 'РАНХиГС'
}


def main():
	univers = univers_research()
	print(univers['Показатель'])


def univers_research():
	name_row = True
	univers = pd.DataFrame()
	for i in universID:
		df = pd.read_csv(f"{DIR}/{i}.csv", names=['Пункт', 'Показатель', 'Ед. изм', 'Значение'],
						 encoding='cp1251')
		if name_row:
			univers['Пункт'] = df['Пункт']
			univers['Показатель'] = df['Показатель']
			univers['Ед. изм'] = df['Ед. изм']
			name_row = False
		univers[i] = df['Значение']
	univers = univers.rename(columns=universAbbs)
	# print(univers)
	return univers


if __name__ == '__main__':
	main()
