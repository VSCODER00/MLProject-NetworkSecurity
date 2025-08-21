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