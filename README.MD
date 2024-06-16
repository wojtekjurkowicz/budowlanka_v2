# Budowlanka Project

Budowlanka Project jest aplikacją webową stworzoną w Django 5.0.4, która służy do zarządzania realizacjami, wizytami oraz komentarzami. Projekt wykorzystuje Django Admin do zarządzania treściami oraz oferuje eksport danych do formatu PDF.

## Opis aplikacji

Aplikacja składa się z kilku modułów:

### Mainapp

Moduł `mainapp` zawiera modele oraz widoki dotyczące realizacji (`Realization`), wizyt (`Appointment`) oraz komentarzy (`Comment`). Zawiera również szablony HTML oraz formularze do zarządzania tymi treściami.

### Accounts

Moduł `accounts` odpowiada za zarządzanie użytkownikami i autoryzacją w systemie. Umożliwia logowanie, rejestrację oraz zarządzanie kontem użytkownika.

## Moduł Admina

### `admin.py`

Moduł `admin.py` definiuje specjalne klasy admina dla każdego z modeli (`RealizationAdmin`, `AppointmentAdmin`, `CommentAdmin`). Każda z tych klas zawiera funkcjonalność eksportu danych do formatu PDF dzięki wykorzystaniu biblioteki `reportlab`. 

### `apps.py`

Moduł `apps.py` definiuje konfigurację aplikacji Django (`MainappConfig`) i jest używany do rejestrowania aplikacji w `settings.py`.

## Uwagi

Aplikacja jest w pełni skonfigurowana do działania w środowisku deweloperskim. Wymaga dalszej konfiguracji i dostosowania do środowiska produkcyjnego, w tym ustawienia bazy danych, serwera pocztowego oraz zabezpieczeń.

