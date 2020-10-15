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
    # figure = univers.loc[0]['ГУУ': 'РАНХиГС']
    # figure = figure.astype(float)
    # figure.plot(kind='bar')
    # plt.show()


def univers_research():
    name_row = True
    univers = pd.DataFrame(index=range(120))
    for i in universID:
        df = pd.read_csv(f"{DIR}/{i}.csv", names=['Пункт', 'Показатель', 'Ед. изм', 'Значение'],
                         encoding='cp1251', decimal=',')
        if name_row:
            univers['Показатель'] = df['Показатель']
            name_row = False
        univers[i] = df['Значение'].tolist()
    univers = univers.rename(columns=universAbbs)

    # Добавление численности НПР
    univers.loc[len(univers)] = univers.loc[85: 86, univers.columns[1:]].astype(float).sum(numeric_only=True)
    univers['Показатель'][len(univers)-1] = 'Численность НПР'

    # Добавление доли НПР к общему количеству студентов
    univers.loc[len(univers)] = univers.loc[120, univers.columns[1:]].astype(float)/\
                                univers.loc[61, univers.columns[1:]].astype(float)
    univers['Показатель'][len(univers)-1] = 'Доля НПР к общему кол-ву студентов'
    print(univers)
    # print(univers)
    try:
        writer = pd.ExcelWriter('data/analysis1.xlsx', engine='xlsxwriter', options={'strings_to_numbers': True})
        univers.to_excel(writer)
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        format1 = workbook.add_format({'bold': False, 'font_name': 'Arial', 'font_size': 10})
        format2 = workbook.add_format({'num_format': '# ##0.00'})
        worksheet.set_column('B:B', 100, format1)
        worksheet.set_column('C:G', 10, format2)
        writer.save()
    except Exception as e:
        print(e)
    return univers


if __name__ == '__main__':
    main()
