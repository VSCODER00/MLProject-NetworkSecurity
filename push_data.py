import os
from dotenv import load_dotenv, dotenv_values
load_dotenv()
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from networksecurity.exception.exception import CustomException
import pandas as pd
import sys
uri =os.getenv("MONGO_URI")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

class ETLPipeline():
    def __init__(self):
        pass

    def load_data_from_csv(self,file_path):
        try:
            df=pd.read_csv(file_path)
            df.reset_index(drop=True,inplace=True)
            x=df.to_dict(orient='records')
            
            return x

        except Exception as e:
            raise CustomException(e,sys)
        
    
    def insert_into_mongoDB(self):
        try:
            self.db=client["ML-NSProj"]
            self.collection=self.db["dataset"]
            self.collection.insert_many(self.load_data_from_csv("Network_Data/phisingData.csv"))
        except Exception as e:
            raise CustomException(e,sys)
        

if __name__=="__main__":
    obj1=ETLPipeline()
    obj1.insert_into_mongoDB()