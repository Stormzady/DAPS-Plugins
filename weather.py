import urllib.request
import sys

def run(args):
    # If a city is provided, use it. Otherwise, use IP-based detection.
    if args:
        city = "+".join(args)
        url = f"https://wttr.in/{city}?format=3"
    else:
        # Default: Detect weather by IP address
        url = "https://wttr.in/?format=3"

    try:
        # Fetch the weather data
        with urllib.request.urlopen(url) as response:
            weather_report = response.read().decode('utf8')
            print(f"\033[96mWeather report:\033[0m {weather_report}")
            return 0
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return 1
