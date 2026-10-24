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

## Szybki start

Wymagania: Python 3.12+, kompilator C++, Visual Studio Build Tools (Desktop development with C++).

```powershell
git clone <URL_REPOZYTORIUM>
cd SDK_dron

python -m venv .venv
.venv\Scripts\Activate.ps1

pip install cmake pytest
python -m cmake -B build -S .
python -m cmake --build build --config Release
pip install -e .

pytest
```

### Szybki test działania
```powershell
python -c "from wut_control import Drone; d = Drone(); d.hello()"
```