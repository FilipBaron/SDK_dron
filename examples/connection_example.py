import time

from wut_control import Drone


def main():
    print("Rozpoczęto skanowanie w poszukiwaniu dronów...")
    devices = Drone.scan_for_devices()

    if not devices:
        print("Nie znaleziono żadnych dronów. Upewnij się, że antena i dron są włączone.")
        return

    uri = devices[0]
    print(f"Znaleziono drona: {uri}. Inicjalizacja połączenia...")

    try:
        with Drone(uri=uri) as drone:
            print(
                f"Status połączenia: {'Połączony' if drone.is_connected() else 'Brak połączenia'}"
            )

            if drone.is_connected():
                print("Dron gotowy do pracy. Wykonywanie testu (oczekiwanie 3 sekundy)...")
                drone.hello()
                time.sleep(3)

    except Exception as e:
        print(f"Wystąpił błąd podczas pracy drona: {e}")

    print("Zakończono działanie skryptu. Połączenie zostało bezpiecznie przerwane.")


if __name__ == "__main__":
    main()
