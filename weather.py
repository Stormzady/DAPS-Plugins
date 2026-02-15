import urllib.request
import json

def run(args):
    try:
        # 1. Get location based on IP (or city if we wanted to add a search later)
        # For now, let's stick to IP-based for speed.
        print("\033[96mLocating...\033[0m")
        with urllib.request.urlopen("http://ip-api.com/json/") as loc_res:
            location = json.loads(loc_res.read().decode())
            lat, lon = location['lat'], location['lon']
            city = location['city']

        # 2. Get weather from Open-Meteo
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        
        with urllib.request.urlopen(url) as weather_res:
            data = json.loads(weather_res.read().decode())
            current = data['current_weather']
            temp = current['temperature']
            wind = current['windspeed']

            print(f"\033[92mWeather for {city}:\033[0m")
            print(f"Temperature: {temp}°C")
            print(f"Wind Speed:  {wind} km/h")
            return 0

    except Exception as e:
        print(f"\033[91mWeather Error:\033[0m {e}")
        return 1
