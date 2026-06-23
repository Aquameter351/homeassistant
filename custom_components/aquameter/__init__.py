from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.components.bluetooth import async_discovered_service_info

from .bluetooth import AquaMeterBluetoothClient
from .const import DOMAIN, SERVICE_UUID

PLATFORMS = ["sensor"]


async def async_setup(hass: HomeAssistant, config: dict):
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})

    ble_device = None

    for info in async_discovered_service_info(hass, connectable=True):
        uuids = [u.lower() for u in info.service_uuids]
        if SERVICE_UUID.lower() in uuids:
            ble_device = info.device
            break

    if ble_device is None:
        raise ConfigEntryNotReady("AquaMeter Bluetooth device not found")

    client = AquaMeterBluetoothClient(ble_device)
    await client.connect()

    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    data = hass.data[DOMAIN].pop(entry.entry_id, None)

    if data:
        await data["client"].disconnect()

    return unload_ok