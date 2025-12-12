# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import pandas as pd
from surprise import Reader
from surprise import KNNWithMeans
from surprise import Dataset
import pickle
from surprise.model_selection import cross_validate
from surprise import accuracy, Dataset, SVD
from sklearn.model_selection import train_test_split
from surprise.model_selection import GridSearchCV
from surprise import SVD
import pickle



def process_data(filename):
    movie_df_csv = pd.read_csv(filename)
    df_sub = movie_df_csv[['userid','movieid','rating']]
    train, test = train_test_split(df_sub, test_size=0.2)
    print("Done with train test split")
    return train,test

def load(train,test):
    reader = Reader(rating_scale=(1, 5))    
    data_train = Dataset.load_from_df(train[['userid','movieid','rating']], reader)
    trainingSet = data_train.build_full_trainset()
    print("Done Processing")
    return trainingSet, data_train, test

def modelling(trainingSet, data_train, test):
   param_grid = {
    "n_epochs": [5, 10],
    "lr_all": [0.002, 0.005],
    "reg_all": [0.4, 0.6]
    }

    # Get the best params using GridSearchCV
   gs = GridSearchCV(SVD, param_grid, measures=["rmse"], cv=4)
   gs.fit(data_train)
   best_params = gs.best_params["rmse"]
   print(gs.best_score["rmse"])
   print(gs.best_params["rmse"])
    
   # Extract and train model with best params
   svd_algo = SVD(n_epochs=best_params['n_epochs'],
                   lr_all=best_params['lr_all'],
                   reg_all=best_params['reg_all'])
   svd_algo.fit(trainingSet)

   predictions = []
   actuals = []
   rmse_val = []
   for col, row in test.iterrows():
       predictions.append(svd_algo.predict(row.userid, row.movieid).est)
       actuals.append(row.rating)
   rmse_val = rmse(np.array(predictions), np.array(actuals))
   print("Test RMSE for SVD : " + str(rmse_val))
   print("Done Modelling")
   return svd_algo

def model_to_binary(svd_model):
    filename = 'SVD_14k'
    outfile = open(filename,'wb')
    pickle.dump(svd_model,outfile)
    outfile.close()      
    print("Done Converting to Binary")

    #this function returns the root mean squared error between two arrays
def rmse(predictions, targets):
    return np.sqrt(((predictions - targets) ** 2).mean())

def main():
    data_file = "watched_rated_df.csv"
    train,test=process_data(data_file)
    trainingSet, data_train, test = load(train,test)
    svd_model = modelling(trainingSet, data_train, test)
    model_to_binary(svd_model)
    
if __name__ == "__main__":
    main()
