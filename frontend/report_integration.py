#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import streamlit as st
import json
import sys
from typing import Dict, Any, Optional, Tuple

# Добавляем корневую директорию в sys.path для импорта модулей
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from report_generator import generate_dental_report, ReportAnalyzer

def detect_language(text: str) -> str:
    """
    Определяет язык текста (русский или немецкий).
    
    Args:
        text: Текст для анализа
        
    Returns:
        Код языка ('ru' или 'de')
    """
    # Простая эвристика для определения языка
    russian_chars = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    german_chars = 'äöüß'
    
    # Приводим к нижнему регистру
    text = text.lower()
    
    # Подсчитываем количество русских и немецких символов
    ru_count = sum(1 for char in text if char in russian_chars)
    de_count = sum(1 for char in text if char in german_chars)
    
    # Если русских символов больше, возвращаем 'ru', иначе 'de'
    return 'ru' if ru_count > de_count else 'de'

def detect_category(text: str) -> Tuple[str, str]:
    """
    Определяет категорию и процедуру на основе текста.
    
    Args:
        text: Текст транскрипции
        
    Returns:
        Кортеж (категория, процедура)
    """
    # Словарь ключевых слов для категорий и процедур
    categories = {
        'endo': ['эндо', 'каналы', 'канал', 'пульпит', 'endo', 'kanal', 'wurzelbehandlung'],
        'chirurgie': ['удаление', 'экстракция', 'extraktion', 'entfernung', 'хирург'],
        'fullungen': ['пломба', 'композит', 'füllung', 'komposit', 'пломбирование'],
        'implantation': ['имплант', 'имплантат', 'implant'],
        'kfo': ['брекеты', 'элайнеры', 'brackets', 'aligner', 'ортодонт'],
        'kinder': ['детский', 'ребенок', 'kinder', 'kind', 'молочн'],
        'opg_dvt': ['снимок', 'рентген', 'опг', 'двт', 'opg', 'röntgen', 'dvt'],
        'pa_pzr': ['чистка', 'пародонт', 'зубной камень', 'parodont', 'zahnstein', 'pzr', 'пародонтит'],
        'schmerzbehandlung': ['боль', 'schmerz', 'обезболивание'],
        'ze': ['коронка', 'протез', 'krone', 'prothese', 'протезирование'],
        'cmd': ['внчс', 'сустав', 'kiefergelenk', 'cmd', 'вчнс'],
        'aufklarung': ['консультация', 'осмотр', 'beratung', 'untersuchung']
    }
    
    # Словарь процедур для каждой категории
    procedures = {
        'endo': ['endo_revision'],
        'chirurgie': ['extraktion'],
        'fullungen': ['komposit'],
        'implantation': ['implantat_setzen'],
        'kfo': ['brackets'],
        'kinder': ['kariesbehandlung'],
        'opg_dvt': ['opg'],
        'pa_pzr': ['pa_status', 'pzr'],
        'schmerzbehandlung': ['schmerztheraphie'],
        'ze': ['krone'],
        'cmd': ['funktionsanalyse'],
        'aufklarung': ['erstberatung']
    }
    
    # Приводим текст к нижнему регистру
    text = text.lower()
    
    # Проверяем соответствие ключевым словам
    category_scores = {}
    for category, keywords in categories.items():
        score = sum(text.count(keyword) for keyword in keywords)
        category_scores[category] = score
    
    # Находим категорию с наибольшим количеством совпадений
    if not category_scores:
        return ('base', 'template')
        
    best_category = max(category_scores.items(), key=lambda x: x[1])
    
    # Если нет явных совпадений, возвращаем базовую категорию
    if best_category[1] == 0:
        return ('base', 'template')
    
    # Для найденной категории определяем процедуру
    # Для простоты возьмем первую процедуру из списка
    category = best_category[0]
    procedure = procedures.get(category, ['default'])[0]
    
    # Для pa_pzr проверим, какая из процедур больше подходит
    if category == 'pa_pzr':
        if any(keyword in text for keyword in ['pa_status', 'статус', 'пародонтальный']):
            procedure = 'pa_status'
        else:
            procedure = 'pzr'
    
    return (category, procedure)

def generate_report_from_text(
    transcription: str,
    category: Optional[str] = None,
    procedure: Optional[str] = None,
    language: Optional[str] = None,
    procedure_info: Optional[Dict[str, str]] = None,
    procedure_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Генерирует отчет на основе текста транскрипции.
    Если категория, процедура или язык не указаны, определяет их автоматически.
    
    Args:
        transcription: Текст транскрипции
        category: Категория процедуры (опционально)
        procedure: Название процедуры (опционально)
        language: Язык отчета (опционально)
        procedure_info: Дополнительная информация о процедуре (опционально)
        procedure_id: ID процедуры в Airtable (опционально)
        
    Returns:
        Структурированный отчет
    """
    # Определяем язык, если не указан
    if not language:
        language = detect_language(transcription)
    
    # Если указан procedure_id, используем его напрямую
    if procedure_id:
        return generate_dental_report(
            transcription=transcription,
            language=language,
            procedure_id=procedure_id
        )
    
    # Определяем категорию и процедуру, если не указаны
    if not category or not procedure:
        detected_category, detected_procedure = detect_category(transcription)
        category = category or detected_category
        procedure = procedure or detected_procedure
    
    # Генерируем отчет, используя категорию и процедуру
    return generate_dental_report(
        transcription=transcription,
        category=category,
        procedure=procedure,
        language=language,
        procedure_info=procedure_info
    )

def report_to_markdown(report: Dict[str, Any]) -> str:
    """
    Преобразует структурированный отчет в формат Markdown.
    
    Args:
        report: Структурированный отчет
        
    Returns:
        Отчет в формате Markdown
    """
    # Заголовок отчета
    markdown = f"# {report.get('title', 'Отчет')}\n\n"
    
    # Добавляем стандартные разделы
    sections = {
        'aufklarung': 'Aufklärung',
        'befund': 'Befund',
        'verwendete_materialien': 'Verwendete Materialien',
        'durchfuhrung': 'Durchführung',
        'therapieplanung': 'Therapieplanung',
        'sonstiges': 'Sonstiges',
        'nachster_termin': 'Nächster Termin'
    }
    
    for key, title in sections.items():
        value = report.get(key, [])
        if value:
            markdown += f"## {title}\n"
            
            # Если значение - список, преобразуем в маркированный список
            if isinstance(value, list):
                for item in value:
                    if item:  # Проверяем, что элемент не пустой
                        markdown += f"- {item}\n"
            else:
                markdown += f"{value}\n"
            
            markdown += "\n"
    
    # Добавляем специфичные для категории поля, если они есть
    special_fields = {}
    for key, value in report.items():
        if key not in ['title'] + list(sections.keys()) and value:
            special_fields[key] = value
    
    if special_fields:
        markdown += "## Дополнительная информация\n\n"
        for key, value in special_fields.items():
            if isinstance(value, list):
                markdown += f"### {key}\n"
                for item in value:
                    markdown += f"- {item}\n"
            elif isinstance(value, dict):
                markdown += f"### {key}\n"
                for k, v in value.items():
                    markdown += f"- {k}: {v}\n"
            else:
                markdown += f"### {key}\n{value}\n"
            markdown += "\n"
    
    return markdown

# Функция для получения списка процедур из Airtable
def get_procedures_from_airtable():
    """
    Получает список процедур из Airtable для виджета.
    
    Returns:
        Список словарей с данными о процедурах
    """
    try:
        # Создаем экземпляр анализатора, чтобы получить доступ к AirtableClient
        analyzer = ReportAnalyzer()
        
        # Используем клиент Airtable
        table = analyzer.airtable_client.api.table(
            analyzer.airtable_client.base_id,
            "Procedures"
        )
        
        # Получаем все записи
        records = table.all()
        
        # Формируем список процедур
        procedures = []
        for record in records:
            if "fields" in record:
                procedure = {
                    "id": record["fields"].get("procedureId", ""),
                    "name": record["fields"].get("name", ""),
                    "category": record["fields"].get("category", ""),
                    "description": record["fields"].get("description", "")
                }
                procedures.append(procedure)
        
        return procedures
    except Exception as e:
        st.error(f"Ошибка при получении списка процедур: {str(e)}")
        return []

# Функция для интеграции с Streamlit
def render_report_widget(key="report_widget"):
    """
    Отображает виджет для генерации отчета в Streamlit.
    
    Args:
        key: Уникальный ключ для виджета
    """
    with st.expander("Генератор отчетов", expanded=False):
        # Ввод транскрипции
        transcription = st.text_area(
            "Текст транскрипции",
            height=200,
            key=f"{key}_transcription"
        )
        
        # Получаем список процедур из Airtable
        airtable_procedures = get_procedures_from_airtable()
        
        # Группируем процедуры по категориям
        procedures_by_category = {}
        for proc in airtable_procedures:
            category = proc.get("category", "Без категории")
            if category not in procedures_by_category:
                procedures_by_category[category] = []
            procedures_by_category[category].append(proc)
        
        # Дополнительные настройки
        col1, col2 = st.columns(2)
        
        with col1:
            # Выбор метода определения процедуры
            detection_method = st.radio(
                "Метод определения процедуры",
                options=["Автоматически", "Выбрать из списка"],
                key=f"{key}_detection_method"
            )
            
            procedure_id = None
            selected_category = None
            selected_procedure = None
            
            if detection_method == "Выбрать из списка":
                # Выбор категории
                category_options = list(procedures_by_category.keys())
                selected_category = st.selectbox(
                    "Категория",
                    options=[""] + category_options,
                    key=f"{key}_category_select"
                )
                
                # Выбор процедуры из выбранной категории
                if selected_category:
                    procedure_options = procedures_by_category[selected_category]
                    selected_procedure = st.selectbox(
                        "Процедура",
                        options=procedure_options,
                        format_func=lambda x: x.get("name", ""),
                        key=f"{key}_procedure_select"
                    )
                    
                    if selected_procedure:
                        procedure_id = selected_procedure.get("id")
                        
                        # Показываем информацию о выбранной процедуре
                        st.info(
                            f"**{selected_procedure.get('name')}**\n\n"
                            f"{selected_procedure.get('description', '')}"
                        )
            else:
                st.info("Категория и процедура будут определены автоматически на основе текста транскрипции.")
        
        with col2:
            # Выбор языка
            languages = {
                'auto': 'Автоматически',
                'ru': 'Русский',
                'de': 'Немецкий'
            }
            
            language = st.selectbox(
                "Язык отчета",
                options=list(languages.keys()),
                format_func=lambda x: languages.get(x, x),
                key=f"{key}_language"
            )
            
            # Выбор формата вывода
            output_format = st.selectbox(
                "Формат вывода",
                options=['markdown', 'json'],
                format_func=lambda x: 'Markdown (читаемый текст)' if x == 'markdown' else 'JSON (структурированные данные)',
                key=f"{key}_format"
            )
        
        # Кнопка для генерации отчета
        if st.button("Сгенерировать отчет", key=f"{key}_generate"):
            if not transcription:
                st.error("Пожалуйста, введите текст транскрипции.")
                return
            
            with st.spinner("Генерация отчета..."):
                try:
                    # Подготовка параметров
                    params = {}
                    
                    # Если выбрано "Выбрать из списка" и процедура выбрана
                    if detection_method == "Выбрать из списка" and selected_procedure:
                        # Предпочитаем использовать ID процедуры, если он есть
                        if procedure_id:
                            params['procedure_id'] = procedure_id
                        # Если ID нет, используем категорию и название
                        else:
                            params['category'] = selected_category
                            params['procedure'] = selected_procedure.get("name", "")
                    
                    # Если язык не "auto", указываем язык
                    if language != 'auto':
                        params['language'] = language
                    
                    # Генерация отчета
                    report = generate_report_from_text(transcription, **params)
                    
                    # Отображение результата
                    if output_format == 'markdown':
                        st.markdown(report_to_markdown(report))
                    else:
                        st.json(report)
                    
                    # Сохранение в сессии для дальнейшего использования
                    st.session_state[f"{key}_last_report"] = report
                    
                except Exception as e:
                    st.error(f"Ошибка при генерации отчета: {str(e)}")

# Пример использования
if __name__ == "__main__":
    st.set_page_config(page_title="Генератор отчетов", layout="wide")
    st.title("Генератор отчетов по транскрипциям")
    
    render_report_widget() 