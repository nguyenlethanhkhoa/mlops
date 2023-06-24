# mlops
Sample for MLOps System

```commandline
docker-compose build --no-cache
docker-compose up -d
```

Test
```commandline
curl -X POST http://localhost:8000/phase-1/prob-1/predict -H "Content-Type: application/json" -d @src/model_predictor/data/curl/phase-1/prob-1/payload-1.json
```
