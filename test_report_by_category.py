#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
from dental_assistant.frontend.report_generator import ReportAnalyzer, generate_dental_report

# Устанавливаем тестовый API ключ
os.environ["OPENAI_API_KEY"] = "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"

# Пример транскрипции на русском языке
SAMPLE_TRANSCRIPTION_RU = """
Пациент обратился с жалобой на периодическую боль в области зуба 47.
При осмотре: визуализируется глубокая кариозная полость на жевательной поверхности.
Перкуссия слабо болезненная, реакция на холод резко болезненная, быстропроходящая.
Принято решение о проведении эндодонтического лечения.
После анестезии Sol. Articaini 4% провел раскрытие полости зуба, обнаружены 3 канала.
Проведена механическая и медикаментозная обработка каналов, постоянное пломбирование гуттаперчей и силером.
Пациенту рекомендовано контрольное посещение через неделю.
"""

def test_analyzer_by_id():
    """Тестирование генерации отчета с использованием procedure_id"""
    print("\n=== Тест генерации отчета с использованием procedure_id ===")
    
    # Создаем анализатор
    analyzer = ReportAnalyzer()
    
    # Генерируем отчет с использованием ID
    report = generate_dental_report(
        transcription=SAMPLE_TRANSCRIPTION_RU,
        language="ru",
        procedure_id="endotreatment"  # Предполагаемый ID для эндодонтического лечения
    )
    
    # Выводим результат
    print(json.dumps(report, ensure_ascii=False, indent=2))
    
    return report

def test_analyzer_by_category_name():
    """Тестирование генерации отчета с использованием категории и названия процедуры"""
    print("\n=== Тест генерации отчета с использованием категории и названия ===")
    
    # Генерируем отчет с использованием категории и названия
    report = generate_dental_report(
        transcription=SAMPLE_TRANSCRIPTION_RU,
        language="ru",
        category="Endodontics",  # Категория (может отличаться в зависимости от данных в Airtable)
        procedure="Эндодонтическое лечение"  # Название процедуры
    )
    
    # Выводим результат
    print(json.dumps(report, ensure_ascii=False, indent=2))
    
    return report

def test_auto_detection():
    """Тестирование автоматического определения категории и процедуры"""
    print("\n=== Тест автоматического определения категории и процедуры ===")
    
    from dental_assistant.frontend.report_integration import detect_category, generate_report_from_text
    
    # Определяем категорию и процедуру
    category, procedure = detect_category(SAMPLE_TRANSCRIPTION_RU)
    print(f"Определенная категория: {category}")
    print(f"Определенная процедура: {procedure}")
    
    # Генерируем отчет с автоматическим определением
    report = generate_report_from_text(SAMPLE_TRANSCRIPTION_RU)
    
    # Выводим результат
    print(json.dumps(report, ensure_ascii=False, indent=2))
    
    return report

if __name__ == "__main__":
    print("Тестирование генерации отчетов по категории и названию процедуры")
    print("-" * 70)
    
    # Тестируем по ID
    test_analyzer_by_id()
    
    # Тестируем по категории и названию
    test_analyzer_by_category_name()
    
    # Тестируем автоматическое определение
    test_auto_detection() 