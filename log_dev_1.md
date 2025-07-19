 │    6      | Error Handling | `routes.py` (all edit/delete routes) | Was passiert, wenn versucht wird, einen nicht existierenden               │
 │           Datensatz zu bearbeiten oder zu löschen (z.B. über eine manipulierte URL)? | Hoch | Erledigt | Eine URL zum Bearbeiten              │
 │           eines Bienenstocks mit einer ungültigen ID aufrufen (z.B. `/hives/invalid-id/edit`). | Die Anwendung sollte einen                   │
 │           sauberen 404-Fehler (Seite nicht gefunden) anzeigen und nicht abstürzen. | Die Anwendung zeigt wie erwartet "Hive not               │
 │           found" an und stürzt nicht ab. Die Fehlerseite ist jedoch nicht benutzerfreundlich (siehe Issue #1). |                              │
 │    7      | Routing | `routes.py` | Mehrere Blueprints (`inspections_bp`, `treatments_bp`, etc.) werden mit dem `url_prefix='/'`              │
 │           registriert. Dies könnte zu Konflikten führen, wenn Routen in verschiedenen Blueprints identisch sind. | Mittel |                   │
 │           Erledigt | Alle Routen der Anwendung manuell und per Code-Analyse auf mögliche Überschneidungen prüfen. | Jede URL ist              │
 │           einzigartig und führt zur korrekten Funktion. | Die Analyse aller Controller hat gezeigt, dass die Routen gut                       │
 │           strukturiert sind. Durch die Verwendung von kontextbezogenen Pfaden (z.B. `/hives/<hive_id>/inspections/...`) und                   │
 │           spezifischen Entitätsnamen (`/inspections/<id>/...`) gibt es keine Konflikte. |                                                     │
 │    8      | Date Handling | Diverse Model-Dateien | Die Anwendung stürzte ab, wenn in den JSON-Dateien ein ungültiges Datumsformat            │
 │           vorlag. | Hoch | Erledigt | Manuell ein ungültiges Datum in eine der JSON-Dateien eintragen (z.B. `inspections.json`)               │
 │           und die zugehörige Seite laden. | Die Anwendung sollte nicht abstürzen, sondern den fehlerhaften Datensatz ignorieren. |            │
 │           Die `from_dict`-Methoden in allen relevanten Model-Klassen wurden mit `try-except`-Blöcken versehen. Die Anwendung fängt            │
 │           nun ungültige Datumsformate ab und zeigt die Seite korrekt an, ohne abzustürzen. |                                                  │
 │    9    - | Data Management | `data_manager.py` | Der `update`-Vorgang liest und schreibt bei jeder Änderung die gesamte                      │
 │           JSON-Datei. Bei größeren Datenmengen ist dies ineffizient. | Mittel | Analysiert | - | - | Dies ist kein Fehler, sondern            │
 │           eine Beobachtung zur Leistung. Für die aktuelle Größe der App ist es akzeptabel. Für zukünftige Versionen wurde Issue #2            │
 │           erstellt. |                                                                                                                         │
 │    10   - | Usability | `hive_detail.html` | Auf der Detailseite eines Bienenstocks werden viele verschiedene Daten geladen. Dies             │
 │           könnte bei großen Datenmengen zu langen Ladezeiten führen. | Niedrig | Analysiert | Die Ladezeit der `hive_detail`-Seite            │
 │           mit einer großen Anzahl von Inspektionen, Behandlungen etc. beobachten. | Die Seite sollte in einer akzeptablen                     │
 │           Zeitspanne geladen werden. | Die aktuelle Implementierung ist für normale Datenmengen ausreichend. Für zukünftige                   │
 │           Versionen wurde Issue #3 erstellt. |                                                                                                │
 │    9    + | Data Management | `data_manager.py` | Der `update`-Vorgang liest und schreibt bei jeder Änderung die gesamte                      │
 │           JSON-Datei. Bei größeren Datenmengen ist dies ineffizient. | Mittel | Analysiert | - | - | Dies ist kein Fehler, sondern            │
 │           eine Beobachtung zur Leistung. Für die aktuelle Größe der App ist es akzeptabel. Für zukünftige Versionen wurde Issue               │
 │           #23 erstellt. |                                                                                                                     │
 │    10   + | Usability | `hive_detail.html` | Auf der Detailseite eines Bienenstocks werden viele verschiedene Daten geladen. Dies             │
 │           könnte bei großen Datenmengen zu langen Ladezeiten führen. | Niedrig | Analysiert | Die Ladezeit der `hive_detail`-Seite            │
 │           mit einer großen Anzahl von Inspektionen, Behandlungen etc. beobachten. | Die Seite sollte in einer akzeptablen                     │
 │           Zeitspanne geladen werden. | Die aktuelle Implementierung ist für normale Datenmengen ausreichend. Für zukünftige                   │
 │           Versionen wurde Issue #22 erstellt. |                                                                                               │
 │    11                                                                                                                                         │
 │    12     # Zukünftige Verbesserungen / Issues                                                                                                │
 │    13                                                                                                                                         │
 │    14     | ID | Bereich (Area) | Beschreibung (Description) | Priorität (Priority) | Status | Testfall (Test Case) | Erwartetes              │
 │           Ergebnis (Expected Result) | Tatsächliches Ergebnis (Actual Result) |                                                               │
 │    15     | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |                                                                           │
 │    16   - | 1 | Usability / Error Handling | Die Fehlerseiten (z.B. 404 Not Found) sind reiner Text ohne Design oder                          │
 │           Navigationslinks (z.B. "Zurück zur Startseite"). | Niedrig | Erledigt | - | - | - |                                                 │
 │    17   - | 2 | Usability / Navigation | Mehrere Listenansichten für Bienenstock-bezogene Daten (Inspektionen, Fütterungen,                   │
 │           Ernten, Ableger, Behandlungen, Varroakontrollen) enthielten keinen direkten Link zurück zur Detailseite des jeweiligen              │
 │           Bienenstocks. Dies führte zu "Sackgassen" in der Navigation. | Mittel | Erledigt | Alle betroffenen Listen-Templates                │
 │           wurden mit einem "Zurück zum Bienenstock"-Link versehen. | Die Links sind vorhanden und funktionieren korrekt. |                    │
 │    16   + | 1 | Usability / Error Handling | Die Fehlerseiten (z.B. 404 Not Found) sind reiner Text ohne Design oder                          │
 │           Navigationslinks (z.B. "Zurück zur Startseite"). | Niedrig | Erledigt | Eine nicht existierende URL aufrufen. | Die                 │
 │           Anwendung sollte eine ansprechend gestaltete 404-Seite mit Navigationsmöglichkeit anzeigen. | Die 404-Seite erbt nun von            │
 │           `base.html` und enthält einen "Zurück zur Startseite"-Link. Funktioniert fehlerfrei. |                                              │
 │    17   + | 2 | Usability / Navigation | Mehrere Listenansichten für Bienenstock-bezogene Daten (Inspektionen, Fütterungen,                   │
 │           Ernten, Ableger, Behandlungen, Varroakontrollen) enthielten keinen direkten Link zurück zur Detailseite des jeweiligen              │
 │           Bienenstocks. Dies führte zu "Sackgassen" in der Navigation. | Mittel | Erledigt | Alle betroffenen Listen-Templates                │
 │           wurden mit einem "Zurück zum Bienenstock"-Link versehen. | Die Links sind vorhanden und funktionieren korrekt. | Alle               │
 │           Listen-Templates wurden aktualisiert und enthalten nun einen "Zurück zum Bienenstock"-Link. Die Navigation ist                      │
 │           verbessert. |                                                                                                                       │
 │    18     | 3 | Missing Template | Die Vorlage `new_split.html` fehlt, was zu einem `TemplateNotFound`-Fehler führt, wenn versucht            │
 │           wird, einen neuen Ableger hinzuzufügen. | Hoch | Erledigt | Navigieren Sie zu `/hives/<hive_id>/splits/new`. | Die Seite            │
 │           sollte ohne Fehler geladen werden und das Formular zum Hinzufügen eines neuen Ablegers anzeigen. | Die Seite                        │
 │           `new_split.html` wird jetzt ohne Fehler geladen und das Formular wird angezeigt. |                                                  │
 │    19     | 4 | Missing Template | Die Vorlage `edit_split.html` fehlt, was zu einem `TemplateNotFound`-Fehler führt, wenn                    │
 │           versucht wird, einen Ableger zu bearbeiten. | Hoch | Erledigt | Navigieren Sie zu                                                   │
 │           `/hives/<hive_id>/splits/<split_id>/edit`. | Die Seite sollte ohne Fehler geladen werden und das Formular zum Bearbeiten            │
 │           eines Ablegers anzeigen. | Die Seite `edit_split.html` wird jetzt ohne Fehler geladen und das Formular wird angezeigt. |            │
 │    20     | 5 | BuildError / Navigation | Der "Edit"-Link in der Ableger-Liste (`splits_list.html`) führt zu einem `BuildError`               │
 │           beim Klicken. | Hoch | Erledigt | Klicken Sie auf einen "Edit"-Link in der Ableger-Liste. | Die Bearbeitungsseite sollte            │
 │           geladen werden. | Die Bearbeitungsseite wird jetzt ohne Fehler geladen. |                                                           │
 │    24     | 9 | BuildError / Navigation | Der "Add New Varroa Control Record"-Link in der Varroakontrollen-Liste                              │
 │           (`varroa_controls_list.html`) führt zu einem `BuildError` beim Klicken. | Hoch | Erledigt | Klicken Sie auf den "Add New            │
 │           Varroa Control Record"-Link in der Varroakontrollen-Liste. | Die Seite zum Hinzufügen eines neuen Varroakontrolleintrags            │
 │           sollte geladen werden. | Das Formular zur Eingabe des Ergebnisses einer Varroa-Kontrolle wird angezeigt. Der Eintrag                │
 │           wird erfolgreich hinzugefügt und die Liste wird aktualisiert. |                                                                     │
 │    25     | 10 | BuildError / Navigation | Der "Edit"-Link in der Varroakontrollen-Liste (`varroa_controls_list.html`) führt zu               │
 │           einem `BuildError` beim Klicken. | Hoch | Erledigt | Klicken Sie auf einen "Edit"-Link in der Varroakontrollen-Liste. |             │
 │           Die Bearbeitungsseite sollte geladen werden. | Die Bearbeitungsseite wird geladen. Der Eintrag wird erfolgreich                     │
 │           aktualisiert und die Liste wird aktualisiert. |                                                                                     │
 │    26     | 11 | BuildError / Navigation | Der "Delete"-Link in der Varroakontrollen-Liste (`varroa_controls_list.html`) führt zu             │
 │           einem `BuildError` beim Klicken. | Hoch | Erledigt | Klicken Sie auf einen "Delete"-Link in der Varroakontrollen-Liste.             │
 │           | Der Eintrag sollte gelöscht werden. | Der Eintrag wird gelöscht und die Liste wird aktualisiert. |                                │
 │    27   - | 12 | BuildError / Navigation | Die Links "Bearbeiten" und "Löschen" auf der Ableger-Liste (`splits_list.html`) und der            │
 │           Bienenstock-Detailseite (`hive_detail.html`) führen zu einem `BuildError`, da der `main.`-Präfix im `url_for`-Aufruf                │
 │           fehlt. | Hoch | In Bearbeitung | Klicken Sie auf "Bearbeiten" oder "Löschen" auf der Ableger-Liste oder der                         │
 │           Bienenstock-Detailseite. | Die Links sollten korrekt zur Bearbeitungs- bzw. Löschseite navigieren. | TBD |                          │
 │    28   - | 13 | Refactoring / Quality | Eine zentrale `base.html` muss erstellt oder finalisiert werden. Alle anderen Templates              │
 │           müssen von dieser erben, um das Layout zu standardisieren. | Hoch | Offen | Code-Review aller Templates. | Alle                     │
 │           `*.html`-Dateien in `templates/` verwenden `{% extends 'base.html' %}`. | TBD |                                                     │
 │    29   - | 14 | Refactoring / Quality | Ein Makro zum Rendern von Bienenstock-Karten muss erstellt werden, um Code-Duplizierung              │
 │           zu vermeiden. | Mittel | Offen | Code-Review von `index.html` und anderen potenziellen Übersichtsseiten. | Die                      │
 │           Darstellung einer Bienenstock-Karte ist in ein Makro ausgelagert und wird bei Bedarf aufgerufen. | TBD |                            │
 │    30   - | 15 | Refactoring / Quality | Ein Makro zum Rendern von Ereignis-Karten im Chronik-Feed muss erstellt werden. | Mittel             │
 │           | Offen | Code-Review von `hive_detail.html`. | Die Darstellung eines einzelnen Ereignisses (Kontrolle, Fütterung etc.)             │
 │           ist in ein Makro ausgelagert. | TBD |                                                                                               │
 │    31   - | 16 | UX/UI | Die Detailseite (`hive_detail.html`) benötigt einen prominenten Header für die Stammdaten des Volkes. |              │
 │           Mittel | Offen | Die Detailseite eines Bienenstocks laden. | Die Stammdaten (Name, Königin, Beute) sind klar und                    │
 │           deutlich im oberen Bereich der Seite sichtbar. | TBD |                                                                              │
 │    32   - | 17 | UX/UI | Auf der Detailseite (`hive_detail.html`) soll eine Button-Leiste für schnelle Aktionen hinzugefügt                   │
 │           werden. | Hoch | Offen | Die Detailseite eines Bienenstocks laden. | Eine Leiste mit Buttons wie "+ Kontrolle", "+                  │
 │           Fütterung" etc. ist sichtbar und verlinkt auf die entsprechenden Formulare. | TBD |                                                 │
 │    33   - | 18 | UX/UI | Die Ereignis-Anzeige auf der Detailseite (`hive_detail.html`) soll von einer Tabelle in einen                        │
 │           chronologischen Feed umgewandelt werden. | Hoch | Offen | Die Detailseite eines Bienenstocks laden. | Alle Ereignisse               │
 │           werden als Feed von "Karten" mit Typ-Icons untereinander angezeigt. | TBD |                                                         │
 │    34   - | 19 | UX/UI | Das Layout der Startseite (`index.html`) soll von einer einfachen Liste in ein Card-Layout umgewandelt               │
 │           werden. | Mittel | Offen | Die Startseite laden. | Jeder Bienenstock wird als eigene "Karteikarte" mit den wichtigsten              │
 │           Stammdaten angezeigt. | TBD |                                                                                                       │
 │    35   - | 20 | UX/UI | Auf den Bienenstock-Karten der Startseite soll eine "Zustands-Ampel" implementiert werden. | Mittel |                │
 │           Offen | Die Startseite laden. | Jede Karte zeigt eine farbliche Markierung (z.B. Grün, Gelb, Rot), die den Zustand des              │
 │           Volkes signalisiert. | TBD |                                                                                                        │
 │    36   - | 21 | UX/UI | Die Formulare sollen moderne Eingabeelemente (z.B. Sterne-Rating, Tags) erhalten, um die Dateneingabe zu             │
 │           vereinfachen. | Niedrig | Offen | Ein beliebiges Formular zur Dateneingabe öffnen (z.B. `new_inspection.html`). |                   │
 │           Anstelle von reinen Textfeldern werden interaktive Elemente zur Bewertung und Auswahl verwendet. | TBD |                            │
 │    37   - | 22 | Performance / Usability | Die `hive_detail`-Seite lädt alle zugehörigen Daten (Inspektionen, Behandlungen etc.)              │
 │           auf einmal. Bei sehr großen Datenmengen sollte eine Paginierung (Seitenumbrüche) implementiert werden, um die Ladezeiten            │
 │           zu verbessern. | Niedrig | Offen | - | - | - |                                                                                      │
 │    38   - | 23 | Performance / Data Management | Der `update`-Vorgang im `data_manager` ist nicht für große Datenmengen optimiert.            │
 │           Er sollte so geändert werden, dass er nur den spezifischen Datensatz aktualisiert, anstatt die gesamte Datei neu zu                 │
 │           schreiben. | Niedrig | Offen | - | - | - |                                                                                          │
 │    27   + | 12 | BuildError / Navigation | Die Links "Bearbeiten" und "Löschen" auf der Ableger-Liste (`splits_list.html`) und der            │
 │           Bienenstock-Detailseite (`hive_detail.html`) führen zu einem `BuildError`, da der `main.`-Präfix im `url_for`-Aufruf                │
 │           fehlt. | Hoch | Erledigt | Klicken Sie auf "Bearbeiten" oder "Löschen" auf der Ableger-Liste oder der                               │
 │           Bienenstock-Detailseite. | Die Links sollten korrekt zur Bearbeitungs- bzw. Löschseite navigieren. | Die                            │
 │           `url_for`-Aufrufe wurden korrigiert und die Links funktionieren nun wie erwartet. |                                                 │
 │    28   + | 13 | Refactoring / Quality | Eine zentrale `base.html` muss erstellt oder finalisiert werden. Alle anderen Templates              │
 │           müssen von dieser erben, um das Layout zu standardisieren. | Hoch | Erledigt | Code-Review aller Templates. | Alle                  │
 │           `*.html`-Dateien in `templates/` verwenden `{% extends 'base.html' %}`. | `base.html` wurde erstellt und alle relevanten            │
 │           Templates wurden angepasst, um davon zu erben. Das Layout ist nun standardisiert. |                                                 │
 │    29   + | 14 | Refactoring / Quality | Ein Makro zum Rendern von Bienenstock-Karten muss erstellt werden, um Code-Duplizierung              │
 │           zu vermeiden. | Mittel | Erledigt | Code-Review von `index.html` und anderen potenziellen Übersichtsseiten. | Die                   │
 │           Darstellung einer Bienenstock-Karte ist in ein Makro ausgelagert und wird bei Bedarf aufgerufen. | Das                              │
 │           `render_hive_card`-Makro wurde erstellt und wird in `index.html` verwendet. |                                                       │
 │    30   + | 15 | Refactoring / Quality | Ein Makro zum Rendern von Ereignis-Karten im Chronik-Feed muss erstellt werden. | Mittel             │
 │           | Erledigt | Code-Review von `hive_detail.html`. | Die Darstellung eines einzelnen Ereignisses (Kontrolle, Fütterung                │
 │           etc.) ist in ein Makro ausgelagert. | Das `render_timeline_event`-Makro wurde erstellt und wird in `hive_detail.html`               │
 │           verwendet. |                                                                                                                        │
 │    31   + | 16 | UX/UI | Die Detailseite (`hive_detail.html`) benötigt einen prominenten Header für die Stammdaten des Volkes. |              │
 │           Mittel | Erledigt | Die Detailseite eines Bienenstocks laden. | Die Stammdaten (Name, Königin, Beute) sind klar und                 │
 │           deutlich im oberen Bereich der Seite sichtbar. | Ein prominenter Header-Bereich für Stammdaten wurde in                             │
 │           `hive_detail.html` implementiert. |                                                                                                 │
 │    32   + | 17 | UX/UI | Auf der Detailseite (`hive_detail.html`) soll eine Button-Leiste für schnelle Aktionen hinzugefügt                   │
 │           werden. | Hoch | Erledigt | Die Detailseite eines Bienenstocks laden. | Eine Leiste mit Buttons wie "+ Kontrolle", "+               │
 │           Fütterung" etc. ist sichtbar und verlinkt auf die entsprechenden Formulare. | Eine Aktionsleiste mit Buttons für                    │
 │           schnelle Aktionen wurde in `hive_detail.html` hinzugefügt. |                                                                        │
 │    33   + | 18 | UX/UI | Die Ereignis-Anzeige auf der Detailseite (`hive_detail.html`) soll von einer Tabelle in einen                        │
 │           chronologischen Feed umgewandelt werden. | Hoch | Erledigt | Die Detailseite eines Bienenstocks laden. | Alle Ereignisse            │
 │           werden als Feed von "Karten" mit Typ-Icons untereinander angezeigt. | Die Ereignis-Anzeige wurde in einen                           │
 │           chronologischen Feed umgewandelt, der das `render_timeline_event`-Makro verwendet. |                                                │
 │    34   + | 19 | UX/UI | Das Layout der Startseite (`index.html`) soll von einer einfachen Liste in ein Card-Layout umgewandelt               │
 │           werden. | Mittel | Erledigt | Die Startseite laden. | Jeder Bienenstock wird als eigene "Karteikarte" mit den                       │
 │           wichtigsten Stammdaten angezeigt. | Das Layout der Startseite wurde in ein Card-Layout umgewandelt, das das                         │
 │           `render_hive_card`-Makro verwendet. |                                                                                               │
 │    35   + | 20 | UX/UI | Auf den Bienenstock-Karten der Startseite soll eine "Zustands-Ampel" implementiert werden. | Mittel |                │
 │           Offen | Die Startseite laden. | Jede Karte zeigt eine farbliche Markierung (z.B. Grün, Gelb, Rot), die den Zustand des              │
 │           Volkes signalisiert. | Ein Platzhalter für die Zustands-Ampel ist vorhanden. Die Logik zur Bestimmung des Zustands muss             │
 │           noch implementiert werden. |                                                                                                        │
 │    36   + | 21 | UX/UI | Die Formulare sollen moderne Eingabeelemente (z.B. Sterne-Rating, Tags) erhalten, um die Dateneingabe zu             │
 │           vereinfachen. | Niedrig | Offen | Ein beliebiges Formular zur Dateneingabe öffnen (z.B. `new_inspection.html`). |                   │
 │           Anstelle von reinen Textfeldern werden interaktive Elemente zur Bewertung und Auswahl verwendet. | Die Formulare wurden             │
 │           mit Bootstrap-Klassen optisch verbessert. Moderne Eingabeelemente erfordern JavaScript und sind noch nicht                          │
 │           implementiert. |                                                                                                                    │
 │    37   + | 22 | Performance / Usability | Die `hive_detail`-Seite lädt alle zugehörigen Daten (Inspektionen, Behandlungen etc.)              │
 │           auf einmal. Bei sehr großen Datenmengen sollte eine Paginierung (Seitenumbrüche) implementiert werden, um die Ladezeiten            │
 │           zu verbessern. | Niedrig | Offen | - | - | Dies ist eine zukünftige Performance-Optimierung für große Datenmengen. |                │
 │    38   + | 23 | Performance / Data Management | Der `update`-Vorgang im `data_manager` ist nicht für große Datenmengen optimiert.            │
 │           Er sollte so geändert werden, dass er nur den spezifischen Datensatz aktualisiert, anstatt die gesamte Datei neu zu                 │
 │           schreiben. | Niedrig | Offen | - | - | Dies ist eine zukünftige Backend-Performance-Optimierung. |    