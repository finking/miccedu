import os
import requestIndicators
import time
from config import BASEURL, VPO, DIR, universAbbs
from utils import get_html, get_indicators, writer_xlsx

DEGREE = 1000
listFiles = []


def main():
    list_files(DIR)
    get_univers()
    univers = research_univers()
    writer_xlsx(univers)
    print(univers)


# Получение существующих файлов по университетам.
def list_files(pathFiles):
    for file in os.listdir(pathFiles):
        listFiles.append(file.split('.')[0])


# Получение данных по университетам.
def get_univers():
    for k, v in universAbbs.items():
        if v not in listFiles:
            start_time = time.process_time()
            html = get_html(BASEURL + VPO + str(k))
            requestIndicators.get_indicators(v, html)
            print(f'Данные для {v} записаны за: ')
            print("%s seconds." % (time.process_time() - start_time))
        else:
            print(f'Файл с параметрами {v} уже существует. '
                  f'Если его необходимо обновить, то нужно удалить {DIR}/{v}.csv')


def research_univers():
    # Создание excel файла для анализа нескольких университетов.
    univers = get_indicators()

    # Добавление численности НПР
    add_indicator(univers, 'sum',  'Численность НПР', 85, 86)

    # Добавление доли НПР к общему количеству студентов
    add_indicator(univers, 'div', 'Доля НПР к общему кол-ву студентов', 120, 61)

    # Доходы вуза из бюджетных источников
    add_indicator(univers, 'sub', 'Доходы вуза из бюджетных источников (млн руб)', 111, 112, degree=DEGREE)

    # Общий доход ВУЗа в расчете на одну публикацию
    add_indicator(univers, 'div/mul', 'Общий доход ВУЗа в расчете на одну публикацию в Scopus (млн руб)',
                  111, 19, 120, degree=DEGREE, hundred=100)

    # Доход ВУЗа из бюджета в расчете на одну публикацию
    add_indicator(univers, 'div/mul', 'Доход ВУЗа из бюджета в расчете на одну публикацию в Scopus (млн руб)',
                  122, 19, 120, hundred=100)
    return univers


def add_indicator(univers, operator, name, ind1, ind2, ind3=0, degree=1, hundred=1):
    if operator == 'sum':
        univers.loc[len(univers)] = univers.loc[ind1: ind2, univers.columns[1:]].astype(float).sum(numeric_only=True)
    elif operator == 'div':
        univers.loc[len(univers)] = univers.loc[ind1, univers.columns[1:]].astype(float) / \
                                    univers.loc[ind2, univers.columns[1:]].astype(float) / degree
    elif operator == 'sub':
        univers.loc[len(univers)] = (univers.loc[ind1, univers.columns[1:]].astype(float) -
                                     univers.loc[ind2, univers.columns[1:]].astype(float)) / degree
    elif operator == 'div/mul':
        univers.loc[len(univers)] = univers.loc[ind1, univers.columns[1:]].astype(float) / \
                                    (univers.loc[ind2, univers.columns[1:]].astype(float) / hundred *
                                     univers.loc[ind3, univers.columns[1:]]) / degree
    univers['Показатель'][len(univers) - 1] = name


if __name__ == '__main__':
    main()
