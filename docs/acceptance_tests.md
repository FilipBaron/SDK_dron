# Testy Akceptacyjne

Testy akceptacyjne polegają na wykonaniu prostych misji przez fizycznego drona w sali 134. Dowodem zaliczenia każdego testu jest załączony materiał wideo.

---

### Misja 1: Lot po wyznaczonych punktach
* **Cel:** Weryfikacja pozycjonowania.
* **Przebieg:** Skrypt ustala współrzędne w przestrzeni sali. Dron startuje, przelatuje kolejno przez zadane punkty, zawisa na końcu trasy i ląduje.
* **Kryterium zaliczenia:** Dron odwiedza wyznaczone punkty w zadanej kolejności.
---

### Misja 2: Unikanie przeszkód z użyciem lidaru
* **Cel:** Weryfikacja czujnikiów odległości i reakcji drona w czasie rzeczywistym.
* **Przebieg:** Dron leci po prostej trasie, na której ustawiona jest przeszkoda. Po wykryciu przeszkody w zadanej odległości algorytm zatrzymuje drona lub wykonuje manewr ominięcia.
* **Kryterium zaliczenia:** Brak kolizji, dron zatrzymuje się lub omija przeszkodę na podstawie danych z lidaru.

---

### Misja 3: Przeszukiwanie sali i detekcja markera z użyciem kamery
* **Cel:** Weryfikacja obrazu z kamery.
* **Przebieg:** Dron przeszukuje wyznaczony obszar sali w celu odnalezienia markera. Po wykryciu markera w kadrze zatrzymuje się przy nim.
* **Kryterium zaliczenia:** Poprawna detekcja markera i reakcja drona.
