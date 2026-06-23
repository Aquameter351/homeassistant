from homeassistant.components.sensor import SensorEntity


async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([
        AquaMeterSensor("Water Remaining", "L"),
        AquaMeterSensor("Tank Level", "%"),
        AquaMeterSensor("Flow Rate", "L/min"),
        AquaMeterSensor("Today Consumption", "L"),
    ])


class AquaMeterSensor(SensorEntity):
    def __init__(self, name, unit):
        self._attr_name = f"AquaMeter {name}"
        self._attr_native_unit_of_measurement = unit
        self._attr_native_value = None