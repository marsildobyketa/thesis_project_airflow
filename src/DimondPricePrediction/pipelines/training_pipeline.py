from src.DimondPricePrediction.components.data_ingestion import DataIngestion
from src.DimondPricePrediction.components.data_transformation import DataTransformation
from src.DimondPricePrediction.components.model_trainer import ModelTrainer
from src.DimondPricePrediction.components.model_evaluation import ModelEvaluation
from src.DimondPricePrediction.utils.utils import load_object
import os
import sys
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn
import numpy as np
import pickle
from src.DimondPricePrediction.utils.utils import load_object
import dagshub


import pandas as pd
import numpy as np
import os
import sys
from src.DimondPricePrediction.logger import logging
from src.DimondPricePrediction.exception import customexception
from dataclasses import dataclass
from src.DimondPricePrediction.utils.utils import save_object
from src.DimondPricePrediction.utils.utils import evaluate_model
from src.DimondPricePrediction.components.model_evaluation import ModelEvaluation

from sklearn.linear_model import LinearRegression, Ridge,Lasso,ElasticNet

import os
import sys
from src.DimondPricePrediction.logger import logging
from src.DimondPricePrediction.exception import customexception
import pandas as pd
class TrainingPipeline:
    def start_data_ingestion(self):
        try:
            data_ingestion=DataIngestion()
            train_data_path,test_data_path=data_ingestion.initiate_data_ingestion()
            return train_data_path,test_data_path
        except Exception as e:
            raise customexception(e,sys)
        
    def start_data_transformation(self,train_data_path,test_data_path):
        try:
            data_transformation = DataTransformation()
            train_arr,test_arr=data_transformation.initialize_data_transformation(train_data_path,test_data_path)
            return train_arr,test_arr
        except Exception as e:
            raise customexception(e,sys)
    
    def start_model_training(self,train_arr,test_arr):
        try:
            model_trainer=ModelTrainer()
            model_trainer.initate_model_training(train_arr,test_arr)
            print ("Model Training Done")
        except Exception as e:
            raise customexception(e,sys)
                
    def start_trainig(self):
        try:
            train_data_path,test_data_path=self.start_data_ingestion()
            train_arr,test_arr=self.start_data_transformation(train_data_path,test_data_path)
            self.start_model_training(train_arr,test_arr)
            #evaluation_pipeline.initiate_model_evaluation(train_arr,test_arr)
        except Exception as e:
            raise customexception(e,sys)
        

if __name__=="__main__":

    training_pipeline=TrainingPipeline()
    training_pipeline.start_trainig()
    

    
    


        

