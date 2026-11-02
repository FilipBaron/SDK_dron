from . import _core


class Drone:
    """
    Main interface of the wut-control SDK for autonomous drone control.
    Provides flight control, sensor readings, and camera feed access from a single class.
    """

    def __init__(self, uri: str = "radio://0/80/2M"):
        """
        Establishes a connection with the drone and prepares it for operation.
        Eventually, this will handle communication with the C++ core defined in src/bindings.
        """
        pass

    def health_check(self) -> dict:
        """
        Verifies battery status, connection quality, and sensor readiness before takeoff.
        Returns a dictionary with basic telemetry parameters.
        """
        pass

    def takeoff(self, target_height: float = 0.5):
        """
        Sends the takeoff command and ascends to the specified target height.
        """
        pass

    def land(self):
        """
        Sends the safe landing command.
        """
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
        """
        Returns the current distances measured by the lidars.
        """
        pass

    def get_camera_frame(self):
        """
        Provides the current video frame from the camera stream.
        """
        pass

    def get_estimated_position(self) -> tuple[float, float, float]:
        """
        Returns the estimated position of the drone (X, Y, Z) based on the accelerometer
        or lighthouse system.
        """
        pass

    def hello(self):
        _core.hello_drone()
