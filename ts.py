import pandas as pd
import matplotlib.pyplot as plt

# data = {'Name': ['SUM', 'REA', 'RANEPA', 'FA'],
#         'Score1': [27, 24, 22, 32],
#         'Score2': [30, 35, 27, 32],
#         'Qualification': ['Msc', 'MA', 'MCA', 'Phd']}

data = {'Name': ['Score0', 'Score1', 'Score2', 'Score3'],
		'SUM': [27, 24, 22, 32],
		'REA': [30, 35, 27, 30],
		'RANEPA': [25, 30, 29, 28]}

df = pd.DataFrame(data)
print(df)

# print(df["Score1"])
df.plot(x='Name', y = 'Score1', kind='bar')
plt.show()


