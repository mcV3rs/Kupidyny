# Kupidyny — CUPID

Repozytorium dla zadania projektowego na przedmiocie Inżynieria Oprogramowania, Wydział Matematyki Stosowanej,
Politechnika Śląska 2022/2023.

## Instrukcja

### Instalacja

Pobranie repozytorium:

```shell
$ git clone https://github.com/mcV3rs/Kupidyny.git
```

Utworzenie wirtualnego środowiska:

```sh
$ cd kupidyny
$ python3 -m venv venv
```

Aktywacja wirtualnego środowiska:

```sh
$ source venv/bin/activate
```

Instalacja wymaganych pakietów z wykorzystaniem pliku _requirements.txt_:

```sh
(venv) $ pip install -r requirements.txt
```

### Inicjalizacja bazy danych

W celu poprawnego działania aplikacji wymagane jest utworzenie bazy danych SQLite oraz dodanie dwóch rekordów

```sh
(venv) $ flask init_db
(venv) $ flask populate_db
```

### Aktywacja aplikacji

Aktywacja serwera aplikacji w trybie deweloperskim:

```sh
(venv) $ flask --app app --debug run
```

Aplikacja będzie dostępna pod adresem http://127.0.0.1:5000.

---

Aktywacja serwera aplikacji w trybie deweloperskim z dostępem z poziomu sieci lokalnej LAN:

```sh
(venv) $ flask --app app --debug run --host 0.0.0.0
```

Aplikacja będzie dostępna pod adresem http://127.0.0.1:5000 oraz http://<lokalny_adres_hosta>:5000

## Użyte pakiety

* **Flask**: mikro-framework do tworzenia aplikacji sieciowych, wraz z następującymi zależnościami:
  * click: pakiet do tworzenia interfejsów wiersza poleceń
  * itsdangerous: kryptograficzne podpisywanie danych
  * Jinja2: silnik szablonów
  * MarkupSafe: zamiana znaczenia znaków w celu zwiększenia bezpieczeństwa danych przekazywanych od użytkownika
  * Werkzeug: zbiór narzędzi do tworzenia aplikacji, która może komunikować się z serwerem WSGI
* **pytest**: framework do testowania projektów w Pythonie
* **Flask-SQLAlchemy** - ORM (Object Relational Mapper) dla Flask
* **Flask-Login** - obsługa zarządzania użytkownikami (logowanie/wylogowanie) w Flask
* **Flask-WTF** - uproszczenie formularzy w Flask
* **flake8** - narzędzie do analizy statycznej
* **pdfkit** - dodatek do narzędzia wkhtmltopdf do konwersji HTML na PDF za pomocą Webkit.

Aplikacja została napisana z wykorzystaniem Pythona 3.10.

## Testy

W celu aktywowania wszystkich testów:

```sh
(venv) $ python -m pytest -v
```

W celu sprawdzenia pokrycia kodu:

```sh
(venv) $ python -m pytest --cov-report term-missing --cov=project
```

## Autorzy

- [Jakub Gurgul](https://gitlab.com/v3rs)
- [Jan Konopka](https://github.com/Jkfre247)
- [Mariusz Pyrk](https://github.com/MariuszPyrk)

## Status projektu

Projekt jest aktualnie w fazie rozwoju.

---
