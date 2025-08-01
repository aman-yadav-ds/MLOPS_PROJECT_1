import os
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import * #All paths defined in paths_config.py will be loaded here
from utils.common_functions import read_yaml

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self, config):
        self.config = config["data_ingestion"] #This will ready only the data_ingestion configuration from config.yaml
        self.bucket_name = self.config["bucket_name"]   #set bucket_name from config.yaml
        self.file_name = self.config["bucket_file_name"]    #set bucket_file_name from config.yaml
        self.train_test_ratio = self.config["train_ratio"]  #set train_ratio from config.yaml

        os.makedirs(RAW_DIR, exist_ok=True)

        logger.info(f"Data Ingestion Started with {self.bucket_name} and file is {self.file_name}")
    
    def download_csv_from_gcp(self):
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_name)

            blob.download_to_filename(RAW_FILE_PATH)

            logger.info(f"CSV file is successfully downloaded to {RAW_FILE_PATH}")
        
        except Exception as e:
            logger.error("Error while Downloading the CSV file")
            raise CustomException("Failed to download CSV file", e)
    
    def split_data(self):
        try:
            logger.info("Starting the splitting process.")
            data = pd.read_csv(RAW_FILE_PATH)
            train_data, test_data = train_test_split(data, test_size=1-self.train_test_ratio, random_state=42)

            train_data.to_csv(TRAIN_FILE_PATH)
            test_data.to_csv(TEST_FILE_PATH)

            logger.info(f"Train data saved to {TRAIN_FILE_PATH}")
            logger.info(f"Test data saved to {TEST_FILE_PATH}")
        
        except Exception as e:
            logger.error("Error while splitting data.")
            raise CustomException("Failed to split data in Training and Testing sets.", e)
    
    def ingest_data(self):
        try:
            logger.info("Starting Data Ingestion process.")
            self.download_csv_from_gcp()
            self.split_data()
            logger.info("Data Ingestion completed successfully.")
        
        except CustomException as ce:
            logger.error(f"CustomException: {str.ce}")
        
        finally:
            logger.info("Data Ingestion step completed")

if __name__ == "__main__":
    data_ingestor = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestor.ingest_data()