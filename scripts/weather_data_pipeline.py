import pandas as pd
import requests

def fetch_weather_data():
    API_KEY = "7ea39878086d39a2ab28e22cd4633f9d"
    CITY = "Chennai"
    URL = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"

    response = requests.get(URL)
    data = response.json()

    print(data)  # DEBUG

    if 'list' not in data:
        print("Error: No 'list' in response. Check API key or city.")
        return

    records = []
    for entry in data['list']:
        records.append({
            "datetime": entry['dt_txt'],
            "temperature": entry['main']['temp'],
            "humidity": entry['main']['humidity'],
            "weather": entry['weather'][0]['description']
        })

    df = pd.DataFrame(records)
    df.to_csv("../data/raw_weather_data.csv", index=False)
    print("✅ Raw data saved!")

if __name__ == "__main__":
    fetch_weather_data()
