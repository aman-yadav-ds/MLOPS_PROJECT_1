from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataPreprocessor
from src.model_training import ModelTraining
from utils.common_functions import read_yaml
from config.paths_config import *


if __name__ == "__main__":
    ### 1. Data Ingestion
    data_ingestor = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestor.ingest_data()

    ### 2.Data Preprocessing
    preprocessor = DataPreprocessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
    preprocessor.process()

    ### 3. Model Training
    trainer = ModelTraining(PROCESSED_TRAIN_DATA_PATH, PROCESSED_TEST_DATA_PATH, MODEL_OUTPUT_PATH)
    trainer.run()