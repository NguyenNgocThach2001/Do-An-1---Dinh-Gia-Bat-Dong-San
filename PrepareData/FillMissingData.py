import numpy as np
import pandas as pd

data = pd.read_csv("House_Dataset.csv")
df = pd.DataFrame(data)
df = df.dropna(how = 'all')
df['Số toilet'] = df['Số toilet'].replace('None', -1)
df['Số tầng'] = df['Số tầng'].replace('None', -1)
df['Số phòng ngủ'] = df['Số phòng ngủ'].replace('None', -1)
df['Diện Tích'] = df['Diện Tích'].astype(str)
df['Giá'] = df['Giá'].astype(str)

df = df.drop('Hướng ban công', 1)
df = df.drop('Hướng nhà', 1)
df = df.drop('Mặt tiền', 1)
df = df.drop('Pháp lý', 1)
df = df.drop('Đường vào', 1)
df = df.drop('Địa chỉ', 1)

df.drop_duplicates()
df.dropna()

# xoa het none
df.drop(df[df['Số toilet'].astype(int) == -1].index, inplace = True)
df.drop(df[df['Số tầng'].astype(int) == -1].index, inplace = True)
df.drop(df[df['Số phòng ngủ'].astype(int) == -1].index, inplace = True)


df.drop(df[df['Số toilet'].astype(int) >= 15].index, inplace = True)
df.drop(df[df['Số tầng'].astype(int) >= 10].index, inplace = True)
df.drop(df[df['Số phòng ngủ'].astype(int) >= 15].index, inplace = True)
df.drop(df[df['Diện Tích'].astype(str) == ("Địa" or "None")].index, inplace = True)
df.drop(df[df['Giá'].astype(str) == ("Loại" or "None")].index, inplace = True)
df['Diện Tích'] = df['Diện Tích'].astype(float)
df['Giá'] = df['Giá'].astype(float)
df = df.reset_index(drop=True)

ctoilet = df['Số toilet'].value_counts()
ctang = df['Số tầng'].value_counts()
cphongngu = df['Số phòng ngủ'].value_counts()

toilet_mode = ((ctoilet.nlargest(2)).iloc[1:2].index[0])
tang_mode = ((ctang.nlargest(2)).iloc[1:2].index[0])
phongngu_mode = ((cphongngu.nlargest(2)).iloc[1:2].index[0])

# print(ctoilet)
# print(ctang)
# print(cphongngu)

# print(toilet_mode)
# print(tang_mode)
# print(phongngu_mode)

df['Số toilet'] = df['Số toilet'].replace(-1, toilet_mode)
df['Số tầng'] = df['Số tầng'].replace(-1, tang_mode)
df['Số phòng ngủ'] = df['Số phòng ngủ'].replace(-1, phongngu_mode)

def swap_columns(df, col1, col2):
    col_list = list(df.columns)
    x, y = col_list.index(col1), col_list.index(col2)
    col_list[y], col_list[x] = col_list[x], col_list[y]
    df = df[col_list]
    return df

df = swap_columns(df, 'Giá', 'Diện Tích')

df.to_csv("Dataset.csv", sep=',', encoding='utf-8')

print(df)

