import time

from wut_control import Drone


def select_device(devices: list[str]) -> str | None:
    print("\nZnalezione urządzenia:")
    for idx, uri in enumerate(devices, start=1):
        print(f"  [{idx}] {uri}")

    while True:
        choice = input(f"Wybierz numer urządzenia (1-{len(devices)}) lub 'q' aby wyjść: ").strip()
        if choice.lower() == "q":
            return None

        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(devices):
                return devices[index]

        print("Nieprawidłowy wybór. Podaj poprawny numer z listy.")


def main():
    print("Rozpoczęto skanowanie w poszukiwaniu dronów...")
    devices = Drone.scan_for_devices()

    if not devices:
        print("Nie znaleziono żadnych dronów. Upewnij się, że antena i dron są włączone.")
        return

    uri = select_device(devices)
    if not uri:
        print("Anulowano wybór urządzenia.")
        return

    drone = Drone(uri=uri)

    try:
        print(f"\n[1/4] Łączenie z {uri}...")
        drone.connect()
        print(f"Status: {'Połączony' if drone.is_connected() else 'Brak połączenia'}")

        if drone.is_connected():
            drone.hello()
            time.sleep(2)

        print("\n[2/4] Rozłączanie z dronem...")
        drone.disconnect()
        print(f"Status: {'Połączony' if drone.is_connected() else 'Rozłączony'}")
        time.sleep(2)

        print(f"\n[3/4] Ponowne łączenie z {uri}...")
        drone.connect()
        print(f"Status: {'Połączony' if drone.is_connected() else 'Brak połączenia'}")

        if drone.is_connected():
            drone.hello()
            time.sleep(2)

    except Exception as e:
        print(f"Wystąpił błąd podczas pracy drona: {e}")

    finally:
        if drone.is_connected():
            print("\n[4/4] Końcowe rozłączanie z dronem...")
            drone.disconnect()
            print(f"Status: {'Połączony' if drone.is_connected() else 'Rozłączony'}")

    print("Zakończono działanie skryptu.")


if __name__ == "__main__":
    main()