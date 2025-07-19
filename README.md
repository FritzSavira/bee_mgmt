# BeeManagement - Digital Beekeeping Management

BeeManagement is a web application for managing bee colonies. The application enables beekeepers to digitally record and manage their hives, queens, inspections, treatments, and much more.

## Features

- **Hive management**: Record and monitor all your hives with detailed information on location, hive type, and colony strength
- **Queen management**: Document queens with information on origin, date of birth, and characteristics
- **Inspection log**: Keep records of regular checks on your colonies
- **Treatment management**: Log treatments for diseases and parasites
- **Feeding management**: Document the feeding of your bee colonies
- **Honey harvest management**: Record the harvest quantity and quality of your honey production
- **Varroa control**: Monitor and log Varroa treatments
- **Colony formation**: Document the reproduction of your bee colonies
- **Automatic reminders**: Receive notifications about overdue inspections and treatments

## Technology stack

- **Backend**: Python with Flask framework
- **Data storage**: JSON files for easy data management without a database server
- **Deployment**: Docker & Docker Compose for easy installation and operation
- **Web server**: Gunicorn for robust production deployment

## Installation

### Prerequisites
- Docker and Docker Compose installed
- Git (optional, for source code download)

### Local installation with Docker

1. Clone repository (or download as ZIP):
```
git clone https://github.com/FritzSavira/bee_mgmt.git
cd bee_mgmt
```

2. Start Docker container:
```
docker-compose up -d
```

3. The application is now accessible at [http://localhost:5000](http://localhost:5000).

### Manual installation (without Docker)

1. Clone the repository:
```
  git clone https://github.com/FritzSavira/bee_mgmt.git
  cd bee_mgmt
  ```

2. Create and activate virtual environment:
```
  python -m venv venv
  # On Windows:
  venv\Scripts\activate
  # On Linux/Mac:
  source venv/bin/activate
  ```

3. Install dependencies:
```
  pip install -r requirements.txt
  ```

4. Start the Flask application:
   ```
   python -m flask run
   ```

5. The application is now accessible at [http://localhost:5000](http://localhost:5000).

## Data structure

The application stores data in JSON files in the `/data` directory:
- `hives.json`: Beehive information
- `queens.json`: Queen information
- `inspections.json`: Inspection logs
- `treatments.json`: Treatment records
- `feeding.json`: Feeding records
- `harvests.json`: harvest records
- `varroa_controls.json`: varroa control records
- `splits.json`: split records

## Contributing to the project

Contributions to the project are welcome! Please fork the project, make your changes, and submit a pull request.

## License

This project is licensed under the MIT license. For more information, see the `LICENSE` file.

## Contact

If you have any questions or suggestions, please create an issue on GitHub or contact the project maintainer directly.

Translated with DeepL.com (free version)





# BeeManagement - Digitale Imkerei-Verwaltung

BeeManagement ist eine Webanwendung zur Verwaltung von Bienenbeständen. Die Anwendung ermöglicht Imkern, ihre Bienenstöcke, Königinnen, Inspektionen, Behandlungen und vieles mehr digital zu erfassen und zu verwalten.

## Funktionen

- **Bienenstockverwaltung**: Erfassung und Überwachung aller Ihrer Bienenstöcke mit detaillierten Informationen zu Standort, Beutentyp und Stärke der Kolonie
- **Königinnenverwaltung**: Dokumentation von Königinnen mit Informationen zu Herkunft, Geburtsdatum und Eigenschaften
- **Inspektionsprotokoll**: Führen Sie Aufzeichnungen über regelmäßige Kontrollen Ihrer Völker
- **Behandlungsverwaltung**: Protokollieren Sie Behandlungen gegen Krankheiten und Parasiten
- **Fütterungsverwaltung**: Dokumentieren Sie die Fütterung Ihrer Bienenvölker
- **Honigernteverwaltung**: Erfassen Sie Erntemenge und -qualität Ihrer Honigproduktion
- **Varroakontrolle**: Überwachung und Protokollierung von Varroa-Behandlungen
- **Ablegerbildung**: Dokumentation der Vermehrung Ihrer Bienenvölker
- **Automatische Erinnerungen**: Erhalten Sie Benachrichtigungen über überfällige Inspektionen und Behandlungen

## Technologiestack

- **Backend**: Python mit Flask-Framework
- **Datenspeicherung**: JSON-Dateien für einfache Datenhaltung ohne Datenbankserver
- **Deployment**: Docker & Docker Compose für einfache Installation und Betrieb
- **Web-Server**: Gunicorn für robuste Produktionsbereitstellung

## Installation

### Voraussetzungen
- Docker und Docker Compose installiert
- Git (optional, für Quellcode-Download)

### Lokale Installation mit Docker

1. Repository klonen (oder als ZIP herunterladen):
   ```
   git clone https://github.com/FritzSavira/bee_mgmt.git
   cd bee_mgmt
   ```

2. Docker Container starten:
   ```
   docker-compose up -d
   ```

3. Die Anwendung ist nun unter [http://localhost:5000](http://localhost:5000) erreichbar.

### Manuelle Installation (ohne Docker)

1. Repository klonen:
   ```
   git clone https://github.com/FritzSavira/bee_mgmt.git
   cd bee_mgmt
   ```

2. Virtuelle Umgebung erstellen und aktivieren:
   ```
   python -m venv venv
   # Unter Windows:
   venv\Scripts\activate
   # Unter Linux/Mac:
   source venv/bin/activate
   ```

3. Abhängigkeiten installieren:
   ```
   pip install -r requirements.txt
   ```

4. Flask-Anwendung starten:
   ```
   python -m flask run
   ```

5. Die Anwendung ist nun unter [http://localhost:5000](http://localhost:5000) erreichbar.

## Datenstruktur

Die Anwendung speichert Daten in JSON-Dateien im Verzeichnis `/data`:
- `hives.json`: Bienenstockinformationen
- `queens.json`: Königinneninformationen
- `inspections.json`: Inspektionsprotokolle
- `treatments.json`: Behandlungsaufzeichnungen
- `feeding.json`: Fütterungsaufzeichnungen
- `harvests.json`: Ernteaufzeichnungen
- `varroa_controls.json`: Varroa-Kontrollaufzeichnungen
- `splits.json`: Aufzeichnungen zur Ablegerbildung

## Beitrag zum Projekt

Beiträge zum Projekt sind willkommen! Bitte erstellen Sie einen Fork des Projekts, nehmen Sie Ihre Änderungen vor und reichen Sie einen Pull Request ein.

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. Weitere Informationen finden Sie in der Datei `LICENSE`.

## Kontakt

Bei Fragen oder Anregungen erstellen Sie bitte ein Issue auf GitHub oder kontaktieren Sie den Projektbetreuer direkt.
