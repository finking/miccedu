import pandas as pd, os
from utils import get_html
import requestIndicators, time
from config import BASEURL, VPO, DIR, YEAR
DEGREE = 1000
listFiles = []

universAbbs = {
    60: 'ГУУ',
    209: 'РЭУ',
    1766: 'ВШЭ',
    1767: 'ФинУнивер',
    1783: 'РАНХиГС'
}  # В Аббревиатуре нельзя использовать ".", т.е. нельзя написать Фин.Универ


def list_files(pathFiles):
    for file in os.listdir(pathFiles):
        listFiles.append(file.split('.')[0])


def univers_research():
    for k, v in universAbbs.items():
        if v not in listFiles:
            start_time = time.process_time()
            html = get_html(BASEURL+VPO+str(k))
            requestIndicators.get_indicators(v, html)
            print(f'Данные для {v} записаны за: ')
            print("%s seconds." % (time.process_time() - start_time))
        else:
            print(f'Файл с параметрами {v} уже существует. '
                  f'Если его необходимо обновить, то нужно удалить {DIR}/{v}.csv')

    name_row = True
    univers = pd.DataFrame(index=range(120))
    for k, v in universAbbs.items():
        df = pd.read_csv(f"{DIR}/{v}.csv", names=['Пункт', 'Показатель', 'Ед. изм', 'Значение'],
                         encoding='cp1251', decimal=',')
        if name_row:
            univers['Показатель'] = df['Показатель']
            name_row = False
        univers[v] = df['Значение'].tolist()

    # Добавление численности НПР
    univers.loc[len(univers)] = univers.loc[85: 86, univers.columns[1:]].astype(float).sum(numeric_only=True)
    univers['Показатель'][len(univers)-1] = 'Численность НПР'

    # Добавление доли НПР к общему количеству студентов
    univers.loc[len(univers)] = univers.loc[120, univers.columns[1:]].astype(float)/\
                                univers.loc[61, univers.columns[1:]].astype(float)
    univers['Показатель'][len(univers)-1] = 'Доля НПР к общему кол-ву студентов'

    # Доходы вуза из бюджетных источников
    univers.loc[len(univers)] = (univers.loc[111, univers.columns[1:]].astype(float) -
                                 univers.loc[112, univers.columns[1:]].astype(float)) / DEGREE
    univers['Показатель'][len(univers) - 1] = 'Доходы вуза из бюджетных источников (млн руб)'

    # Общий доход ВУЗа в расчете на одну публикацию
    univers.loc[len(univers)] = univers.loc[111, univers.columns[1:]].astype(float) / \
                                (univers.loc[19, univers.columns[1:]].astype(float)/100 *
                                 univers.loc[120, univers.columns[1:]]) / DEGREE
    univers['Показатель'][len(univers) - 1] = 'Общий доход ВУЗа в расчете на одну публикацию в Scopus (млн руб)'

    # Доход ВУЗа из бюджета в расчете на одну публикацию
    univers.loc[len(univers)] = univers.loc[122, univers.columns[1:]].astype(float) / \
                                (univers.loc[19, univers.columns[1:]].astype(float)/100 *
                                 univers.loc[120, univers.columns[1:]])
    univers['Показатель'][len(univers) - 1] = 'Доход ВУЗа из бюджета в расчете на одну публикацию в Scopus (млн руб)'

    print(univers)
    # print(univers)
    try:
        writer = pd.ExcelWriter(f'data/analysis_{YEAR}.xlsx', engine='xlsxwriter', options={'strings_to_numbers': True})
        univers.to_excel(writer)
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        format1 = workbook.add_format({'bold': False, 'font_name': 'Arial', 'font_size': 10})
        format2 = workbook.add_format({'num_format': '# ##0.00'})
        worksheet.set_column('B:B', 100, format1)
        worksheet.set_column('C:G', 10, format2)
        writer.save()
    except Exception as e:
        print(f"ERROR: Запись в файл не удалась! По причине:{e}")
    return univers


if __name__ == '__main__':
    list_files(DIR)
    univers_research()
