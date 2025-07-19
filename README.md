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
