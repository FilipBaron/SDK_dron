from __future__ import annotations
from . import _core
import time


class Drone:
    """
    Main interface of the wut-control SDK for autonomous drone control.
    Provides flight control, sensor readings, and camera feed access from a single class.
    """

    def __init__(
            self,
            uri: str | None = None,
            backend: _core.IDroneBackend | None = None,
    ) -> None:
        self._uri = uri
        self._backend: _core.IDroneBackend = (
            backend if backend is not None else _core.CrazyflieBackend()
        )

    @staticmethod
    def scan_for_devices(
            start_channel: int = 0,
            end_channel: int = 125,
            address: int = 0xE7E7E7E7E7,
    ) -> list[str]:
        """
        Scans the environment for available drones.
        Returns a list of found interfaces/URIs (e.g., 'radio://0/80/2M/E7E7E7E7E7').
        """
        scanner = _core.CrazyflieBackend()
        found = scanner.scan(start_channel, end_channel, address)
        return [device.uri for device in found]

    def connect(self, uri: str | None = None, timeout: float = 10.0) -> None:
        """Establishes a connection with the drone within the given timeout."""
        deadline = time.monotonic() + timeout
        last_error: Exception | None = None

        while True:
            try:
                target_uri = uri or self._uri
                if target_uri is None:
                    devices = self._backend.scan()
                    if not devices:
                        raise RuntimeError("No Crazyflie drones found during scan.")
                    target_uri = devices[0].uri

                self._backend.connect(target_uri)
                self._uri = target_uri
                return
            except Exception as exc:
                last_error = exc
                if time.monotonic() >= deadline:
                    raise TimeoutError(
                        f"Failed to connect within {timeout}s: {last_error}"
                    ) from last_error
                time.sleep(0.2)

    def disconnect(self) -> None:
        """Safely terminates the connection with the drone."""
        self._backend.disconnect()

    def is_connected(self) -> bool:
        """Returns the current connection status."""
        return self._backend.is_connected()

    def connection(self) -> _core.IDroneBackend:
        """Direct access to the underlying backend (e.g. for swarm logic)."""
        return self._backend

    def get_battery_level(self) -> float:
        """Returns the current battery voltage or percentage."""
        pass

    def get_sensor_status(self) -> dict:
        """Returns the operational status of individual sensors (e.g., IMU, lidar)."""
        pass

    def is_ready_to_fly(self) -> bool:
        """
        Evaluates if the drone is ready for takeoff.
        Checks connection status, battery levels, and sensor health.
        """
        pass

    def health_check(self) -> dict:
        """
        Aggregates full telemetry and system health parameters.
        """
        return {
            "connected": self.is_connected(),
            "battery": self.get_battery_level(),
            "sensors": self.get_sensor_status(),
            "ready_to_fly": self.is_ready_to_fly(),
        }

    def start_motors(self):
        """Spins up the motors to idle speed without taking off."""
        pass

    def stop_motors(self):
        """Stops the motors gracefully."""
        pass

    def emergency_stop(self):
        """
        EMERGENCY KILL SWITCH.
        Immediately cuts all power to the motors. The drone will fall.
        """
        self._backend.emergency_stop()

    def set_altitude(self, target_height: float, velocity: float = 0.2):
        """Ascends or descends to the specified altitude."""
        pass

    def rotate(self, degrees: float, angular_velocity: float = 50.0):
        """
        Rotates the drone around its Z axis (yaw).
        Useful for panning the camera.
        """
        pass

    def stop(self):
        """
        Halts all current movement commands and forces the drone to hover in place.
        """
        pass

    def go_to_position(self, x: float, y: float, z: float, velocity: float = 0.2):
        """
        Moves the drone to a specific (X, Y, Z) coordinate in the current coordinate system,
        without needing to calculate relative distances.
        """
        pass

    def takeoff(self, target_height: float = 0.5):
        """Sends the takeoff command and ascends to the specified target height."""
        pass

    def land(self):
        """Sends the safe landing command."""
        pass

    def go_forward(self, distance: float, velocity: float = 0.2):
        """Flies forward by the specified distance in meters."""
        pass

    def go_backward(self, distance: float, velocity: float = 0.2):
        """Flies backward by the specified distance in meters."""
        pass

    def go_left(self, distance: float, velocity: float = 0.2):
        """Flies left by the specified distance in meters."""
        pass

    def go_right(self, distance: float, velocity: float = 0.2):
        """Flies right by the specified distance in meters."""
        pass

    def get_lidar_distances(self) -> dict[str, float]:
        """Returns the current distances measured by the lidars."""
        pass

    def get_camera_frame(self):
        """Provides the current video frame from the camera stream."""
        pass

    def get_estimated_position(self) -> tuple[float, float, float]:
        """Returns the estimated position of the drone (X, Y, Z)."""
        pass

    def move_by_vector(self, dx: float, dy: float, dz: float, velocity: float = 0.2):
        """
        Moves the drone by a specified vector (dx, dy, dz) in meters relative to its current
        position.
        """
        pass

    def hello(self):
        _core.hello_drone()
