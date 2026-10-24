from wut_control import Drone

def test_drone_initialization():
    drone = Drone()
    assert drone is not None

def test_drone_hello_runs():
    drone = Drone()
    drone.hello()