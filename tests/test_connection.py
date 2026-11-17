import pytest
from unittest.mock import MagicMock, patch
from wut_control.communication.DroneConnection import DroneConnection

@patch('wut_control.communication.DroneConnection.Crazyflie')
@patch('wut_control.communication.DroneConnection.cflib.crtp')
def test_scan_for_devices(mock_crtp, mock_cf):
    # Symulacja znalezienia jednego interfejsu radiowego
    mock_crtp.scan_interfaces.return_value = [("radio://0/80/2M", "")]
    
    devices = DroneConnection.scan_for_devices()
    
    assert devices == ["radio://0/80/2M"]
    mock_crtp.init_drivers.assert_called_once()

@patch('wut_control.communication.DroneConnection.Crazyflie')
@patch('wut_control.communication.DroneConnection.cflib.crtp')
def test_connect_and_disconnect(mock_crtp, mock_cf_class):
    mock_cf_instance = mock_cf_class.return_value
    mock_cf_instance.is_link_open.return_value = False

    connection = DroneConnection(uri="radio://0/80/2M")
    
    # Symulacja udanego wywołania callbacku po uruchomieniu open_link
    def mock_open_link(uri):
        connection._on_connected(uri)
        mock_cf_instance.is_link_open.return_value = True

    mock_cf_instance.open_link.side_effect = mock_open_link
    
    connection.connect(timeout=1.0)
    assert connection.is_connected is True
    mock_cf_instance.open_link.assert_called_once_with("radio://0/80/2M")

    # Symulacja rozłączenia i wywołania callbacku
    def mock_close_link():
        connection._on_disconnected(connection.uri)
        mock_cf_instance.is_link_open.return_value = False
        
    mock_cf_instance.close_link.side_effect = mock_close_link
    
    connection.disconnect(timeout=1.0)
    assert connection.is_connected is False
    mock_cf_instance.close_link.assert_called_once()

@patch('wut_control.communication.DroneConnection.Crazyflie')
@patch('wut_control.communication.DroneConnection.cflib.crtp')
def test_connect_timeout(mock_crtp, mock_cf_class):
    mock_cf_instance = mock_cf_class.return_value
    connection = DroneConnection(uri="radio://0/80/2M")
    
    # Zablokowanie wywołania callbacku, co powinno skutkować błędem TimeoutError
    with pytest.raises(TimeoutError):
        connection.connect(timeout=0.1)