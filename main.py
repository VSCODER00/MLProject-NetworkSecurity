from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.exception.exception import CustomException
from networksecurity.entity.config import DataIngestionConfig, DataTransformationConfig,DataValidationConfig,TrainingPipelineConfig
import sys
from networksecurity.entity.artifacts import DataIngestionArtifact

if __name__=="__main__":
    training_pipeline_config=TrainingPipelineConfig()
    data_ingestion_config=DataIngestionConfig(training_pipeline_config=training_pipeline_config)
    data_ingestion=DataIngestion(data_ingestion_config=data_ingestion_config)
    print(data_ingestion.initiate_data_ingestion())

    #data validation:
    data_validation_config=DataValidationConfig(training_pipeline_config=training_pipeline_config)
    data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

    data_validation=DataValidation(data_validation_config=data_validation_config,data_ingestion_artifact=data_ingestion_artifact)
    data_validation_artifact=data_validation.initiate_data_validation()
    print(data_validation.initiate_data_validation())

    #data transformation
    data_transformation_config=DataTransformationConfig(training_pipeline_config=training_pipeline_config)
    data_transformation=DataTransformation(data_transformation_config=data_transformation_config,data_validation_artifact=data_validation_artifact)
    print(data_transformation.initiate_data_transformation())
