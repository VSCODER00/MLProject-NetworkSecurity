import os
import sys
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
from networksecurity.entity.artifacts import DataTransformationArtifact,ModelTrainerArtifact
from networksecurity.exception.exception import CustomException
from networksecurity.utils.utils import load_numpy_array_data
from sklearn.model_selection import GridSearchCV
import joblib

class ModelTrainer:
    def __init__(self,data_transformation_artifact=DataTransformationArtifact):
        self.data_transformation_artifact=data_transformation_artifact
    def train_model(self,x_train,x_test,y_train,y_test):
        try:
            models = {
                "Random Forest": RandomForestClassifier(verbose=1),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic Regression": LogisticRegression(verbose=1),
                "AdaBoost": AdaBoostClassifier(),
            }
            params={
                 "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }
            }
            report={}
            best_score = -1
            best_model_name = None
            best_model = None
            for key,value in models.items():
                model=value
                parameters=params[key]
                gs=GridSearchCV(model,param_grid=parameters,n_jobs=-1,scoring='accuracy',verbose=1)
                gs.fit(x_train,y_train)
                y_pred=gs.predict(x_test)
                score=accuracy_score(y_true=y_test,y_pred=y_pred)
                report[key]=score
                if score > best_score:
                    best_score = score
                    best_model_name = key
                    best_model = gs.best_estimator_
            sorted_report = dict(sorted(report.items(), key=lambda item: item[1], reverse=True))
            path = os.path.join("artifacts", "models", f"{best_model_name.replace(' ', '_').lower()}_best.pkl")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            joblib.dump(best_model, path)
            model_trainer_artifact=ModelTrainerArtifact(path)
            return model_trainer_artifact


        except Exception as e:
            raise CustomException(e,sys)
    def initiate_model_training(self):
        train_path=self.data_transformation_artifact.transformed_train_file_path
        test_path=self.data_transformation_artifact.transformed_test_file_path
        train_arr=load_numpy_array_data(train_path)
        test_arr=load_numpy_array_data(test_path)
        x_train,x_test,y_train,y_test=(
            train_arr[:,:-1],
            test_arr[:,:-1],
            train_arr[:,-1],
            test_arr[:,-1]
        )
        model_trainer_artifact=self.train_model(x_train,x_test,y_train,y_test)
        return model_trainer_artifact


        