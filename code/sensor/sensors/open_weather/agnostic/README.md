# OpenWeather Current Weather Data

Client for OpenWeather's Current Weather Data API. Documentation is available [here](https://openweathermap.org/current).

## Setup
- Sign up for an API key [here](https://home.openweathermap.org/users/sign_up)
- Once your account is active, view your API keys [here](https://home.openweathermap.org/api_keys)
- Copy the key into your configuration, along with your desired coordinates:
    ```json
    ...
        "open_weather": {
            "latitude": 47.578407901391955,
            "longitude": -121.97813275174478,
            "app_id": "this is your API key"
        }
    ...
    ```