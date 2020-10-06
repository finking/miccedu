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

	figure = univers.loc['Средний балл ЕГЭ студентов, принятых по результатам ЕГЭ на обучение по очной форме по программам '
				  'бакалавриата и специалитета за счет средств соответствующих бюджетов бюджетной системы РФ']
	# figure = figure.astype(float)
	# figure.plot(kind='bar')
	#
	# plt.show()

def univers_research():
	name_row = True
	univers = pd.DataFrame(index=range(120))
	for i in universID:
		df = pd.read_csv(f"{DIR}/{i}.csv", names=['Пункт', 'Показатель', 'Ед. изм', 'Значение'],
						 encoding='cp1251')
		if name_row:
		# 	univers['Пункт'] = df['Пункт']
		# 	univers['Показатель'] = df['Показатель']
		# 	univers['Ед. изм'] = df['Ед. изм']
			univers.index = df['Показатель']
			name_row = False
		univers[i] = df['Значение'].tolist()
	univers = univers.rename(columns=universAbbs)
	# print(univers)
	try:
		univers.to_excel(excel_writer='data/analysis1.xlsx')
	except Exception as e:
		print(e)
	return univers


if __name__ == '__main__':
	main()
