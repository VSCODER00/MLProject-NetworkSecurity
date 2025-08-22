import numpy as np
import pandas as pd
import os

TARGET_COLUMN="Result"
PIPELINE_NAME="NetworkSecurity"
ARTIFACT_DIR="Artifacts"
FILE_NAME="phishingData.csv"
TRAIN_FILE_NAME="train.csv"
TEST_FILE_NAME="test.csv"

DATA_INGESTION_DIR="data_ingestion"
DATA_INGESTION_COLLECTION_NAME="dataset"
DATA_INGESTION_INGESTED_DIR="ingested"
DATA_INGESTION_DATABASE_NAME="ML-NSProj"
DATA_INGESTION_FEATURE_STORE_DIR="feature_store"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO=0.2

DATA_VALIDATION_DIR_NAME = "data_validation"
DATA_VALIDATION_VALID_DIR = "validated"
DATA_VALIDATION_INVALID_DIR = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME = "report.yaml"

SCHEMA_FILE_PATH = os.path.join("data_schema", "schema.yaml")

DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"

PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform",
}
DATA_TRANSFORMATION_TRAIN_FILE_PATH: str = "train.npy"

DATA_TRANSFORMATION_TEST_FILE_PATH: str = "test.npy"