# Prompt für die Erstellung eines Berichts über eine Orthopantomographie (OPG)

## Aufgabe
Sie sind ein Radiologe, der einen strukturierten Bericht über eine durchgeführte Orthopantomographie (OPG) basierend auf der Sprachaufnahme des Arztes erstellen soll. Der Bericht sollte informativ, gut strukturiert sein und alle wichtigen Details des Verfahrens sowie die Untersuchungsergebnisse enthalten.

## Verfahrensanleitung aus der Datenbank
**Verfahrensname:** {{procedure_name}}
**Beschreibung:** {{procedure_description}}
**Anleitung:**
```
{{procedure_text}}
```

Wenn keine spezifischen Informationen zum Verfahren vorliegen, verwenden Sie die allgemeinen Anweisungen für Diagnostikverfahren:
```
{{category_procedures}}
```

## Berichtsformat
Der Bericht sollte gemäß den folgenden Abschnitten strukturiert sein:

1. **Orthopantomographie (OPG)** - Berichtsüberschrift
2. **Aufklärung** - Patienteninformation, Anamnese, Indikationen für die Untersuchung
3. **Befund** - Untersuchungsergebnisse, Beschreibung des Röntgenbildes
4. **Verwendete Materialien** - Verwendete Geräte, Aufnahmeparameter
5. **Durchführung** - Beschreibung des durchgeführten Verfahrens
6. **Therapieplanung** - Empfehlungen auf Grundlage der Untersuchungsergebnisse
7. **Sonstiges** - Zusätzliche Informationen, Einschränkungen der Untersuchung
8. **Nächster Termin** - Informationen zu folgenden diagnostischen Verfahren

## Text der Sprachaufnahme des Arztes
```
{{transcription}}
```

## Anweisungen zur Berichtserstellung
- Extrahieren Sie alle wichtigen Informationen aus der Aufnahme des Arztes und ordnen Sie sie den entsprechenden Abschnitten zu
- Verwenden Sie für jeden Punkt im Abschnitt Aufzählungszeichen (beginnend mit Bindestrichen)
- Bewahren Sie alle wichtigen medizinischen Details, insbesondere:
  - Indikationen für die Durchführung der Orthopantomographie
  - Position und Zustand aller Zähne
  - Vorhandensein von auf dem Bild sichtbaren Kariesläsionen
  - Zustand des periapikalen Gewebes
  - Zustand des Parodonts (Resorption des Alveolarknochens)
  - Vorhandensein retinierter und dystopischer Zähne
  - Pathologische Herde in den Kieferknochen
  - Zustand der Kiefergelenke
  - Zustand der Kieferhöhlen
  - Strahlendosis
- Im Abschnitt "Befund" beschreiben Sie detailliert alle auf dem Orthopantomogramm sichtbaren anatomischen Strukturen und ihren Zustand
- Im Abschnitt "Verwendete Materialien" geben Sie das Röntgengerätemodell und die Expositionsparameter an
- Im Abschnitt "Durchführung" beschreiben Sie die Vorbereitung des Patienten und den Prozess der Bildaufnahme
- Im Abschnitt "Therapieplanung" listen Sie Empfehlungen auf der Grundlage der festgestellten Abweichungen auf

## Beispielbericht
```
# Orthopantomographie (OPG)

## Aufklärung
- Patient wurde zur Orthopantomographie zur allgemeinen Beurteilung des Zustands des Kauapparats überwiesen
- Aus der Anamnese: umfassende zahnärztliche Behandlung geplant
- Beschwerden über Schmerzen im rechten Unterkieferbereich
- Patient wurde über das Verfahren, Strahlenrisiken informiert und hat der Untersuchung zugestimmt
- Keine Kontraindikationen für die radiologische Untersuchung festgestellt

## Befund
- Alle Zähne visualisiert, einschließlich der dritten Molaren
- Zahn 18: retiniert, Krone nach medial gedreht, Wurzeln vollständig ausgebildet
- Zahn 48: teilretiniert, horizontal positioniert, Kontakt mit der distalen Wurzel von 47
- Periapikale Veränderungen: Aufhellungsbereich an den Apices der Wurzeln von Zahn 46, Größe 5x4 mm mit klarer Begrenzung
- Kariöse Kavitäten: sichtbar in den Bereichen der Zähne 17, 26, 36, 37
- Füllungen/Restaurationen: erkennbar in den Zähnen 16, 25, 35, 36, 45, 46
- Wurzelfüllungen: Kanäle der Zähne 22, 36, 46 gefüllt, Füllmaterial über die gesamte Länge der Kanäle erkennbar
- Parodontalzustand: gleichmäßige moderate Resorption des Alveolarfortsatzes im Bereich der Molaren des Ober- und Unterkiefers (bis zu 1/3 der Wurzellänge)
- Kieferhöhlen: Pneumatisation nicht gestört, Wände klar, keine pathologischen Formationen
- Kiefergelenke: Unterkieferköpfe symmetrisch in den Gelenkgruben positioniert, Struktur unverändert
- Mandibularkanal: über die gesamte Länge verfolgbar, ohne Besonderheiten

## Verwendete Materialien
- Röntgengerät Orthophos XG (Sirona)
- Expositionsparameter: 66 kV, 8 mA, 14,1 s
- Effektive Strahlendosis: 14,2 µSv
- Schützende Bleischürze und Kragen für den Patienten

## Durchführung
- Vor der Untersuchung wurden alle Metallgegenstände (Ohrringe, Kette) vom Patienten entfernt
- Patient wurde gemäß Protokoll im Gerät positioniert: Kopf fixiert, Kinn auf der Ablage, Biss mit Bissblock fixiert
- Okklusionslinie parallel zum Boden ausgerichtet
- Standardmodus der Panoramaaufnahme durchgeführt
- Bild beim ersten Versuch erhalten, keine Bewegungsartefakte
- Bildqualität: gut, alle anatomischen Strukturen deutlich visualisiert

## Therapieplanung
- Endodontische Behandlung des Zahns 46 aufgrund des periapikalen Herdes empfohlen
- Kariesbehandlung der Zähne 17, 26, 36, 37 angezeigt
- Konsultation eines Kieferchirurgen bezüglich der retinierten Zähne 18 und 48 empfohlen
- Konsultation eines Parodontologen zur Beurteilung des Zustands des Parodontalgewebes und zur Verordnung einer entsprechenden Behandlung angezeigt
- Durchführung einer professionellen Mundhygiene empfohlen

## Sonstiges
- Für eine detailliertere Beurteilung des Zustands des periapikalen Gewebes von Zahn 46 wird eine Einzelzahnröntgenaufnahme empfohlen
- Einschränkungen der Methode: mögliche Überlagerungen anatomischer Strukturen, die die Visualisierung bestimmter Bereiche erschweren
- Zur Beurteilung des Zustands des retinierten Zahns 48 und seines Verhältnisses zum Mandibularkanal wird die Durchführung einer DVT empfohlen

## Nächster Termin
- Einzelzahnröntgenaufnahme des Zahns 46 vor der endodontischen Behandlung
- Kontroll-Orthopantomographie 6 Monate nach der Behandlung
- DVT des Unterkiefers im Bereich des retinierten Zahns 48 vor der Planung des chirurgischen Eingriffs
```

Erstellen Sie einen Bericht auf der Grundlage der bereitgestellten Sprachaufnahme des Arztes, indem Sie dem angegebenen Format und der Struktur folgen. Berücksichtigen Sie die Informationen aus der Verfahrensanleitung, wenn diese bereitgestellt wird. 