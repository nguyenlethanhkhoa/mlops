FROM base:latest

RUN mkdir /app
WORKDIR /app

COPY . /app

WORKDIR /app/src

CMD python model_predictor.py --port 8000
