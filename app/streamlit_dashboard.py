# 📁 streamlit_dashboard.py

import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# ✅ OpenWeatherMap API key
API_KEY = "7ea39878086d39a2ab28e22cd4633f9d"  # Replace with your real key

# ----------------------------------------------
# 🎨 Streamlit Page Config
st.set_page_config(
    page_title="🌤️ Weather Dashboard",
    page_icon="🌤️",
    layout="wide",
)

# ----------------------------------------------
# 🏷️ Sidebar styling
st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/1163/1163661.png",
    width=120,
)
st.sidebar.title("☀️ Weather Dashboard")
st.sidebar.markdown(
    """
    Welcome to the **Weather Forecast Dashboard**!  
    Enter a city name and see the hourly temperature trend.
    """
)

# ----------------------------------------------
# 📍 City input in sidebar
city = st.sidebar.text_input("Enter City Name", value="Chennai")

# 🔘 Button to get weather in sidebar
show_forecast = st.sidebar.button("Get Weather Forecast")

# ----------------------------------------------
# 🎉 Intro landing page (shows before forecast)
if not show_forecast:
    st.markdown(
        """
        <div style="text-align: center; margin-top: 100px;">
            <h1 style="font-size: 60px;">🌤️ Weather Forecast App</h1>
            <p style="font-size: 24px; color: #ddd;">Check hourly temperature trends for any city!</p>
            <p style="font-size: 20px; color: #aaa;">➡️ Use the sidebar to enter a city and click "Get Weather Forecast".</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ----------------------------------------------
# 📊 Show forecast only if button clicked
if show_forecast:
    # 🌐 API Call
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()

    if response.get("cod") != "200":
        st.error(f"Error: {response.get('message')}")
    else:
        # ✅ Parse forecast
        forecast = []
        for entry in response["list"]:
            forecast.append({
                "datetime": entry["dt_txt"],
                "temperature": entry["main"]["temp"],
                "condition": entry["weather"][0]["main"],
                "description": entry["weather"][0]["description"].title(),
            })
        df = pd.DataFrame(forecast)

        # ----------------------------------------------
        # 📈 Beautiful Plotly Chart with clear axis labels
        st.header(f"📈 Hourly Temperature Forecast for {city}")

        fig = px.line(
            df,
            x="datetime",
            y="temperature",
            labels={
                "datetime": "Date & Time",
                "temperature": "Temperature (°C)"
            },
            title=f"🌈 Temperature Trend - Next 5 Days",
            markers=True,
        )

        fig.update_traces(
            line=dict(color="royalblue", width=3, shape='spline'),
            marker=dict(size=8, color="white", line=dict(width=2, color="royalblue")),
        )

        fig.update_layout(
            xaxis=dict(
                title=dict(
                    text="Date & Time",
                    font=dict(size=16, color="white")  # ✅ explicit color for dark mode
                ),
                showgrid=True,
                gridcolor="rgba(173, 216, 230, 0.3)",
                zeroline=False,
                tickangle=-45,
            ),
            yaxis=dict(
                title=dict(
                    text="Temperature (°C)",
                    font=dict(size=16, color="white")  # ✅ explicit color for dark mode
                ),
                showgrid=True,
                gridcolor="rgba(173, 216, 230, 0.3)",
                zeroline=False,
            ),
            title=dict(
                text=f"🌈 Temperature Trend - Next 5 Days",
                font=dict(size=24, color="white"),  # ✅ chart title in white
                x=0.5,
                xanchor='center',
            ),
            plot_bgcolor="rgba(0,0,0,0)",  # transparent plot background
            paper_bgcolor="rgba(0,0,0,0)",  # transparent paper background
            font=dict(color="white", family="Arial"),  # ✅ base font in white
            margin=dict(l=40, r=40, t=80, b=40),
            hovermode="x unified",
            showlegend=False,
        )

        st.plotly_chart(fig, use_container_width=True)

        # ----------------------------------------------
        # 🗂️ Two columns: detailed forecast + raw data
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader(f"🌦️ Detailed Forecast (Next 24 Hours)")
            for i in range(min(8, len(df))):
                row = df.iloc[i]
                icon = {
                    "Clear": "☀️",
                    "Clouds": "☁️",
                    "Rain": "🌧️",
                    "Thunderstorm": "⛈️",
                    "Snow": "❄️",
                    "Drizzle": "🌦️",
                    "Mist": "🌫️",
                }.get(row["condition"], "🌈")
                with st.container():
                    st.write(
                        f"**{row['datetime']}** | {icon} **{row['description']}** | 🌡️ **{row['temperature']}°C**"
                    )
                    st.markdown("---")

        with col2:
            st.subheader("📋 Raw Forecast Data")
            st.dataframe(df, height=400)

# ----------------------------------------------
# ✅ Footer
st.markdown("---")
st.caption(
    "Made with ❤️ using [OpenWeatherMap](https://openweathermap.org/), "
    "[Plotly](https://plotly.com/python/), and [Streamlit](https://streamlit.io/)."
)
