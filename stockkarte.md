# Stockkarte für Bienenstock - Datenfelder

## Grunddatenfelder für die Stockkarte

### 1. Stockidentifikation
- Stocknummer/ID
- Standort des Bienenstocks (z.B. Garten, Feld XY)
- Datum der Erstellung/Inbetriebnahme
- Beutentyp (Dadant, Zander, Langstroth etc.)
- Anzahl Zargen/Honigräume

### 2. Königinneninformationen
- Herkunft der Königin (eigene Nachzucht, gekauft von...)
- Geburtsjahr/Schlupfdatum
- Farbmarkierung (entsprechend der internationalen Farbcodierung)
- Rasse/Genetik
- Einweiseldatum
- Zeichnung vorhanden (ja/nein)
- Geflügelt/ungeflügelt

### 3. Volkscharakteristik
- Volksstärke (Anzahl besetzter Wabengassen)
- Sanftmut (Skala 1-5)
- Schwarmneigung (niedrig/mittel/hoch)
- Wabensitz (ruhig/unruhig)
- Honigertrag (unterdurchschnittlich/durchschnittlich/überdurchschnittlich)

### 4. Inspektionsdaten (regelmäßige Einträge)
- Inspektionsdatum
- Brutstatus (keine Brut/wenig/normal/viel)
- Königin gesichtet (ja/nein)
- Schwarmzellen vorhanden (Anzahl)
- Futtervorrat (gering/ausreichend/gut)
- Durchgeführte Maßnahmen
- Auffälligkeiten

### 5. Behandlungen
- Datum der Behandlung
- Art der Behandlung (Varroabehandlung etc.)
- Verwendetes Mittel
- Dosierung
- Behandlungsdauer
- Wirksamkeitsbeobachtung

### 6. Fütterung
- Datum
- Futterart (Zuckerwasser, Futterteig etc.)
- Menge in kg/l
- Konzentration (bei Flüssigfutter)

### 7. Honigernte
- Erntedatum
- Menge in kg
- Honigsorte/Trachtursprung
- Wassergehalt
- Besonderheiten

### 8. Varroakontrolle
- Kontrolldatum
- Anzahl gefallener Milben
- Messmethode
- Befallsgrad

### 9. Vermehrung/Ableger
- Datum der Bildung von Ablegern
- Methode
- Neue Stock-ID des Ablegers

## Struktur

### Grundaufbau
1. **Hauptblatt "Übersicht"**
   - Eine Zeile pro Bienenstock mit den wichtigsten Grundinformationen
   - Enthält Stocknummer, Standort, aktuelle Königin, Volkscharakteristik

2. **Blatt "Inspektionen"**
   - Spalte A: Stocknummer (als Referenz)
   - Spalte B: Datum
   - Weitere Spalten für alle Inspektionsdaten
   - Jede Inspektion bekommt eine neue Zeile

3. **Blatt "Behandlungen"**
   - Ähnliche Struktur wie Inspektionen
   - Dokumentation aller Behandlungsmaßnahmen

4. **Blatt "Ernte"**
   - Dokumentation aller Ernten mit detaillierten Informationen

### Funktionen

2. **Bedingte Formatierung**
   - Wichtige Werte farblich hervorheben
   - Z.B. rote Markierung bei niedrigem Futtervorrat

3. **Berechnete Felder**
   - Berechnung des Königinnenalters (=HEUTE()-Geburtsdatum)
   - Summierung der Honigernten pro Saison

4. **Filter aktivieren**
   
5. **Datum-Erinnerungen**
   - Bedingte Formatierung für anstehende Behandlungen
   - Formel: =WENN(HEUTE()-[letztes Behandlungsdatum]>30;"Kontrolle fällig";"")
