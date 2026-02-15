import urllib.request
import json

def run(args):
    try:
        # 1. Determine Coordinates
        if args:
            city_query = "%20".join(args)
            print(f"\033[96mSearching for {city_query.replace('%20', ' ')}...\033[0m")
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_query}&count=1&language=en&format=json"
            
            with urllib.request.urlopen(geo_url) as res:
                geo_data = json.loads(res.read().decode())
                if not geo_data.get('results'):
                    print(f"\033[91mError:\033[0m Could not find city '{' '.join(args)}'")
                    return 1
                result = geo_data['results'][0]
                lat, lon = result['latitude'], result['longitude']
                display_name = f"{result['name']}, {result.get('country', '')}"
        else:
            # Default to IP-based location
            print("\033[96mLocating via IP...\033[0m")
            with urllib.request.urlopen("http://ip-api.com/json/") as res:
                loc = json.loads(res.read().decode())
                lat, lon, display_name = loc['lat'], loc['lon'], loc['city']

        # 2. Get Weather for the coordinates found
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        
        with urllib.request.urlopen(weather_url) as res:
            data = json.loads(res.read().decode())
            current = data['current_weather']
            
            print(f"\033[92mWeather for {display_name}:\033[0m")
            print(f"Temperature: {current['temperature']}°C")
            print(f"Wind Speed:  {current['windspeed']} km/h")
            return 0

    except Exception as e:
        print(f"\033[91mWeather Error:\033[0m {e}")
        return 1
