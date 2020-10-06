# import pandas as pd
# import matplotlib.pyplot as plt
#
# # data = {'Name': ['SUM', 'REA', 'RANEPA', 'FA'],
# #         'Score1': [27, 24, 22, 32],
# #         'Score2': [30, 35, 27, 32],
# #         'Qualification': ['Msc', 'MA', 'MCA', 'Phd']}
#
# data = {'Name': ['Score0', 'Score1', 'Score2', 'Score3'],
# 		'SUM': [27, 24, 22, 32],
# 		'REA': [30, 35, 27, 30],
# 		'RANEPA': [25, 30, 29, 28]}
#
# df = pd.DataFrame(index=['Score0', 'Score1', 'Score2', 'Score3'])
# df['SUM'] = [27, 24, 22, 32]
# df['REA'] = [30, 35, 27, 30]
# df['SANEPA'] = [25, 30, 29, 28]
# # print(df)
#
# print(df.loc["Score1"])
# df.loc['Score1'].plot(kind='bar')
# # # df.plot(x='Name', y = 'Score1', kind='bar')
# plt.show()


str = '82,72'

print(float(str.replace(',', '.')))