# SDK_dron

## Standard wiadomości commitów

W projekcie stosujemy standard **[Conventional Commits](https://www.conventionalcommits.org/)**. Wszystkie commity są automatycznie weryfikowane przez potok CI.

### Format
```text
typ(moduł_opcjonalny): zwięzły opis zmian w trybie rozkazującym

Przykład: feat(core): add take off command
```

### Dostępne typy

* `feat`: Nowa funkcjonalność (np. `feat(core): add take off command`)
* `fix`: Naprawa błędu (np. `fix(bindings): ...`)
* `docs`: Zmiany w dokumentacji
* `style`: Formatowanie kodu bez wpływu na logikę
* `refactor`: Refaktoryzacja
* `perf`: Optymalizacja wydajności
* `test`: Testy jednostkowe i integracyjne (np. `test(python): ...`)
* `build`: Zmiany w systemie budowania (np. `build(cmake): ...`)
* `ci`: Zmiany w potokach CI/CD (np. `ci: ...`)
* `chore`: Drobne prace porządkowe, .gitignore itp.

### Nazwy gałęzi

Nazwy gałęzi tworzymy analogicznie do typów commitów, stosując małe litery i myślniki:

```text
typ/krótki-opis

Przykłady: chore/setup, feat/drone-preparation
```

## Formatowanie

### Python (Ruff)

1. **Weryfikacja:**
```powershell
ruff check .
ruff format --check .
```

2. **Formatowanie:**
```powershell
ruff check --fix . ; ruff format .
```

### C++ (clang-format & clang-tidy)

1. **Weryfikacja:**
```powershell
git ls-files "include/*.hpp" "src/*.cpp" | ForEach-Object { clang-format --dry-run --Werror $_ }
```

2. **Formatowanie:**
```powershell
git ls-files "include/*.hpp" "src/*.cpp" | ForEach-Object { clang-format -i $_ }
```

3. **Analiza statyczna:**
```powershell
git ls-files "src/*.cpp" ":!src/bindings/*" | ForEach-Object { clang-tidy $_ -- -Iinclude -std=c++17 }
```

## Szybki start

Wymagania: Windows 10/11, Python 3.12-3.13, kompilator C++, Visual Studio Build Tools (Desktop development with C++), vcpkg (`libusb:x64-windows`).

```powershell
git clone <URL_REPOZYTORIUM>
cd SDK_dron

vcpkg install libusb:x64-windows

python -m venv .venv
.venv\Scripts\Activate.ps1

pip install scikit-build-core cmake pybind11 pytest clang-format clang-tidy ruff
pip install -e . --no-build-isolation

pytest
```

### Szybki test działania
```powershell
python -c "from wut_control import Drone; d = Drone(); d.hello()"
```