import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import explained_variance_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

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
                            'Score':[mlr_score,decision_score],
                            'Explained Variance Score':[expl_mlr,expl_tr]
                           })
models_score.sort_values(by='Score',ascending=False)
print(models_score)

New_Data = [[[100,1,2,2]]
           ,[[100,2,1,2]]
           ,[[100,2,2,1]]
           ,[[100,2,2,2]]]

print("Regression Tree Predict: ")
for index, it in enumerate(New_Data):
    print("Predict " + str(index) + ": " + str(tr_regressor.predict(it)))

print("Multiple Linear Regression Predict: ")
for index, it in enumerate(New_Data):
    print("Predict " + str(index) + ": " + str(mlr.predict(it)))