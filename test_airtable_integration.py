#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from dental_assistant.report_generator import ReportAnalyzer, AirtableClient

# API ключ
API_KEY = "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"

def test_airtable_client():
    """Тестирование клиента Airtable"""
    print("=== Тестирование AirtableClient ===")
    
    # Создаем клиент Airtable
    airtable_client = AirtableClient()
    
    # Проверяем процедуру "extraktion"
    procedure_id = "extraktion"
    print(f"Получение информации о процедуре с ID: {procedure_id}")
    
    # Получаем информацию о процедуре
    procedure_info = airtable_client.get_procedure_info(procedure_id)
    
    # Выводим результат
    print(json.dumps(procedure_info, ensure_ascii=False, indent=2))
    print("\n")

def test_analyzer_with_procedure_id():
    """Тестирование анализатора с использованием procedure_id"""
    print("=== Тестирование анализатора с procedure_id ===")
    
    # Создаем анализатор с указанным API ключом
    analyzer = ReportAnalyzer(api_key=API_KEY)
    
    # Пример транскрипции на русском языке для экстракции
    transcription = """
    Пациент обратился с жалобами на боль в зубе 47. При осмотре обнаружен глубокий кариес, 
    не подлежащий восстановлению. Была проведена анестезия Ультракаин 1.7 мл. 
    Выполнена атравматичная экстракция зуба 47 с использованием щипцов для моляров. 
    Лунка обработана антисептиком Хлоргексидин 0.05%. Наложены швы Викрил 3-0. 
    Даны рекомендации по уходу после удаления. Назначен Ибупрофен 400 мг при болях. 
    Пациент записан на снятие швов через 7 дней.
    """
    
    # Генерируем отчет, указав только procedure_id
    print("Генерация отчета с указанием только procedure_id:")
    report = analyzer.analyze(
        transcription=transcription,
        procedure_id="extraktion",
        language="ru"
    )
    
    # Выводим результат
    print(json.dumps(report, ensure_ascii=False, indent=2))

def main():
    """Основная функция"""
    # Тестируем клиент Airtable
    test_airtable_client()
    
    # Тестируем анализатор с procedure_id
    test_analyzer_with_procedure_id()

if __name__ == "__main__":
    main() 