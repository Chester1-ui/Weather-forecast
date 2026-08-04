import streamlit as st
from utils.weather import get_weather, get_forecast
import plotly.express as px
from datetime import datetime


st.title("🌦️ Weather Dashboard")

st.write("Search for the current weather in any city around the world.")


city = st.text_input("Enter a city")

search = st.button("Get Weather")


if search:

    if city == "":

        st.warning("Please enter a city name.")

    else:

        with st.spinner("Fetching weather data..."):

            weather = get_weather(city)
            forecast = get_forecast(city)


        if weather is None:

            st.error("City not found. Please check your spelling.")

        else:

            # CURRENT WEATHER

            st.header(f"{weather['name']} Weather")


            temperature = weather["main"]["temp"]
            feels_like = weather["main"]["feels_like"]
            humidity = weather["main"]["humidity"]
            wind = weather["wind"]["speed"]
            description = weather["weather"][0]["description"]

            icon = weather["weather"][0]["icon"]

            icon_url = (
                f"https://openweathermap.org/img/wn/{icon}@2x.png"
            )


            st.image(icon_url)

            st.write(
                f"Condition: {description.title()}"
            )


            col1, col2 = st.columns(2)


            with col1:

                st.metric(
                    "Temperature",
                    f"{temperature} °C"
                )

                st.metric(
                    "Humidity",
                    f"{humidity}%"
                )


            with col2:

                st.metric(
                    "Feels Like",
                    f"{feels_like} °C"
                )

                st.metric(
                    "Wind Speed",
                    f"{wind} m/s"
                )



            # FORECAST

            if forecast is not None:

                st.subheader("5 Day Forecast")


                forecast_list = forecast["list"]


                days = []
                temperatures = []


                cols = st.columns(5)


                for index, item in enumerate(forecast_list[::8]):

                    date = datetime.strptime(
                        item["dt_txt"],
                        "%Y-%m-%d %H:%M:%S"
                    )


                    day = date.strftime("%a %d %b")


                    temp = item["main"]["temp"]


                    description = (
                        item["weather"][0]["description"]
                    )


                    icon = (
                        item["weather"][0]["icon"]
                    )


                    icon_url = (
                        f"https://openweathermap.org/img/wn/{icon}@2x.png"
                    )


                    days.append(day)

                    temperatures.append(temp)


                    with cols[index]:

                        st.write(day)

                        st.image(icon_url)

                        st.write(
                            f"{temp} °C"
                        )

                        st.write(
                            description.title()
                        )



                # GRAPH

                chart_data = {

                    "Day": days,

                    "Temperature": temperatures

                }


                fig = px.line(

                    chart_data,

                    x="Day",

                    y="Temperature",

                    title="5 Day Temperature Forecast"

                )


                st.plotly_chart(fig)