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

### 4.1 UX/UI-Design: Adaption der traditionellen Stockkarte

#### Analyse des traditionellen Layouts

Die physische Stockkarte ist das zentrale, über Jahrzehnte optimierte Werkzeug des Imkers. Ihre digitale Adaption muss den etablierten, mentalen Workflow respektieren, um eine hohe Akzeptanz zu gewährleisten. Gängige Stockkarten kombinieren zwei Elemente:

1.  **Kopfbereich (Stammdaten):** Statische Informationen zum Bienenvolk.
    *   **Identifikation:** Stock-Nummer, Name, Standort.
    *   **Königin:** Alter, Farbe, Herkunft.
    *   **Beute:** Typ des Bienenstocks (z.B. Dadant, Zander).

2.  **Chronik (Logbuch):** Eine Tabelle, in der jede Zeile eine Kontrolle darstellt.
    *   **Spalten:** Datum, Wetter, Volksstärke, Brutbild, Sanftmut, Futtervorrat, Krankheitszeichen, durchgeführte Maßnahmen.

#### Konzept für die WebApp

Das Design der WebApp überführt diese bewährte Struktur in ein modernes, interaktives Interface. Das Ziel ist nicht, die Stockkarte zu ersetzen, sondern sie zu verbessern: schnellere Dateneingabe, bessere Lesbarkeit und automatisierte Auswertungen.

-   **Dashboard-Ansicht (`index.html`):**
    -   Stellt eine Übersicht aller Bienenstöcke dar, ähnlich einer Kartei-Box.
    -   Jeder Bienenstock wird als "Karteikarte" (Card-Element) visualisiert.
    -   Die Karte zeigt die wichtigsten Stammdaten (Stock-Nummer, Name, Status der Königin) und eine "Ampel" für den Zustand (z.B. Grün = alles ok, Gelb = Kontrolle empfohlen, Rot = Problem erkannt).
    -   Ein prominenter Button "Neuer Bienenstock" ist jederzeit sichtbar.

-   **Detailansicht (`hive_detail.html`): Die digitale Stockkarte**
    -   **Header:** Der Kopfbereich der traditionellen Stockkarte wird prominent und klar strukturiert dargestellt. Ein "Bearbeiten"-Button ermöglicht die Änderung der Stammdaten.
    -   **Aktionsleiste:** Eine Button-Leiste für die häufigsten Aktionen ersetzt das manuelle Eintragen in eine "Maßnahmen"-Spalte. Jeder Button führt direkt zu einem dedizierten Formular:
        -   `+ Kontrolle`
        -   `+ Fütterung`
        -   `+ Behandlung`
        -   `+ Ernte`
        -   `+ Varroakontrolle`
        -   `+ Ableger`
    -   **Chronik-Feed:** Anstelle einer starren Tabelle werden alle Ereignisse (Kontrollen, Fütterungen, Behandlungen etc.) in einer einheitlichen, chronologischen Liste (ähnlich einem Social-Media-Feed) angezeigt.
        -   Jeder Eintrag ist eine "Karte" mit einem Icon, das den Typ des Eintrags visualisiert (z.B. ein Auge für Kontrolle, eine Spritze für Behandlung).
        -   Dies verbessert die Lesbarkeit und erlaubt, schnell durch die Historie zu scrollen.
        -   Filter-Optionen (z.B. "Zeige nur Behandlungen") ermöglichen eine schnelle Analyse.

-   **Formulare (`new_*.html`, `edit_*.html`): Intelligente Dateneingabe**
    -   **Reduktion von Tipparbeit:** Wo immer möglich, werden Freitextfelder durch schnell klickbare Optionen ersetzt.
        -   **Bewertungen (Völkerstärke, Sanftmut):** Verwendung von Sterne-Ratings oder Schiebereglern anstelle von Text.
        -   **Beobachtungen (Brutbild, Königin):** Verwendung von Tags oder Checkboxen (z.B. `[x] stifftet`, `[ ] weiselrichtig`, `[x] Königin gesehen`).
    -   **Kontextbezogene Eingaben:** Das Datum ist immer mit dem heutigen Tag vorausgefüllt.
    -   **Klare Handlungsaufforderungen:** Jeder Formular-Submit-Button ist klar beschriftet (z.B. "Kontrolle speichern", "Behandlung hinzufügen").

#### Guideline zur Standardisierung des Frontends

Um eine hohe Code-Qualität, Konsistenz und Wartbarkeit zu gewährleisten, sind die folgenden Jinja2-Praktiken verbindlich für die Entwicklung:

1.  **Template-Vererbung (`base.html`):**
    *   Alle Templates MÜSSEN von einer zentralen `base.html` erben.
    *   Die `base.html` definiert das Grundlayout, die Navigation, den Footer und inkludiert die globalen CSS- und (falls zukünftig vorhanden) JS-Dateien.
    *   Inhaltsspezifische Seiten füllen ausschließlich vordefinierte Blöcke (z.B. `{% block content %}`).

2.  **Makros für wiederverwendbare Komponenten:**
    *   Für alle sich wiederholenden, logischen UI-Elemente MÜSSEN Makros erstellt werden.
    *   Dies gilt insbesondere für:
        -   Die "Bienenstock-Karte" auf der Übersichtsseite.
        -   Einen einzelnen Eintrag im "Chronik-Feed" der Detailseite.
        -   Standardisierte Formularfelder (Label, Input, Fehlermeldung).
    *   Makros sind in einer separaten Datei zu organisieren (z.B. `_macros.html`) und bei Bedarf zu importieren.

3.  **Includes für statische Sektionen:**
    *   Komplexe, aber statische HTML-Abschnitte, die auf mehreren Seiten wiederverwendet werden (z.B. eine Aktionsleiste), SOLLTEN in separate Partial-Dateien (z.B. `_action_bar.html`) ausgelagert und mit `{% include %}` eingebunden werden.

### 4.2 Sprachen

Um die Anwendung mehrsprachig zu gestalten und die Auswahl der Sprache über die Navbar zu ermöglichen, wird die Flask-Erweiterung `Flask-Babel` verwendet.

#### Konzept: Internationalisierung (i18n) und Lokalisierung (l10n) mit Flask-Babel

Das Ziel ist, alle im Browserfenster angezeigten Texte durch sprachspezifische Versionen zu ersetzen.

#### Guideline zur Implementierung:

1.  **Installation und Konfiguration:**
    *   `Flask-Babel` muss in `requirements.txt` hinzugefügt und installiert werden.
    *   Die Initialisierung und Konfiguration von Babel erfolgt in `app/__init__.py`. Dies beinhaltet die Definition der unterstützten Sprachen (z.B. `['de', 'en']`) und eine Funktion zur Ermittlung der aktuellen Sprache (z.B. über Session oder URL-Parameter).

2.  **Textmarkierung in HTML-Templates:**
    *   Alle Texte in den HTML-Dateien (`app/templates/*.html`), die übersetzt werden sollen, MÜSSEN mit der Jinja2-Syntax `{{ _('Text zum Übersetzen') }}` oder `{{ gettext('Text zum Übersetzen') }}` markiert werden.

3.  **Textextraktion:**
    *   Das Babel-CLI-Tool wird verwendet, um alle markierten Texte aus den Templates zu extrahieren. Das Ergebnis ist eine `.pot`-Datei (Portable Object Template), die als Vorlage für alle Übersetzungen dient.

4.  **Übersetzungsdateien (.po) erstellen:**
    *   Für jede unterstützte Sprache (z.B. Deutsch, Englisch) wird aus der `.pot`-Datei eine eigene `.po`-Datei (Portable Object) generiert. Diese Dateien werden im Format `[Sprachcode]/LC_MESSAGES/messages.po` (z.B. `de/LC_MESSAGES/messages.po`) gespeichert.
    *   In den `.po`-Dateien werden die Übersetzungen für jeden Originaltext manuell eingetragen.

5.  **Übersetzungen kompilieren:**
    *   Die `.po`-Dateien MÜSSEN in `.mo`-Dateien (Machine Object) kompiliert werden. Diese kompilierten Dateien werden von Flask-Babel zur Laufzeit effizient geladen, um die Übersetzungen bereitzustellen.

6.  **Sprachauswahl in der Navigation:**
    *   In der `base.html` (oder einer anderen geeigneten Navigationskomponente) wird ein Mechanismus zur Sprachauswahl implementiert. Dies kann ein Dropdown-Menü oder eine Liste von Links sein, die es dem Benutzer ermöglichen, die gewünschte Sprache auszuwählen.
    *   Beim Wechsel der Sprache muss die gewählte Sprache in der Benutzersitzung gespeichert werden (z.B. in der Flask-Session oder als Cookie), damit Flask-Babel die korrekte `.mo`-Datei für nachfolgende Anfragen verwenden kann.

Dieser Prozess gewährleistet eine saubere Trennung von Code und Übersetzungen und ermöglicht eine einfache Erweiterung um weitere Sprachen.


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