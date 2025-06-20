import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

def train_model():
    df = pd.read_csv("../data/raw_weather_data.csv")
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['timestamp'] = df['datetime'].astype(int) / 10**9

    X = df[['timestamp']]
    y = df['temperature']

    model = LinearRegression()
    model.fit(X, y)

    joblib.dump(model, "../app/weather_model.pkl")

    print("Model saved!")

if __name__ == "__main__":
    train_model()
