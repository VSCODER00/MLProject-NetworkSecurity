import pymongo
import os
import sys
import pandas as pd
from networksecurity.entity.config import DataIngestionConfig, TrainingPipelineConfig
from networksecurity.exception.exception import CustomException
from networksecurity.entity.artifacts import DataIngestionArtifact,DataValidationArtifact
from dotenv import load_dotenv
load_dotenv()
from sklearn.model_selection import train_test_split
url=os.getenv("MONGO_URI")




class DataIngestion:
    def __init__(self,data_ingestion_config=DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise CustomException(e,sys)

    def fetch_from_database(self):
        try:
            client=pymongo.MongoClient(url)
            db=client[self.data_ingestion_config.database_name]
            collection=db[self.data_ingestion_config.collection_name]
            data=list(collection.find())
            df=pd.DataFrame(data)
            df.drop("_id",axis=1,inplace=True)
            print(df.columns)
            return df
        except Exception as e:
            raise CustomException(e,sys)
        
    def save_the_raw_data(self,dataframe):
        try:
            pathTostoreRawData=self.data_ingestion_config.feature_store_file_path
            os.makedirs(os.path.dirname(pathTostoreRawData), exist_ok=True)
            dataframe.to_csv(pathTostoreRawData,index=False)

        except Exception as e:
            raise CustomException(e,sys)
        
    def perform_train_test_split(self,dataframe):
        try:
            ratio=self.data_ingestion_config.train_test_split_ratio
            dir_path=self.data_ingestion_config.feature_store_file_path
            train_set, test_set=train_test_split(dataframe,test_size=ratio,random_state=42)
            train_path=self.data_ingestion_config.training_file_path
            test_path=self.data_ingestion_config.testing_file_path
            os.makedirs(os.path.dirname(train_path), exist_ok=True)
            os.makedirs(os.path.dirname(test_path), exist_ok=True)

            train_set.to_csv(train_path,index=False)
            test_set.to_csv(test_path,index=False)
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_ingestion(self):
        dataframe=self.fetch_from_database()
        self.save_the_raw_data(dataframe=dataframe)
        self.perform_train_test_split(dataframe=dataframe)
        Data_ingestion_artifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path, test_file_path=self.data_ingestion_config.testing_file_path)
        return Data_ingestion_artifact

