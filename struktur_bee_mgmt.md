# Bienenstock-Stockkarte WebApp: Architekturkonzept und Entwicklungsplan

## A) Struktur-Konzept der WebApp

### 1. Docker-Umgebung
- **Docker-Container**: Flask/Gunicorn Anwendung
- **Docker-Compose**: Orchestrierung der Container
- **Umgebungsvariablen**: Für Datenbankverbindung und Konfiguration

### 2. Backend-Komponenten
- **Flask-Anwendungsstruktur**:
  ```
  /app
    /templates          # HTML Templates
    /models             # Datenbankmodelle für MongoDB
    /controllers        # Logik für Routen und Datenverarbeitung
    /utils              # Hilfsfunktionen
    __init__.py         # Flask App Initialisierung
    routes.py           # URL-Routing Definitionen
    config.py           # Konfigurationseinstellungen
  ```
- **Gunicorn**: Als WSGI-Server für die Produktionsumgebung


### 3. Datenmodell
- **json-Tabellen**:
  - `hives`: Basisinformationen zu Bienenstöcken
  - `queens`: Informationen zu Königinnen
  - `inspections`: Regelmäßige Kontrollen
  - `treatments`: Behandlungen gegen Krankheiten/Parasiten
  - `feeding`: Fütterungsmaßnahmen
  - `harvests`: Honigernte-Daten
  - `varroa_controls`: Milbenkontrolle
  - `splits`: Informationen zu Ablegern/Vermehrung

### 4. Frontend-Struktur (reines HTML)
- **Seitentypen**:
  - Übersichtsseite: Liste aller Bienenstöcke
  - Detailseite: Informationen zu einem Bienenstock
  - Formulare: Zur Dateneingabe und -bearbeitung
  - Berichtseiten: Zur Anzeige von Auswertungen und Listen

### 5. API-Endpunkte
- **Bienenstock-Management**:
  - `GET /`: Startseite mit Übersicht
  - `GET /hives`: Liste aller Bienenstöcke
  - `GET /hives/<hive_id>`: Detailansicht eines Bienenstocks
  - `GET /hives/new`: Formular für neuen Bienenstock
  - `POST /hives/create`: Speichern eines neuen Bienenstocks
  - `GET /hives/<hive_id>/edit`: Bearbeitungsformular
  - `POST /hives/<hive_id>/update`: Aktualisieren eines Bienenstocks
  - `POST /hives/<hive_id>/delete`: Löschen eines Bienenstocks

- **Datenkategorien** (jeweils für inspections, treatments, feeding, etc.):
  - `GET /hives/<hive_id>/<category>`: Liste aller Einträge einer Kategorie
  - `GET /hives/<hive_id>/<category>/new`: Eingabeformular
  - `POST /hives/<hive_id>/<category>/create`: Speichern eines neuen Eintrags
  - `GET /hives/<hive_id>/<category>/<entry_id>/edit`: Bearbeitungsformular
  - `POST /hives/<hive_id>/<category>/<entry_id>/update`: Aktualisieren eines Eintrags
  - `POST /hives/<hive_id>/<category>/<entry_id>/delete`: Löschen eines Eintrags

- **Berichte**:
  - `GET /reports/harvests`: Ernteübersicht
  - `GET /reports/treatments`: Behandlungsübersicht

### 6. Datenfluss
1. Benutzer interagiert mit HTML-Formularen im Browser
2. HTTP-Anfrage geht an Flask-Server
3. Controller verarbeitet die Anfrage
4. Daten werden in json-Tabellen verwaltet
5. Flask rendert HTML-Template mit den Daten
6. Antwort wird an Browser gesendet

## B) Workflow / Projektablaufplan

### Phase 1: Projektinitialisierung (Woche 1)
1. **Anforderungsanalyse finalisieren**
   - Detaillierte User Stories erstellen
   - Datenmodell definieren
   - Entitäten und Beziehungen dokumentieren

2. **Entwicklungsumgebung einrichten**
   - Python-Umgebung mit Flask installieren
   - json-Tabellen Struktur erstellen
   - Git-Repository initialisieren
   - Docker und Docker-Compose installieren

### Phase 2: Datenbankschema und Backend-Grundlagen (Woche 2)
3. **Datenbank-Design**
   - json-Tabellen definieren
   - Indizes planen

4. **Flask-Basisstruktur erstellen**
   - Projektstruktur anlegen
   - Basiskonfiguration einrichten
   - json-Verbindung implementieren
   - Docker-Containerisierung vorbereiten

### Phase 3: Backend-Funktionalität (Woche 3-4)
5. **Basis-CRUD-Operationen implementieren**
   - Modelle für alle Collections erstellen
   - Controller für grundlegende Operationen entwickeln
   - Routen für Basisoperationen definieren

6. **Geschäftslogik implementieren**
   - Imkerei-spezifische Funktionen entwickeln
   - Validierungslogik erstellen
   - Fehlerbehandlung integrieren

### Phase 4: Frontend-Entwicklung (Woche 5-6)
7. **HTML-Templates erstellen**
   - Basis-Layoutstruktur definieren
   - Übersichtsseiten gestalten
   - Detailseiten für Bienenstöcke entwickeln
   - Formularseiten für alle Datenkategorien erstellen

8. **Formulare und Datenvisualisierung**
   - Formulare für alle CRUD-Operationen einrichten
   - Listenansichten für Daten entwickeln
   - Übersichtsberichte gestalten

### Phase 5: Integration und Testing (Woche 7)
9. **Frontend-Backend-Integration**
   - Templates mit Controller-Logik verbinden
   - Formularverarbeitung implementieren
   - Datenfluss testen

10. **Testphase**
    - Funktionale Tests durchführen
    - Benutzbarkeit überprüfen
    - Edge Cases behandeln

### Phase 6: Containerisierung und Deployment (Woche 8)
11. **Docker-Setup finalisieren**
    - Dockerfile erstellen und testen
    - Docker-Compose-Konfiguration abschließen
    - Umgebungsvariablen für verschiedene Umgebungen einrichten

12. **Deployment vorbereiten**
    - Backup-Strategie entwickeln
    - Logging und Monitoring einrichten

### Phase 7: Dokumentation und Abschluss (Woche 9)
13. **Dokumentation erstellen**
    - Technische Dokumentation schreiben
    - Benutzerhandbuch verfassen
    - API-Referenz erstellen

14. **Projektabschluss**
    - Finale Tests durchführen
    - Code-Review durchführen
    - Deployment durchführen
    - Übergabe an Betrieb

### Hinweise zur Implementierung
- Da JavaScript nicht verwendet werden darf, muss jede Aktion über HTML-Formulare und Seitenneuladen erfolgen
- Für Dropdown-Listen und Auswahlfelder werden HTML-native `<select>` und `<option>` Elemente verwendet
- Datumseingaben erfolgen über HTML5 `<input type="date">`
- Zur Navigation werden einfache Links und Formulare mit Submit-Buttons eingesetzt
- Für Fehlermeldungen werden serverseitig gerenderte HTML-Elemente verwendet

Diese Struktur ermöglicht es einem Entwickler, direkt mit der Implementierung zu beginnen und eine funktionale Bienenstock-Management-Anwendung zu erstellen, die den Anforderungen entspricht.