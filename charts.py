import pandas as pd
from config import universAbbs
YEARS = [2019, 2020, 2021]
NUMBER_INDICATORS = [120, 123]


# Запись в файл графиков по отдельным показателям
def writer_charts_xlsx(indicators, indicatorName):
    try:
        writer = pd.ExcelWriter(f'data/analysis/{indicatorName}.xlsx',
                                engine='xlsxwriter',
                                options={'strings_to_numbers': True})
        indicators.to_excel(writer)
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        format = workbook.add_format({'num_format': '# ##0.00'})
        worksheet.set_column('A:A', 12)
        worksheet.set_column('B:D', 10, format)

        # Создание сравнительной диаграммы для нескольких университетов одновременно.
        chart = workbook.add_chart({'type': 'column'})
        chart.set_size({'width': 620, 'height': 376})
        for i in range(indicators.shape[1]):
            col = i + 1
            chart.add_series({
                'name': ['Sheet1', 0, col],
                'categories': ['Sheet1', 1, 0,   len(indicators.index), 0],
                'values': ['Sheet1', 1, col, len(indicators.index), col],
                'data_labels': {'value': True, 'font': {'rotation': -90}}
            })
        chart.set_title({
            'name': indicatorName,
        })
        worksheet.insert_chart('G2', chart)

        # Создание графика по годам для одного университета
        dictCharts = {}  # Словарь для хранения The Chartsheet Class.
        for i in range(indicators.shape[0]):
            row = i + 1
            dictCharts[i] = workbook.add_chart({'type': 'line'})
            dictCharts.get(i).add_series({
                'name': ['Sheet1', row, 0],
                'categories': ['Sheet1', 0, 1, 0, len(indicators.columns)],
                'values': ['Sheet1', row, 1, row, len(indicators.columns)],
                'line': {'width': 3.25},
                'data_labels': {'value': True, 'position': 'above'},
                'marker': {'type': 'square', 'size': 7},
            })

        # Вставка каждого графика в Excel
        colFigire = 7
        for k in dictCharts.keys():
            colFigire = colFigire + 10
            dictCharts.get(k).set_title({
                'name': indicatorName,
            })
            # chart.set_y_axis({'name': indicatorName, })
            dictCharts.get(k).set_size({'width': 620, 'height': 376})
            worksheet.insert_chart(1, colFigire, dictCharts.get(k))

        writer.save()
    except Exception as e:
        print(f"ERROR: Запись в файл не удалась! По причине: {e}")


def main():
    for NUMBER_INDICATOR in NUMBER_INDICATORS:
        indicators = pd.DataFrame(index=universAbbs.values())
        for year in YEARS:
            df = pd.read_excel(f'data/analysis_{year}.xlsx', engine='openpyxl',index_col=0).T
            indicatorName = df.iloc[0, NUMBER_INDICATOR]
            indicatorValue = df.iloc[1:, NUMBER_INDICATOR].astype(float)
            indicators[year] = indicatorValue.tolist()
        writer_charts_xlsx(indicators, indicatorName)


if __name__ == '__main__':
    main()



