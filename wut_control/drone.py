from . import _core


class Drone:
    """
    Main interface of the wut-control SDK for autonomous drone control.
    Provides flight control, sensor readings, and camera feed access from a single class.
    """

    def __init__(self, uri: str = "radio://0/80/2M"):
        """
        Initializes the drone instance with the given URI.
        Connection is no longer automatic - use connect() explicitly.
        """
        self.uri = uri
        self._is_connected = False

    def connect(self):
        """Establishes a connection with the drone."""
        # TODO: Implement C++ core connection
        self._is_connected = True
        pass

    def disconnect(self):
        """Safely terminates the connection with the drone."""
        # TODO: Implement C++ core disconnection
        self._is_connected = False
        pass

    def is_connected(self) -> bool:
        """Returns the current connection status."""
        return self._is_connected

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

    # --- 3. Silniki i bezpieczeństwo ---

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
        pass

    # --- 4. Wysokość, obrót i zawis ---

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

    def hello(self):
        _core.hello_drone()
