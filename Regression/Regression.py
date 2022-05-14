from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import explained_variance_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

def Predicts():
    dataset = pd.read_csv("Dataset.csv", index_col=0)
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

    New_Data = [[[100,1,2,2]]
            ,[[100,2,1,2]]
            ,[[100,2,2,1]]
            ,[[100,2,2,2]]
            ,[[150,3,1,4]]
            ,[[125,2,2,1]]
            ,[[50,2,4,1]]
            ,[[25,3,3,3]]]

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

    plt.figure()
    plt.plot(xprice, yareage, 'o')
    plt.xlabel("Price")
    plt.ylabel("Areage")
    for index, it in enumerate(MLR_Result):
        plt.plot(it, New_Data[index][0][0], 'o', color = 'red')
    for index, it in enumerate(TRR_Result):
        plt.plot(it, New_Data[index][0][0], 'o', color = 'yellow')
    plt.figure()

    plt.xlabel("Price")
    plt.ylabel("Bedrooms")
    plt.plot(xprice, ybedroom, 'o' )
    for index, it in enumerate(MLR_Result):
        plt.plot(it, New_Data[index][0][1], 'o', color = 'red')
    for index, it in enumerate(TRR_Result):
        plt.plot(it, New_Data[index][0][1], 'o', color = 'yellow')
    plt.figure()


    plt.xlabel("Price")
    plt.ylabel("Toilets")
    plt.plot(xprice, ytoilet, 'o')
    plt.figure()
    for index, it in enumerate(MLR_Result):
        plt.plot(it, New_Data[index][0][2], 'o', color = 'red')
    for index, it in enumerate(TRR_Result):
        plt.plot(it, New_Data[index][0][2], 'o', color = 'yellow')


    plt.xlabel("Price")
    plt.ylabel("Floors")
    plt.plot(xprice, yfloor, 'o')
    for index, it in enumerate(MLR_Result):
        plt.plot(it, New_Data[index][0][3], 'o', color = 'red')
    for index, it in enumerate(TRR_Result):
        plt.plot(it, New_Data[index][0][3], 'o', color = 'yellow')


    plt.show()