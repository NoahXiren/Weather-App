from django.shortcuts import render
import requests
import datetime

def home(request):
    API_KEY = open("C:\\Users\\User\\OneDrive\\Documents\\Weather\\API_KEY", "r").read().strip()
    if request.method != "POST":
        return render(request, 'weather/home.html')
   
    CITY = request.POST.get('city')
    now_weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    future_weather_url = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"
    try:
        current_weather, forecast_weather = get_now_and_future_weather(CITY, API_KEY, now_weather_url, future_weather_url)
        context = {
            "current_weather": current_weather,
            "forecast_weather": forecast_weather,
        }
    except requests.RequestException as e:
        context = {"error": f"An error occurred: {str(e)}"}
        
    return render(request, "weather/home.html", context)
   
def get_now_and_future_weather(city, api_key, now_weather, future_weather):
    """raise_for_status(): this method is to quickly check
    if the request was successful and raise an exception if it wasn't."""
    now_response = requests.get(now_weather)
    now_response.raise_for_status()
    now_data = now_response.json()
   
    forecast_response = requests.get(future_weather)
    forecast_response.raise_for_status()
    future_data = forecast_response.json()

    weather_info = {
        "city": now_data['name'],
        "temperature": now_data['main']['temp'],
        "feels_like": now_data['main']['feels_like'],
        "min_temp": now_data['main']['temp_min'],
        "max_temp": now_data['main']['temp_max'],
        "description": now_data['weather'][0]['description'],
        "icon": now_data['weather'][0]['icon'],
        "humidity": now_data['main']['humidity'],
        "wind_speed": now_data['wind']['speed'],
        "pressure": now_data['main']['pressure'],
        "country": now_data['sys']['country'],
        "clouds": now_data['clouds']['all'],
        "day": datetime.datetime.now().strftime("%a"),  # Short day name (e.g., Thu
        "now_time": datetime.datetime.now().strftime("%H:%M"),
        "sunrise": datetime.datetime.fromtimestamp(now_data['sys']['sunrise']).strftime("%H:%M:%S"),
        "sunset": datetime.datetime.fromtimestamp(now_data['sys']['sunset']).strftime("%H:%M:%S"),
    }

    forecast_data = []
    seen_days = set()
    for forecast in future_data['list']:
        forecast_date = datetime.datetime.fromtimestamp(forecast['dt'])
        day = forecast_date.strftime("%A")
        if day not in seen_days and len(seen_days) < 5:
            seen_days.add(day)
            forecast_data.append({
                "day": day,
                "date": forecast_date.strftime("%Y-%m-%d"),
                "temp": forecast['main']['temp'],
                "min_temp": forecast['main']['temp_min'],
                "max_temp": forecast['main']['temp_max'],
                "description": forecast['weather'][0]['description'],
                "icon": forecast['weather'][0]['icon'],
            })
    
    return weather_info, forecast_data

