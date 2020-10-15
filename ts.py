import pandas as pd
import matplotlib.pyplot as plt
from xlsxwriter import Workbook

def main():
    # data = {'Name': ['SUM', 'REA', 'RANEPA', 'FA'],
    #         'Score1': [27, 24, 22, 32],
    #         'Score2': [30, 35, 27, 32],
    #         'Qualification': ['Msc', 'MA', 'MCA', 'Phd']}

    data = {'Name': ['Score0', 'Score1', 'Score2', 'Score3'],
            'SUM': [27, 24, 22, 32],
            'REA': [30, 35, 27, 30],
            'RANEPA': [25, 30, 29, 28]}

    df = pd.DataFrame(index=['Score0', 'Score1', 'Score2', 'Score3'])
    df['SUM'] = [27, 24, 22, 32]
    df['REA'] = [30, 35, 27, 30]
    df['SANEPA'] = [25, 30, 29, 28]
    df['Description'] = ['Perv', 'Vtor', 'Tret', 'Chet']
    print(df)

    # print(df.loc["Score1"])
    # df.loc['Score1'].plot(kind='bar')
    # # # df.plot(x='Name', y = 'Score1', kind='bar')
    # plt.show()
    print("**")
    df.sum()

    # Сложение только для цифровых данных
    # df.loc['new'] = df.loc[['Score0', 'Score1']].sum(numeric_only=True)
    # df['Description']['new'] = 'ScoreSum'
    # print(df)

    # Деление определенных столбцов
    df.loc['new'] = df.loc['Score0', df.columns[:-1]]/df.loc['Score1', df.columns[:-1]]
    df['Description']['new'] = 'Dev'
    print(df)

    # df.to_excel(excel_writer='data/test.xlsx')

def write_xlsx(data):
    # Create a workbook and add a worksheet.
    workbook = Workbook('data/test.xlsx')
    worksheet = workbook.add_worksheet()

    for number, value in enumerate(data):
        # row_format = workbook.add_format(BASE_FORMAT_PARAMS)
        worksheet.write(f"A{number + 2}", value['name'])
        worksheet.write(f"B{number + 2}", value['type'])


if __name__ == '__main__':
    main()