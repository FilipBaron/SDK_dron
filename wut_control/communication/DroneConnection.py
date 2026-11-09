from typing import Self

import logging
import threading
from dataclasses import dataclass, field

import cflib.crtp
from cflib.crazyflie import Crazyflie

logger = logging.getLogger(__name__)


@dataclass
class DroneConnection:
    uri: str
    _cf: Crazyflie = field(init=False, repr=False)
    _connected: bool = field(default=False, init=False, repr=False)
    _connected_event: threading.Event = field(
        default_factory=threading.Event, init=False, repr=False
    )
    _disconnected_event: threading.Event = field(
        default_factory=threading.Event, init=False, repr=False
    )
    _last_error: str | None = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        cflib.crtp.init_drivers()
        self._cf = Crazyflie(rw_cache="./cache")

        self._cf.connected.add_callback(self._on_connected)
        self._cf.disconnected.add_callback(self._on_disconnected)
        self._cf.connection_failed.add_callback(self._on_connection_failed)
        self._cf.connection_lost.add_callback(self._on_connection_lost)

    @property
    def is_connected(self) -> bool:
        return self._connected and self._cf.is_link_open()

    @property
    def crazyflie(self) -> Crazyflie:
        return self._cf

    @staticmethod
    def scan_for_devices() -> list[str]:
        cflib.crtp.init_drivers()
        found = cflib.crtp.scan_interfaces()
        return [uri for uri, _ in found]

    def connect(self, timeout: float = 10.0) -> None:
        if self._connected:
            logger.warning("Already connected to %s", self.uri)
            return

        logger.info("Connecting to %s...", self.uri)
        self._connected_event.clear()
        self._disconnected_event.clear()
        self._last_error = None

        self._cf.open_link(self.uri)

        if not self._connected_event.wait(timeout=timeout):
            self.disconnect()
            raise TimeoutError(f"Connection to {self.uri} timed out after {timeout}s")

        if not self._connected:
            raise ConnectionError(f"Failed to connect to {self.uri}: {self._last_error}")

        logger.info("Connected to %s", self.uri)

    def disconnect(self, timeout: float = 5.0) -> None:
        if not self._connected and not self._cf.is_link_open():
            return

        logger.info("Disconnecting from %s...", self.uri)
        self._disconnected_event.clear()
        self._cf.close_link()

        self._disconnected_event.wait(timeout=timeout)
        self._connected = False
        logger.info("Disconnected from %s", self.uri)

    def _on_connected(self, uri: str) -> None:
        self._connected = True
        self._connected_event.set()
        logger.info("Link connected: %s", uri)

    def _on_disconnected(self, uri: str) -> None:
        self._connected = False
        self._disconnected_event.set()
        logger.info("Link disconnected: %s", uri)

    def _on_connection_failed(self, uri: str, msg: str) -> None:
        self._connected = False
        self._last_error = msg
        self._connected_event.set()
        logger.error("Connection failed to %s: %s", uri, msg)

    def _on_connection_lost(self, uri: str, msg: str) -> None:
        self._connected = False
        self._disconnected_event.set()
        logger.warning("Connection lost to %s: %s", uri, msg)

    def __enter__(self) -> Self:
        self.connect()
        return self

    def __exit__(self, *args: object) -> None:
        self.disconnect()
