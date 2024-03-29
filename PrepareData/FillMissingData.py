from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

def FillMissing(MaxPrice, MaxAreage):
    data = pd.read_csv("House_Dataset.csv")
    print(data)
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
    # print(df)

    # dff = data.to_numpy()
    # xprice = dff[ :, 0]#Areage
    # yareage = dff[ :, 1]#Price
    # ybedroom = dff[ :, 6]#Bedroom
    # ytoilet = dff[ :, 7]#toilet
    # yfloor = dff[ :, 8]#floor

    # plt.figure()
    # plt.plot(xprice, yareage, 'o')
    # plt.xlabel("Price")
    # plt.ylabel("Areage")
    # plt.figure()
    # plt.xlabel("Price")
    # plt.ylabel("Bedrooms")
    # plt.plot(xprice, ybedroom, 'o' )
    # plt.figure()
    # plt.xlabel("Price")
    # plt.ylabel("Toilets")
    # plt.plot(xprice, ytoilet, 'o')
    # plt.figure()
    # plt.xlabel("Price")
    # plt.ylabel("Floors")
    # plt.plot(xprice, yfloor, 'o')
    # plt.show()

    # xoa het none
    df.drop(df[df['Số toilet'].astype(int) == -1].index, inplace = True)
    df.drop(df[df['Số tầng'].astype(int) == -1].index, inplace = True)
    df.drop(df[df['Số phòng ngủ'].astype(int) == -1].index, inplace = True)


    df.drop(df[df['Số toilet'].astype(int) >= 15].index, inplace = True)
    df.drop(df[df['Số tầng'].astype(int) >= 10].index, inplace = True)
    df.drop(df[df['Số phòng ngủ'].astype(int) >= 15].index, inplace = True)
    df.drop(df[df['Diện Tích'].astype(str) == ("Địa" or "None")].index, inplace = True)
    df.drop(df[df['Giá'].astype(str) == ("Loại" or "None")].index, inplace = True)
    df['Giá'] = df['Giá'].astype(float)
    df['Diện Tích'] = df['Diện Tích'].astype(float)
    df.drop(df[df['Giá'].astype(float) >= MaxPrice].index, inplace = True)
    df.drop(df[df['Diện Tích'].astype(float) >= MaxAreage].index, inplace = True)
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

