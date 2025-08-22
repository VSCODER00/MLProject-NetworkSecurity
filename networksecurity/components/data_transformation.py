import os
import sys
from networksecurity.entity.config import DataTransformationConfig
from networksecurity.entity.artifacts import DataValidationArtifact,DataTransformationArtifact
from networksecurity.exception.exception import CustomException
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.compose import ColumnTransformer
import numpy as np
from networksecurity.utils.utils import save_numpy_array_data, saveObj
class DataTransformation:
    def __init__(self,data_transformation_config=DataTransformationConfig,data_validation_artifact=DataValidationArtifact):
        self.data_transformation_config=data_transformation_config
        self.data_validation_artifact=data_validation_artifact
    

    def initiate_data_transformation(self):
        try:
            train_df=pd.read_csv(self.data_validation_artifact.valid_train_file_path)
            test_df=pd.read_csv(self.data_validation_artifact.valid_test_file_path)
            x_train=train_df.drop('Result',axis=1)
            y_train=train_df['Result']
            x_test=test_df.drop('Result',axis=1)
            y_test=test_df['Result']
            imputer=KNNImputer(missing_values=np.nan,n_neighbors=3,weights='uniform')
            preprocessor=ColumnTransformer([
                ('Imputer',imputer,x_train.columns)
            ])
            x_train=preprocessor.fit_transform(x_train)
            x_test=preprocessor.transform(x_test)
            saveObj(self.data_transformation_config.transformed_object_file_path, preprocessor)
            train_arr=np.c_[x_train,np.array(y_train)]
            test_arr=np.c_[x_test,np.array(y_test)]
            save_numpy_array_data( self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data( self.data_transformation_config.transformed_test_file_path,array=test_arr)
            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            return data_transformation_artifact
        except Exception as e:
            raise CustomException(e,sys)