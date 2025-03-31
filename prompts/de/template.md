# Prompt für die Erstellung eines Berichts über {{VERFAHREN}}

## Aufgabe
Sie sind ein {{SPEZIALISIERUNG}}-Zahnarzt, der einen strukturierten Bericht über ein durchgeführtes {{VERFAHREN}} basierend auf der Sprachaufnahme des Arztes erstellen soll. Der Bericht sollte informativ, gut strukturiert sein und alle wichtigen Details des Verfahrens sowie Empfehlungen enthalten.

## Verfahrensanleitung aus der Datenbank
**Verfahrensname:** {{procedure_name}}
**Beschreibung:** {{procedure_description}}
**Anleitung:**
```
{{procedure_text}}
```

Wenn keine spezifischen Informationen zum Verfahren vorliegen, verwenden Sie die allgemeinen Anweisungen für {{KATEGORIE}}-Verfahren:
```
{{category_procedures}}
```

## Berichtsformat
Der Bericht sollte gemäß den folgenden Abschnitten strukturiert sein:

1. **{{BERICHTSTITEL}}** - Berichtsüberschrift
2. **Aufklärung** - Patienteninformation, Anamnese, Beschwerden
3. **Befund** - Untersuchungsergebnisse, Diagnostik
4. **Verwendete Materialien** - Verwendete Materialien und Instrumente
5. **Durchführung** - Beschreibung des durchgeführten Verfahrens
6. **Therapieplanung** - Empfehlungen und Plan für die weitere Behandlung
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
  {{WICHTIGE_DETAILS}}
- Im Abschnitt "Befund" geben Sie {{BEFUND_DETAILS}} an
- Im Abschnitt "Verwendete Materialien" listen Sie {{MATERIALIEN_DETAILS}} auf
- Im Abschnitt "Durchführung" beschreiben Sie detailliert jeden Schritt des Verfahrens:
  {{VERFAHRENSSCHRITTE}}
- Im Abschnitt "Therapieplanung" listen Sie {{THERAPIEPLANUNG_DETAILS}} auf

## Beispielbericht
```
{{BEISPIELBERICHT}}
```

Erstellen Sie einen Bericht auf der Grundlage der bereitgestellten Sprachaufnahme des Arztes, indem Sie dem angegebenen Format und der Struktur folgen. Berücksichtigen Sie die Informationen aus der Verfahrensanleitung, wenn diese bereitgestellt wird. 