from unittest.mock import MagicMock

import pytest

from wut_control import Drone, _core


def test_scan_for_devices(monkeypatch):
    fake_device = _core.DroneInfo()
    fake_device.uri = "radio://0/80/2M/E7E7E7E7E7"
    fake_device.channel = 80
    fake_device.address = 0xE7E7E7E7E7

    mock_scanner = MagicMock(spec=_core.IDroneBackend)
    mock_scanner.scan.return_value = [fake_device]
    monkeypatch.setattr(_core, "CrazyflieBackend", lambda: mock_scanner)

    devices = Drone.scan_for_devices(start_channel=0, end_channel=125, address=0xE7E7E7E7E7)

    assert devices == ["radio://0/80/2M/E7E7E7E7E7"]
    mock_scanner.scan.assert_called_once_with(0, 125, 0xE7E7E7E7E7)


def test_connect_and_disconnect():
    mock_backend = MagicMock(spec=_core.IDroneBackend)
    mock_backend.is_connected.side_effect = [False, True, False]

    drone = Drone(uri="radio://0/80/2M/E7E7E7E7E7", backend=mock_backend)
    assert drone.is_connected() is False

    drone.connect(timeout=1.0)
    assert drone.is_connected() is True
    mock_backend.connect.assert_called_once_with("radio://0/80/2M/E7E7E7E7E7")

    drone.disconnect()
    assert drone.is_connected() is False
    mock_backend.disconnect.assert_called_once()


def test_connect_auto_scan_when_no_uri():
    fake_device = _core.DroneInfo()
    fake_device.uri = "radio://0/80/2M/E7E7E7E7E7"

    mock_backend = MagicMock(spec=_core.IDroneBackend)
    mock_backend.scan.return_value = [fake_device]

    drone = Drone(backend=mock_backend)
    drone.connect(timeout=1.0)

    mock_backend.scan.assert_called_once()
    mock_backend.connect.assert_called_once_with("radio://0/80/2M/E7E7E7E7E7")


def test_connect_timeout():
    mock_backend = MagicMock(spec=_core.IDroneBackend)
    mock_backend.connect.side_effect = RuntimeError("Radio link timeout")

    drone = Drone(uri="radio://0/80/2M/E7E7E7E7E7", backend=mock_backend)

    with pytest.raises(TimeoutError):
        drone.connect(timeout=0.25)