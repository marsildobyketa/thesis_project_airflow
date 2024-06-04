# Project thesis 

# Marsildo Byketa


## MLflow

[Documentation](https://mlflow.org/docs/latest/index.html)


##### local cmd
- mlflow ui

### dagshub
[dagshub](https://dagshub.com/)

MLFLOW_TRACKING_URI=https://dagshub.com/sunny.savita/fsdsmendtoend.mlflow \
MLFLOW_TRACKING_USERNAME=sunny.savita \
MLFLOW_TRACKING_PASSWORD=3c2c8cd1436ad32b510cfdd84944a528ba4fb650 \
python script.py

Run this to export as env variables:

```bash

export MLFLOW_TRACKING_URI=https://dagshub.com/sunny.savita/fsdsmendtoend.mlflow
export MLFLOW_TRACKING_USERNAME=sunny.savita
export MLFLOW_TRACKING_PASSWORD=3c2c8cd1436ad32b510cfdd84944a528ba4fb650

```
### DVC cmd
- dvc init
- dvc repro
- dvc dag

