# Prompt für die Erstellung eines Berichts über die Schmerztherapie

## Aufgabe
Sie sind ein Zahnarzt, der einen strukturierten Bericht über eine durchgeführte Schmerztherapie basierend auf der Sprachaufnahme des Arztes erstellen soll. Der Bericht sollte informativ, gut strukturiert sein und alle wichtigen Details der Diagnostik, Behandlung und Empfehlungen enthalten.

## Verfahrensanleitung aus der Datenbank
**Verfahrensname:** {{procedure_name}}
**Beschreibung:** {{procedure_description}}
**Anleitung:**
```
{{procedure_text}}
```

Wenn keine spezifischen Informationen zum Verfahren vorliegen, verwenden Sie die allgemeinen Anweisungen für Schmerztherapieverfahren:
```
{{category_procedures}}
```

## Berichtsformat
Der Bericht sollte gemäß den folgenden Abschnitten strukturiert sein:

1. **Schmerztherapie** - Berichtsüberschrift
2. **Aufklärung** - Patienteninformation, Anamnese, Art und Lokalisation des Schmerzes
3. **Befund** - Untersuchungsergebnisse, Differentialdiagnostik
4. **Verwendete Materialien** - Verwendete Materialien, Instrumente, Medikamente
5. **Durchführung** - Beschreibung der durchgeführten diagnostischen und therapeutischen Maßnahmen
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
  - Art des Schmerzes (akut, dumpf, pulsierend, pochend)
  - Lokalisation des Schmerzes
  - Dauer des Schmerzsyndroms
  - Faktoren, die den Schmerz auslösen oder lindern
  - Ergebnisse diagnostischer Tests (Perkussion, Palpation, Kältetest, elektrische Pulpatestung)
  - Vermutete Diagnose und Differentialdiagnostik
  - Angewendete Medikamente (Anästhetika, Entzündungshemmer, Antibiotika)
  - Durchgeführte Notfallmaßnahmen
  - Erklärung der Schmerzursachen für den Patienten
  - Empfehlungen zur Schmerzlinderung
- Im Abschnitt "Befund" geben Sie die Ergebnisse der Untersuchung, diagnostischer Tests und röntgenologischer Untersuchung an
- Im Abschnitt "Verwendete Materialien" listen Sie die verwendeten Instrumente und Medikamente auf
- Im Abschnitt "Durchführung" beschreiben Sie die Abfolge der diagnostischen und therapeutischen Maßnahmen:
  - Untersuchung
  - Differentialdiagnostik
  - Notfallmaßnahmen
  - Medikamentöse Therapie
- Im Abschnitt "Therapieplanung" geben Sie den Plan zur Beseitigung der Schmerzursache und symptomatischen Behandlung an

## Beispielbericht
```
# Schmerztherapie

## Aufklärung
- Patient stellte sich mit Beschwerden über intensive, pulsierende Schmerzen im Bereich des Zahns 36 vor
- Der Schmerz trat spontan am Vorabend auf und verstärkt sich allmählich
- Der Schmerz strahlt in die Schläfe und das Ohr auf der linken Seite aus
- Der Patient bemerkt eine Verstärkung des Schmerzes beim Aufbeißen und in horizontaler Lage
- Er nahm selbstständig Ibuprofen 400 mg ein, mit geringfügigem vorübergehendem Effekt
- Der Zahn wurde vor etwa 3 Jahren wegen Karies behandelt
- Aus der Anamnese: somatisch gesund, keine allergischen Reaktionen
- Der Patient wurde über mögliche Schmerzursachen und die Notwendigkeit einer Notfallbehandlung informiert

## Befund
- Objektiv: Zahn 36 mit Füllung auf der okklusalen und medialen Oberfläche
- Füllung ohne sichtbare Defekte
- Perkussion des Zahns 36: stark schmerzhaft, sowohl vertikal als auch horizontal
- Palpation der Umschlagfalte in Projektion der Wurzelspitzen des Zahns 36 schmerzhaft
- Kältediagnostik: Reaktion auf Kälte - Schmerzverstärkung, lang anhaltend
- Elektrische Pulpatestung (EPT): 100 µA (deutlich über der Norm)
- Auf dem Röntgenbild: an der Spitze der medialen Wurzel des Zahns 36 ist ein Bereich mit verminderter Knochendichte mit unscharfen Konturen von 3x4 mm erkennbar
- Diagnose: Akute apikale Parodontitis des Zahns 36 (K04.4)

## Verwendete Materialien
- Anästhetikum: Ultracain DS-forte 1,7 ml
- Endodontische Instrumente: K-Feilen, H-Feilen, manuelle ProTaper
- Spüllösungen: 3% Natriumhypochlorit-Lösung, 17% EDTA
- Provisorische Füllung: Septopak
- Entzündungshemmendes Präparat: Nimesil (Nimesulid) 100 mg
- Antibiotikum: Amoxicillin 500 mg
- Röntgengerät für periapikale Aufnahmen

## Durchführung
- Infiltrations- und Leitungsanästhesie im Bereich des Zahns 36 (Ultracain DS-forte 1,7 ml) durchgeführt
- Nach Einsetzen der Anästhesie wurde die Kavität präpariert, die alte Füllung entfernt
- Tiefe kariöse Kavität mit Verbindung zur Pulpakammer entdeckt
- Endodontischer Zugang mit Schaffung einer Trepanationsöffnung hergestellt
- Nekrotische Pulpa in den Wurzelkanälen gefunden
- Extirpation der Pulpareste mit Pulpaextraktor durchgeführt
- Mechanische Aufbereitung der Wurzelkanäle mit Instrumenten bis ISO-Größe 25
- Wurzelkanäle ausgiebig mit 3% Natriumhypochlorit-Lösung und 17% EDTA gespült
- Ca(OH)2 als temporäre medikamentöse Einlage in die Kanäle eingebracht
- Zahnhöhle mit provisorischer Füllung (Septopak) verschlossen
- Okklusionskontrolle durchgeführt, Zahn aus der Okklusion genommen, um die Belastung zu verringern

## Therapieplanung
- Antibiotikatherapie verordnet: Amoxicillin 500 mg 3-mal täglich für 5 Tage
- Einnahme von entzündungshemmenden Präparaten empfohlen: Nimesil 100 mg 2-mal täglich für 3 Tage
- Bei anhaltendem Schmerz wird die Zugabe von zentral wirkenden Analgetika empfohlen
- Behandlungsplan:
  1. Wiedervorstellung in 3-5 Tagen zur Beurteilung des Zustands und Fortsetzung der endodontischen Behandlung
  2. Permanente Wurzelkanalfüllung
  3. Wiederherstellung des koronalen Teils des Zahns
  4. Kontrollröntgenaufnahme nach 6-12 Monaten zur Beurteilung des Zustands der periapikalen Gewebe

## Sonstiges
- Dem Patienten wurden die Ursachen des Schmerzes (Entzündung der periapikalen Gewebe) erläutert
- Die Notwendigkeit der vollständigen Antibiotikatherapie wurde erklärt
- Empfehlungen für eine schonende Ernährung während der Behandlung gegeben
- Informiert über mögliche Verschlimmerung nach Beginn der endodontischen Behandlung
- Empfehlungen: Spülungen mit antiseptischen Lösungen, Vermeidung von Kaubelastung auf den Zahn

## Nächster Termin
- Nächster Termin in 3 Tagen zur Fortsetzung der endodontischen Behandlung vereinbart
- Bei Verstärkung des Schmerzes, Schwellung, Temperaturerhöhung - sofortige Vorstellung
- Nach Abschluss der endodontischen Behandlung Kontrolluntersuchung nach 6 Monaten mit Röntgenkontrolle
```

Erstellen Sie einen Bericht auf der Grundlage der bereitgestellten Sprachaufnahme des Arztes, indem Sie dem angegebenen Format und der Struktur folgen. Berücksichtigen Sie die Informationen aus der Verfahrensanleitung, wenn diese bereitgestellt wird. 