from networksecurity.constants.training_pipeline import constants_config
import os
from datetime import datetime
class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp=timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name=constants_config.PIPELINE_NAME
        self.artifact_name=constants_config.ARTIFACT_DIR
        self.artifact_dir=os.path.join(self.artifact_name,timestamp)
        self.model_dir=os.path.join("final_model")
        self.timestamp: str=timestamp



class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_ingestion_dir:str=os.path.join(
            training_pipeline_config.artifact_dir,constants_config.DATA_INGESTION_DIR
        )
        self.feature_store_file_path: str = os.path.join(
                self.data_ingestion_dir, constants_config.DATA_INGESTION_FEATURE_STORE_DIR, constants_config.FILE_NAME
            )
        self.training_file_path: str = os.path.join(
                self.data_ingestion_dir, constants_config.DATA_INGESTION_INGESTED_DIR, constants_config.TRAIN_FILE_NAME
            )
        self.testing_file_path: str = os.path.join(
                self.data_ingestion_dir, constants_config.DATA_INGESTION_INGESTED_DIR, constants_config.TEST_FILE_NAME
            )
        self.train_test_split_ratio: float = constants_config.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name: str = constants_config.DATA_INGESTION_COLLECTION_NAME
        self.database_name: str = constants_config.DATA_INGESTION_DATABASE_NAME


class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir: str = os.path.join( training_pipeline_config.artifact_dir, constants_config.DATA_VALIDATION_DIR_NAME)
        self.valid_data_dir: str = os.path.join(self.data_validation_dir, constants_config.DATA_VALIDATION_VALID_DIR)
        self.invalid_data_dir: str = os.path.join(self.data_validation_dir, constants_config.DATA_VALIDATION_INVALID_DIR)
        self.valid_train_file_path: str = os.path.join(self.valid_data_dir, constants_config.TRAIN_FILE_NAME)
        self.valid_test_file_path: str = os.path.join(self.valid_data_dir, constants_config.TEST_FILE_NAME)
        self.invalid_train_file_path: str = os.path.join(self.invalid_data_dir, constants_config.TRAIN_FILE_NAME)
        self.invalid_test_file_path: str = os.path.join(self.invalid_data_dir, constants_config.TEST_FILE_NAME)
        self.drift_report_file_path: str = os.path.join(
            self.data_validation_dir,
            constants_config.DATA_VALIDATION_DRIFT_REPORT_DIR,
            constants_config.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME,
        )

class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir: str = os.path.join( training_pipeline_config.artifact_dir,constants_config.DATA_TRANSFORMATION_DIR_NAME )
        self.transformed_train_file_path: str = os.path.join( self.data_transformation_dir,constants_config.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            constants_config.TRAIN_FILE_NAME.replace("csv", "npy"),)
        self.transformed_test_file_path: str = os.path.join(self.data_transformation_dir,  constants_config.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            constants_config.TEST_FILE_NAME.replace("csv", "npy"), )
        self.transformed_object_file_path: str = os.path.join( self.data_transformation_dir, constants_config.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
            constants_config.PREPROCESSING_OBJECT_FILE_NAME)