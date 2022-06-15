import requests
import pandas as pd
from config import YEAR, DIR, universAbbs


def get_html(url):
    r = requests.get(url)
    # r = requests.get(url, verify=False) # Если ошибка с сертификатом.
    if r.ok:
        # r.encoding = 'cp1251'
        return r.text
    print(r.status_code)


def get_indicators():
    name_row = True
    univers = pd.DataFrame(index=range(120))
    for k, v in universAbbs.items():
        df = pd.read_csv(f"{DIR}/{v}.csv", names=['Пункт', 'Показатель', 'Ед. изм', 'Значение'],
                         encoding='cp1251', decimal=',')
        if name_row:
            univers['Показатель'] = df['Показатель']
            name_row = False
        univers[v] = df['Значение'].tolist()
    return univers


def writer_xlsx(univers):
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

