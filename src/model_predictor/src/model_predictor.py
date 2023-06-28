import argparse
import json
import logging
import os
import random
import time
from typing import Optional, List

import mlflow
import pandas as pd
import uvicorn
import yaml
from fastapi import FastAPI, Request
from pandas.util import hash_pandas_object
from pydantic import BaseModel

from problem_config import ProblemConst, create_prob_config
from raw_data_processor import RawDataProcessor
from logger import model_1_log, model_2_log
from utils import AppConfig, AppPath

PREDICTOR_API_PORT = 8000


class Data(BaseModel):
    id: str
    rows: list
    columns: list
    prediction: Optional[List[int]]
    drift: Optional[int]


class ModelPredictor:
    def __init__(self, phase, problem, model_name, _logger):
        mlflow.set_tracking_uri(AppConfig.MLFLOW_TRACKING_URI)
        self.logger = _logger

        self.prob_config = create_prob_config(phase, problem)

        # load category_index
        self.category_index = RawDataProcessor.load_category_index(self.prob_config)

        # load model
        model_uri = os.path.join(
            "models:/", f"{phase}_{problem}_{model_name}", "latest"
        )
        self.model = mlflow.pyfunc.load_model(model_uri)

    def predict(self, data: Data):
        start_time = time.time()

        # preprocess
        raw_df = pd.DataFrame(data.rows, columns=data.columns)
        feature_df = RawDataProcessor.apply_category_features(
            raw_df=raw_df,
            categorical_cols=self.prob_config.categorical_cols,
            category_index=self.category_index,
        )

        prediction = self.model.predict(feature_df)
        is_drifted = random.choice([0, 1])

        run_time = round((time.time() - start_time) * 1000, 0)
        logging.info(f"prediction takes {run_time} ms")
        data.prediction = json.dumps(prediction.tolist())
        data.drift = is_drifted

        self.logger.info(json.dumps(data.dict()))
        return {
            "id": data.id,
            "predictions": prediction.tolist(),
            "drift": is_drifted,
        }

    @staticmethod
    def save_request_data(feature_df: pd.DataFrame, captured_data_dir, data_id: str):
        if data_id.strip():
            filename = data_id
        else:
            filename = hash_pandas_object(feature_df).sum()
        output_file_path = os.path.join(captured_data_dir, f"{filename}.parquet")
        feature_df.to_parquet(output_file_path, index=False)
        return output_file_path


class PredictorApi:
    def __init__(self, _models: dict):
        self.app = FastAPI()
        self.models = _models

        @self.app.get("/")
        async def root():
            return {"message": "hello"}

        @self.app.post("/{phase}/{problem}/predict")
        async def predict(data: Data, phase, problem):
            model = self.models[f"{phase}_{problem}"]
            response = model.predict(data)
            return response

    def run(self, port):
        uvicorn.run(self.app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    # default_config_path = (
    #     AppPath.MODEL_CONFIG_DIR
    #     / ProblemConst.PHASE1
    #     / ProblemConst.PROB1
    #     / "model-1.yaml"
    # ).as_posix()

    parser = argparse.ArgumentParser()
    # parser.add_argument("--config-path", type=str, default=default_config_path)
    parser.add_argument("--port", type=int, default=PREDICTOR_API_PORT)
    args = parser.parse_args()

    models = {
        "phase-1_prob-1": ModelPredictor("phase-1", "prob-1", "model-1", model_1_log),
        "phase-1_prob-2": ModelPredictor("phase-1", "prob-2", "model-1", model_2_log),
    }
    api = PredictorApi(models)
    api.run(port=args.port)
