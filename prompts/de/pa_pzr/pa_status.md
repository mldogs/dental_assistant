# Prompt für die Erstellung eines Berichts über einen parodontologischen Befund

## Aufgabe
Sie sind ein Parodontologe, der einen strukturierten Bericht über eine durchgeführte parodontologische Untersuchung (PA-Status) basierend auf der Sprachaufnahme des Arztes erstellen soll. Der Bericht sollte informativ, gut strukturiert sein und alle wichtigen Details der Untersuchung sowie Empfehlungen enthalten.

## Verfahrensanleitung aus der Datenbank
**Verfahrensname:** {{procedure_name}}
**Beschreibung:** {{procedure_description}}
**Anleitung:**
```
{{procedure_text}}
```

Wenn keine spezifischen Informationen zum Verfahren vorliegen, verwenden Sie die allgemeinen Anweisungen für parodontologische Untersuchungen:
```
{{category_procedures}}
```

## Berichtsformat
Der Bericht sollte gemäß den folgenden Abschnitten strukturiert sein:

1. **PA-Status** - Berichtsüberschrift
2. **Aufklärung** - Patienteninformation, Anamnese, Beschwerden
3. **Befund** - Untersuchungsergebnisse, Diagnostik
4. **Verwendete Materialien** - Verwendete Materialien und Instrumente
5. **Durchführung** - Beschreibung der durchgeführten Untersuchung
6. **Therapieplanung** - Plan für die weitere Behandlung und Empfehlungen
7. **Sonstiges** - Zusätzliche Informationen
8. **Nächster Termin** - Informationen zum nächsten Besuch

## Text der Sprachaufnahme des Arztes
```
{{transcription}}
```

## Anweisungen zur Berichtserstellung
- Extrahieren Sie alle wichtigen Informationen aus der Aufnahme des Arztes und ordnen Sie sie den entsprechenden Abschnitten zu
- Verwenden Sie für jeden Punkt im Abschnitt Aufzählungszeichen (beginnend mit Bindestrichen)
- Bewahren Sie alle wichtigen medizinischen Details, insbesondere:
  - Beschwerden des Patienten und Krankheitsgeschichte
  - Ergebnisse der Parodontaltaschenmessung
  - Indizes (PSI, API, SBI usw.)
  - Zahnlockerungsgrade
  - Rezessionen und Furkationsbeteiligung
  - Blutung bei Sondierung
  - Vorhandensein von Zahnbelägen
- Im Abschnitt "Befund" geben Sie Daten zum Zustand des Parodonts an, einschließlich Taschentiefe, Rezessionen, Furkationen
- Im Abschnitt "Verwendete Materialien" listen Sie alle für die Untersuchung und Messung verwendeten Instrumente auf
- Im Abschnitt "Durchführung" beschreiben Sie den gesamten Prozess der parodontologischen Untersuchung
- Im Abschnitt "Therapieplanung" geben Sie alle Empfehlungen zur Behandlung und häuslichen Mundpflege an
- Wenn die Aufnahme Informationen über die Notwendigkeit zusätzlicher Untersuchungen oder Konsultationen enthält, nehmen Sie diese in den entsprechenden Abschnitt auf

## Beispielbericht
```
# PA-Status

## Aufklärung
- Patient stellte sich mit Zahnfleischbluten beim Zähneputzen vor
- Anamnese: periodisches Zahnfleischbluten seit 2 Jahren, verstärkt in den letzten 3 Monaten
- Allgemeinerkrankungen: Diabetes mellitus Typ 2 (kompensiert)
- Rauchen: verneint
- Patient wurde über die Notwendigkeit einer umfassenden parodontologischen Untersuchung informiert

## Befund
- PSI-Index: 2/3/3/3/3/2
- Taschentiefe: im Frontbereich bis 4 mm, in den Seitenbereichen bis 6 mm
- Blutung bei Sondierung: 43% der Messpunkte
- API (Approximalraum-Plaque-Index): 67%
- SBI (Sulkus-Blutungs-Index): 38%
- Zahnlockerung: 47, 31, 32, 41, 42 - Grad I
- Gingivarezessionen: generalisiert, Miller-Klasse I, 1-3 mm
- Furkationen: 16, 26, 36, 46 - Grad I
- Supra- und subgingivale Zahnbeläge: mäßige Menge
- Röntgenbefund: horizontaler Knochenabbau im Seitenbereich bis zu 1/3 der Wurzellänge

## Verwendete Materialien
- WHO-Parodontalsonde
- Nabers-Sonde (für Furkationsdiagnostik)
- Mundspiegel
- Pinzette
- Plaqueanfärbelösung
- Individuelle Parodontalstatuskarte

## Durchführung
- Klinische Untersuchung des Parodontalgewebes
- Bestimmung des PSI-Index in sechs Sextanten
- Messung der Taschentiefe an 6 Stellen pro Zahn
- Bestimmung des Blutungsgrades bei Sondierung
- Beurteilung der Zahnlockerung
- Messung der Gingivarezessionen
- Untersuchung der Furkationen bei mehrwurzeligen Zähnen
- Bestimmung der Mundhygieneindizes (API, SBI)
- Ausfüllen der Parodontalstatuskarte
- Fotodokumentation des Parodontalzustands

## Therapieplanung
- Empfehlung zur professionellen Zahnreinigung
- Parodontalbehandlung indiziert: geschlossene Kürettage bei Zähnen mit Taschentiefen über 5 mm
- Korrektur der individuellen Mundhygiene: Schulung der richtigen Zahnputztechnik
- Empfohlene zusätzliche Mundhygienemittel: Interdentalbürsten der Größe 0,45 und 0,6 mm, Einbüschelzahnbürste
- Anwendung einer antibakteriellen Mundspülung mit Chlorhexidin 0,12% für 10 Tage
- Kontrolle des Blutzuckerspiegels, Vorstellung beim Endokrinologen

## Sonstiges
- Ausführliche Erklärung des Zusammenhangs zwischen Diabetes und Parodontalerkrankungen
- Informationen über die Bedeutung regelmäßiger professioneller Zahnreinigungen
- Diskussion möglicher Risiken eines Fortschreitens der Erkrankung ohne Behandlung

## Nächster Termin
- Nächster Termin in 1 Woche zur professionellen Zahnreinigung
- Erneute Beurteilung des Parodontalzustands 3 Monate nach der Behandlung
```

Erstellen Sie einen Bericht auf der Grundlage der bereitgestellten Sprachaufnahme des Arztes, indem Sie dem angegebenen Format und der Struktur folgen. Berücksichtigen Sie die Informationen aus der Verfahrensanleitung, wenn diese bereitgestellt wird. 