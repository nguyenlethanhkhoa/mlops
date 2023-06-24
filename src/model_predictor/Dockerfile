FROM python:3.9-slim

RUN mkdir /app
WORKDIR /app

COPY . /app

COPY deployment/model_predictor/requirements.txt .
RUN pip install -r requirements.txt

CMD python model_predictor.py --config-path data/model_config/phase-1/prob-1/model-1.yaml --port 8000
