from fastapi import FastAPI, Query
import joblib
import pandas as pd
import datetime

app = FastAPI()
model = joblib.load("weather_model.pkl")

@app.get("/")
def read_root():
    return {"message": "Weather Forecast API"}

@app.get("/predict")
def predict(date: str = Query(..., description="Date in YYYY-MM-DD format")):
    dt = pd.to_datetime(date)
    timestamp = dt.value / 10**9
    prediction = model.predict([[timestamp]])
    return {"date": date, "predicted_temperature": round(prediction[0], 2)}
