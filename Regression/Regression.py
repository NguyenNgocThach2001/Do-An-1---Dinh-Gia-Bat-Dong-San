from lib2to3.pgen2.pgen import DFAState
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import explained_variance_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from pandas.plotting import parallel_coordinates
import collections

def Predicts(New_Data, csvDataPath):
    if(csvDataPath == ''):
        return 0, '', '', '', ''
    dataset = pd.read_csv(csvDataPath, index_col=0)
    # print("Dataset: ")
    # print(dataset)

    X = dataset.iloc[:,1:].values #Variable
    Y = dataset.iloc[:,0].values #Target
    X_train,X_test,y_train,y_test=train_test_split(X,Y,test_size=0.3,random_state=0) #split train model

    # print("X (Variable): ")
    # print(X)
    # print("Y (Target): ")
    # print(Y)

    #DecisionTreeRegressor
    tr_regressor = DecisionTreeRegressor(random_state=0)
    tr_regressor.fit(X_train,y_train)
    tr_regressor.score(X_test,y_test)
    pred_tr = tr_regressor.predict(X_test)
    decision_score=tr_regressor.score(X_test,y_test)
    expl_tr = explained_variance_score(pred_tr,y_test)

    #LineaerRegression
    mlr = LinearRegression()
    mlr.fit(X_train,y_train)
    mlr_score = mlr.score(X_test,y_test)
    pred_mlr = mlr.predict(X_test)
    expl_mlr = explained_variance_score(pred_mlr,y_test)

    print("Multiple Linear Regression Model Score is ",round(mlr.score(X_test,y_test)*100))
    print("Decision tree Regression Model Score is:",round(tr_regressor.score(X_test,y_test)*100))

    models_score =pd.DataFrame({'Model':['Multiple Linear Regression','Decision Tree'],
                                'Score':[mlr_score * 100,decision_score * 100],
                                'Explained Variance Score':[expl_mlr,expl_tr]
                            })
    models_score.sort_values(by='Score',ascending=False)
    print(models_score)

    # New_Data = [[[100,1,2,2]]
    #         ,[[100,2,1,2]]
    #         ,[[100,2,2,1]]
    #         ,[[100,2,2,2]]
    #         ,[[150,3,1,4]]
    #         ,[[125,2,2,1]]
    #         ,[[50,2,4,1]]
    #         ,[[25,3,3,3]]
    #         ,[[200,5,3,3]]]

    TRR_Result = []
    print("Regression Tree Predict: ")
    for index, it in enumerate(New_Data):
        print("Predict " + str(index) + ": " + str(tr_regressor.predict(it)))
        TRR_Result.append(tr_regressor.predict(it))

    MLR_Result = []
    print("Multiple Linear Regression Predict: ")
    for index, it in enumerate(New_Data):
        print("Predict " + str(index) + ": " + str(mlr.predict(it)))
        MLR_Result.append(mlr.predict(it))

    print("Predict Comparison: RT \ MLR")
    for index, it in enumerate(TRR_Result):
        print("Predict " + str(index) + ": " + str(*TRR_Result[index]) + " \ " + str(*MLR_Result[index]))

    df = dataset.to_numpy()
    xprice = df[ :, 0]#Areage
    yareage = df[ :, 1]#Price
    ybedroom = df[ :, 2]#Bedroom
    ytoilet = df[ :, 3]#toilet
    yfloor = df[ :, 4]#floor

    # Biểu đồ phân tán 
    plt.figure()
    plt.plot(xprice, yareage, 'o')
    plt.xlabel("Price")
    plt.ylabel("Areage")
    for index, it in enumerate(MLR_Result):
        plt.plot(it, New_Data[index][0][0], 'o', color = 'red')
    for index, it in enumerate(TRR_Result):
        plt.plot(it, New_Data[index][0][0], 'o', color = 'orange')
    plt.savefig("IMG1.png")


    plt.figure()
    plt.xlabel("Price")
    plt.ylabel("Bedrooms")
    plt.plot(xprice, ybedroom, 'o' )
    for index, it in enumerate(MLR_Result):
        plt.plot(it, New_Data[index][0][1], 'o', color = 'red')
    for index, it in enumerate(TRR_Result):
        plt.plot(it, New_Data[index][0][1], 'o', color = 'orange')
    plt.savefig("IMG2.png")


    plt.figure()
    plt.xlabel("Price")
    plt.ylabel("Toilets")
    plt.plot(xprice, ytoilet, 'o')
    for index, it in enumerate(MLR_Result):
        plt.plot(it, New_Data[index][0][2], 'o', color = 'red')
    for index, it in enumerate(TRR_Result):
        plt.plot(it, New_Data[index][0][2], 'o', color = 'orange')
    plt.savefig("IMG3.png")

    plt.figure()
    plt.xlabel("Price")
    plt.ylabel("Floors")
    plt.plot(xprice, yfloor, 'o')
    for index, it in enumerate(MLR_Result):
        plt.plot(it, New_Data[index][0][3], 'o', color = 'red')
    for index, it in enumerate(TRR_Result):
        plt.plot(it, New_Data[index][0][3], 'o', color = 'orange')
    plt.savefig("IMG4.png")


    #Biểu đồ cột 
    df = pd.DataFrame(dataset)
    plt.figure()
    df['Diện Tích'].value_counts().plot(kind='bar', xlabel='Diện Tích', ylabel='Tần Suất')
    plt.savefig("IMG11.png")

    plt.figure()
    df['Số phòng ngủ'].value_counts().plot(kind='bar', xlabel='Số Phòng Ngủ', ylabel='Tần Suất')
    plt.savefig("IMG22.png")

    plt.figure()
    df['Số toilet'].value_counts().plot(kind='bar', xlabel='Số Toilet', ylabel='Tần Suất')
    plt.savefig("IMG33.png")

    plt.figure()
    df['Số tầng'].value_counts().plot(kind='bar', xlabel='Số Tầng', ylabel='Tần Suất')
    plt.savefig("IMG44.png")
    
    #Biểu đồ song song
    plt.figure()
    fig = parallel_coordinates(dataset, 'Giá', color = 'blue')
    fig.plot(New_Data[0], color = 'red')
    plt.savefig("IMG55.png")

    return plt, ("Kết quả dự đoán" + ": "), (str(round(float(TRR_Result[index]), 2)) + " tỷ "), ("\ "), (str(round(float(MLR_Result[index]),2)) + " tỷ")
    # plt.show()