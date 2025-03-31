#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from dental_assistant.report_generator import ReportAnalyzer

# Пример транскрипции на русском языке
RUSSIAN_TRANSCRIPTION = """
Пациент обратился с жалобами на боль в зубе 36. При осмотре обнаружен глубокий кариес с вовлечением пульпы.
Была проведена анестезия Ультракаин 1.7 мл. Выполнена эндодонтическая ревизия. Обнаружены три канала: 
медиально-буккальный, медиально-лингвальный и дистальный. Рабочая длина МБ канала 21 мм, МЛ канала 20.5 мм,
дистального канала 19 мм. Проведена хемомеханическая обработка каналов инструментами ProTaper. 
Ирригация гипохлоритом натрия 3%, ЭДТА 17%, физраствором. Каналы запломбированы методом латеральной конденсации
с использованием силера AH Plus. Поставлена временная пломба из Септопака. Рекомендован рентген-контроль через неделю.
Пациент записан на дальнейшее лечение через 7 дней.
"""

# Пример транскрипции на немецком языке
GERMAN_TRANSCRIPTION = """
Der Patient kam mit Schmerzen im Zahn 46. Bei der Untersuchung wurde eine tiefe Karies mit Pulpabeteiligung festgestellt.
Es wurde eine Anästhesie mit Ultracain 1.7 ml durchgeführt. Eine endodontische Revision wurde durchgeführt. 
Es wurden drei Kanäle gefunden: mesio-bukkal, mesio-lingual und distal. Die Arbeitslänge des MB-Kanals betrug 20 mm, 
des ML-Kanals 19,5 mm und des distalen Kanals 18 mm. Es wurde eine chemomechanische Aufbereitung der Kanäle mit 
ProTaper-Instrumenten durchgeführt. Spülung mit 3% Natriumhypochlorit, 17% EDTA und Kochsalzlösung. 
Die Kanäle wurden mit der lateralen Kondensationsmethode unter Verwendung des Sealers AH Plus gefüllt. 
Es wurde eine temporäre Füllung aus Septopak gelegt. Eine Röntgenkontrolle wurde für die nächste Woche empfohlen.
Der Patient hat einen Termin zur weiteren Behandlung in 7 Tagen.
"""

# API ключ
API_KEY = "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"

def main():
    """Основная функция тестирования"""
    # Создаем анализатор отчетов с указанным API ключом
    analyzer = ReportAnalyzer(api_key=API_KEY)
    
    print("=== Тестирование генерации отчета на русском языке ===")
    
    # Генерируем отчет на основе русской транскрипции
    russian_report = analyzer.analyze(
        transcription=RUSSIAN_TRANSCRIPTION,
        category="endo",
        procedure="endo_revision",
        language="ru"
    )
    
    # Выводим результат
    print(json.dumps(russian_report, ensure_ascii=False, indent=2))
    print("\n\n")
    
    print("=== Тестирование генерации отчета на немецком языке ===")
    
    # Генерируем отчет на основе немецкой транскрипции
    german_report = analyzer.analyze(
        transcription=GERMAN_TRANSCRIPTION,
        category="endo",
        procedure="endo_revision",
        language="de"
    )
    
    # Выводим результат
    print(json.dumps(german_report, ensure_ascii=False, indent=2))
    
    print("\n\n")
    print("=== Тестирование автоматического определения категории и процедуры ===")
    
    # Тестируем автоматическое определение категории и процедуры
    auto_report = analyzer.analyze(
        transcription=RUSSIAN_TRANSCRIPTION
    )
    
    # Выводим результат
    print(json.dumps(auto_report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main() 