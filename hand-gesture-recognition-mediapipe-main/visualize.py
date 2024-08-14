import pandas as pd
import matplotlib.pyplot as plt

file_path = r'C:\Users\UVRLab\Desktop\PythonPart\HMD_point_history_40_5.csv'

df = pd.read_csv(file_path, header=None)

x_columns = [i for i in range(df.shape[1]) if i % 2 == 0]
y_columns = [i for i in range(df.shape[1]) if i % 2 != 0]

x_values_df = df.iloc[:, x_columns]
y_values_df = df.iloc[:, y_columns]

for index, row in x_values_df.iterrows():
    x = row.values
    y = y_values_df.iloc[index].values
    plt.plot(x, y, marker='o', label=f'Row {index}')

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Data Visualization')
plt.ylim(-1, 1)
plt.xlim(-1, 1)
plt.legend()
plt.show()
