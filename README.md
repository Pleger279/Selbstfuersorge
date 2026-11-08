# Takeaway-Widget

Text für ein KWGT-Widget auf dem Homescreen. Das Widget liest `zeilen.txt`.

## Text aktualisieren

Immer mit dem Skript, nie `zeilen.txt` von Hand schreiben:

```
python3 tools/fit.py "Titel" "1. …" "2. …" "3. …" "Sonnenkind-Satz"
```

Das Skript misst den Text mit der Widget-Schrift (Lora) und hängt als sechsten Teil die
Schriftgrösse an, bei der alles sicher Platz hat. Es schreibt `zeilen.txt` und `takeaway.txt`.
Danach committen und pushen.

## Vorlage neu bauen

`python3 make.py Takeaway.kwgt` erzeugt die KWGT-Vorlage. Nur nötig, wenn sich das Design ändert.

Schrift: Lora (SIL Open Font License), im Ordner `fonts/`.
