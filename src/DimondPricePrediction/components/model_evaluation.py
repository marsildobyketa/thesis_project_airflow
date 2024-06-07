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


class ModelEvaluation:

    def eval_metrics(self, actual, pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))  # here is RMSE
        mae = mean_absolute_error(actual, pred)  # here is MAE
        r2 = r2_score(actual, pred)  # here is r3 value
        return rmse, mae, r2

    def initiate_model_evaluation(self, train_array, test_array):
        try:
            X_test, y_test = (test_array[:, :-1], test_array[:, -1])

            model_path = os.path.join("artifacts", "model.pkl")
            model = load_object(model_path)

            dagshub.init(repo_owner='marsildobyketa', repo_name='thesis_project_airflow', mlflow=True)
            print("model evaluation")
            

            with mlflow.start_run():

                predicted_qualities = model.predict(X_test)

                (rmse, mae, r2) = self.eval_metrics(y_test, predicted_qualities)

                mlflow.log_metric("rmse", rmse)
                mlflow.log_metric("r2", r2)
                mlflow.log_metric("mae", mae)


                mlflow.sklearn.log_model(
                    model, "model", registered_model_name="ml_model"
                 )
 

        except Exception as e:
            raise e
