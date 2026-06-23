import logging
from typing import Optional

from bleak_retry_connector import BleakClientWithServiceCache, establish_connection

from .const import TX_UUID
from .parser import AquaMeterData, parse_q_packet

_LOGGER = logging.getLogger(__name__)


class AquaMeterBluetoothClient:
    def __init__(self, ble_device):
        self.ble_device = ble_device
        self.client: Optional[BleakClientWithServiceCache] = None
        self.latest_data: Optional[AquaMeterData] = None
        self._buffer = ""
        self._callbacks = []

    def register_callback(self, callback):
        self._callbacks.append(callback)

    async def connect(self):
        _LOGGER.info("Connecting to AquaMeter: %s", self.ble_device.address)

        self.client = await establish_connection(
            BleakClientWithServiceCache,
            self.ble_device,
            self.ble_device.address,
        )

        await self.client.start_notify(TX_UUID, self._notification_handler)

        _LOGGER.info("AquaMeter connected and notifications enabled")

    async def disconnect(self):
        if self.client and self.client.is_connected:
            await self.client.stop_notify(TX_UUID)
            await self.client.disconnect()

        self.client = None

    def _notification_handler(self, sender, data: bytearray):
        try:
            chunk = data.decode("utf-8")
        except UnicodeDecodeError:
            _LOGGER.warning("Received invalid AquaMeter BLE data: %s", data)
            return

        self._buffer += chunk

        while "\n" in self._buffer:
            line, self._buffer = self._buffer.split("\n", 1)
            self._handle_line(line.strip())

    def _handle_line(self, line: str):
        if not line:
            return

        _LOGGER.warning("AquaMeter RX: %s", line)

        data = parse_q_packet(line)

        if data is None:
            return

        self.latest_data = data

        for callback in self._callbacks:
            callback(data)