from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

import os
import sys
import numpy as np
import pandas as pd
import pymongo
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_collection_as_dataframe(self):
        """
        Read data from MongoDB
        """
        try:
            logging.info("Connecting to MongoDB")

            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name

            print("DB:", database_name)
            print("Collection:", collection_name)

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)

            collection = self.mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))

            print("DEBUG: Data shape:", df.shape)

            if df.shape[0] == 0:
                raise Exception("No data found in MongoDB collection")

            if "_id" in df.columns:
                df = df.drop(columns=["_id"])

            df.replace({"na": np.nan}, inplace=True)

            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_data_into_feature_store(self, dataframe: pd.DataFrame):
        try:
            logging.info("Exporting data into feature store")

            feature_store_file_path = self.data_ingestion_config.feature_store_file_path

            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)

            dataframe.to_csv(feature_store_file_path, index=False, header=True)

            logging.info(f"Data saved at: {feature_store_file_path}")

            return dataframe

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        try:
            logging.info("Starting train-test split")

            print("DEBUG: Data shape before split:", dataframe.shape)

            if dataframe.shape[0] == 0:
                raise Exception("Dataset is empty before train_test_split")

            train_set, test_set = train_test_split(
                dataframe,
                test_size=self.data_ingestion_config.train_test_split_ratio,
                random_state=42
            )

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_set.to_csv(
                self.data_ingestion_config.training_file_path,
                index=False,
                header=True
            )

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path,
                index=False,
                header=True
            )

            logging.info("Train and test files saved successfully")

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_ingestion(self):
        try:
            logging.info("Starting data ingestion process")

            dataframe = self.export_collection_as_dataframe()

            dataframe = self.export_data_into_feature_store(dataframe)

            self.split_data_as_train_test(dataframe)

            dataingestionartifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )

            logging.info("Data ingestion completed successfully")

            return dataingestionartifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)