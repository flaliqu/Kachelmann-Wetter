import json
import logging
from homeassistant.components.weather import (
    WeatherEntity,
    WeatherEntityFeature
)
from homeassistant.const import TEMP_CELSIUS, SPEED_KILOMETERS_PER_HOUR, PRESSURE_HPA
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    with open(hass.config.path("custom_components/kachelmann_weather/demo_data.json")) as f:
        data = json.load(f)
    async_add_entities([KachelmannWeather(data)], True)

class KachelmannWeather(WeatherEntity):
    _attr_name = "Kachelmann Wetter"
    _attr_supported_features = WeatherEntityFeature.FORECAST_HOURLY | WeatherEntityFeature.FORECAST_DAILY
    _attr_temperature_unit = TEMP_CELSIUS
    _attr_wind_speed_unit = SPEED_KILOMETERS_PER_HOUR
    _attr_pressure_unit = PRESSURE_HPA

    def __init__(self, data):
        self._data = data

    def update(self):
        pass

    @property
    def temperature(self):
        return self._data["current"]["temperature"]

    @property
    def humidity(self):
        return self._data["current"]["humidity"]

    @property
    def pressure(self):
        return self._data["current"]["pressure"]

    @property
    def wind_speed(self):
        return self._data["current"]["wind_speed"]

    @property
    def condition(self):
        return self._data["current"]["condition"]

    @property
    def forecast(self):
        return [
            {"datetime": f"2025-08-02T{hour['hour']:02d}:00:00", "temperature": hour["temperature"], "condition": hour["condition"]}
            for hour in self._data["hourly"]
        ]

    @property
    def forecast_daily(self):
        return [
            {"datetime": f"2025-08-{2 + i:02d}", "temperature": day["temperature"], "condition": day["condition"]}
            for i, day in enumerate(self._data["daily"])
        ]
