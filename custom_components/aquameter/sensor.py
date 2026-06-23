from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfVolume, PERCENTAGE

from .const import DOMAIN


SENSORS = [
    ("water", "Water Remaining", UnitOfVolume.LITERS),
    ("percent", "Tank Level", PERCENTAGE),
    ("flow", "Flow Rate", "L/min"),
    ("today", "Today Consumption", UnitOfVolume.LITERS),
]


async def async_setup_entry(hass, entry, async_add_entities):
    client = hass.data[DOMAIN][entry.entry_id]["client"]

    entities = [
        AquaMeterSensor(client, key, name, unit)
        for key, name, unit in SENSORS
    ]

    async_add_entities(entities)


class AquaMeterSensor(SensorEntity):
    def __init__(self, client, key, name, unit):
        self.client = client
        self.key = key

        self._attr_name = f"AquaMeter {name}"
        self._attr_native_unit_of_measurement = unit
        self._attr_native_value = None

        client.register_callback(self._handle_update)

    def _handle_update(self, data):
        if self.key == "water":
            self._attr_native_value = data.water

        elif self.key == "percent":
            if data.capacity > 0:
                self._attr_native_value = round((data.water / data.capacity) * 100, 1)
            else:
                self._attr_native_value = None

        elif self.key == "flow":
            self._attr_native_value = data.flow

        elif self.key == "today":
            self._attr_native_value = data.today

        self.schedule_update_ha_state(True)