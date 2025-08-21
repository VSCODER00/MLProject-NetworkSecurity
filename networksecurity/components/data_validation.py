import os
import pandas as pd
import numpy as np
import yaml
import sys
from networksecurity.entity.config import DataValidationConfig,TrainingPipelineConfig,DataIngestionConfig
from networksecurity.entity.artifacts import DataIngestionArtifact,DataValidationArtifact
from networksecurity.exception.exception import CustomException
from networksecurity.constants.training_pipeline.constants_config import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp

from networksecurity.utils.utils import write_yaml_file


class DataValidation:
    def __init__(self,data_validation_config=DataValidationConfig,data_ingestion_artifact=DataIngestionArtifact):
        self.data_validation_config=data_validation_config
        self.data_ingestion_artifact=data_ingestion_artifact
    
    def displayYamlFile(self):
        with open(SCHEMA_FILE_PATH, 'r') as file:
            self.loaded_data = yaml.safe_load(file)
            return (len(self.loaded_data['columns']))
    def detect_dataset_drift(self,base_df,current_df,threshold=0.5):
        status=True
        report={}
        for column in base_df.columns:
            d1=base_df[column]
            d2=current_df[column]
            is_same_dist=ks_2samp(d1,d2)
            if threshold<=is_same_dist.pvalue:
                is_found=False
            else:
                is_found=True
                status=False
            report.update({column:{
                "p_value":float(is_same_dist.pvalue),
                "drift_status":is_found
                
                }})
        drift_report_file_path = self.data_validation_config.drift_report_file_path

        
        #Create directory
        dir_path = os.path.dirname(drift_report_file_path)
        os.makedirs(dir_path,exist_ok=True)
        write_yaml_file(file_path=drift_report_file_path,content=report)
        return status


    def initiate_data_validation(self):
        try:
            train_dataframe=pd.read_csv(self.data_ingestion_artifact.trained_file_path)
            test_dataframe=pd.read_csv(self.data_ingestion_artifact.test_file_path)
            number_of_col=self.displayYamlFile()
            status=False
            if(len(train_dataframe.columns)==number_of_col and len(test_dataframe.columns)==number_of_col): 
                status=True
            #detect data drift:

            status=self.detect_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path, index=False, header=True

            )

            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path, index=False, header=True
            )
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )
            return data_validation_artifact


        except Exception as e:
            raise CustomException(e,sys)


    