from typing import Dict, Optional, Any
import os
import logging
import yaml
from pathlib import Path
import openai
import streamlit as st

# Минимальный набор встроенных шаблонов
DEFAULT_TEMPLATES = {
    "default": """
    Aufgabe für den Zahnarzt-Experten

    Sie müssen einen strukturierten medizinischen Bericht auf der Grundlage der Transkription der Rede des Arztes erstellen.

    Transkription:
    {{transcription}}

    Verfahren: {{procedure_name}}
    {{procedure_description}}

    Ihre Aufgabe ist es, die Transkription sorgfältig zu analysieren und einen strukturierten Bericht über das zahnärztliche Verfahren zu erstellen. Verwenden Sie das internationale Zahnzahlungssystem (FDI).

    Der Bericht sollte enthalten:
    1. Überschrift (Name des Verfahrens)
    2. Beschwerden des Patienten und Anamnese
    3. Untersuchungsergebnisse
    4. Verwendete Materialien
    5. Beschreibung des Verfahrens
    6. Behandlungsplan und Empfehlungen
    7. Zusätzliche Informationen (falls vorhanden)
    8. Nächster Besuch (falls angegeben)

    Nehmen Sie alle klinisch relevanten Details aus der Transkription auf. Verwenden Sie professionelle medizinische Terminologie, aber bewahren Sie die Klarheit der Darstellung.
    """
}

# Словарь для маппинга категорий на имена ключей в конфиге промптов
CATEGORY_KEY_MAP = {
    # Точные названия категорий из Airtable
    "Aufklärung": "aufklarung",  
    "Befundaufnahme": "aufklarung",  # обе категории используют один шаблон
    "Endo": "endo",
    "Füllungen": "fullungen",
    "Implantation": "implantation",
    "Kinder": "kinder",
    "PA": "pa_pzr",
    "PZR": "pa_pzr",  # обе категории используют один шаблон
    "Smerzbehandlung": "schmerzbehandlung",
    "ZE": "ze",
    "OPG-DVT": "opg_dvt",
    "CMD": "cmd",
    "KFO": "kfo",
    "Chirurgie": "chirurgie",
    
    # Немецкие дополнительные синонимы
    "Endodontie": "endo",
    "Zahnfüllungen": "fullungen",
    "Implantologie": "implantation",
    "Kinderzahnheilkunde": "kinder",
    "Parodontologie": "pa_pzr",
    "Professionelle Zahnreinigung": "pa_pzr",
    "Schmerzbehandlung": "schmerzbehandlung",
    "Zahnprothetik": "ze",
    "Prothetik": "ze",
    "Röntgendiagnostik": "opg_dvt",
    "Kieferorthopädie": "kfo",
    "Chirurgische Eingriffe": "chirurgie",
    
    # Значение по умолчанию
    "default": "default"
}

class ReportGenerator:
    """
    Класс для генерации отчетов о стоматологических процедурах.
    """
    
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        """
        Инициализация генератора отчетов.
        
        Args:
            api_key: API ключ OpenAI
            model: Модель OpenAI
        """
        self.api_key = api_key
        self.model = model
        self.client = openai.OpenAI(api_key=api_key)
        self.logger = logging.getLogger(__name__)
        
        # Загрузка промптов
        self.templates = self._load_prompts()
        
        self.logger.debug(f"Инициализирован ReportGenerator с model={self.model}")

    def _load_prompts(self) -> Dict[str, str]:
        """
        Загружает шаблоны промптов из YAML файла.
        
        Returns:
            Dict[str, str]: Словарь шаблонов, где ключ - категория, значение - шаблон
        """
        templates = {}
        yaml_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "prompts", "templates.yaml")
        
        try:
            if os.path.exists(yaml_path):
                with open(yaml_path, 'r', encoding='utf-8') as file:
                    templates = yaml.safe_load(file)
                self.logger.info(f"Загружено {len(templates)} шаблонов из YAML файла")
            else:
                self.logger.warning(f"YAML файл с шаблонами не найден: {yaml_path}")
                templates = DEFAULT_TEMPLATES
        except Exception as e:
            self.logger.error(f"Ошибка при загрузке YAML файла: {e}")
            templates = DEFAULT_TEMPLATES
        
        # Убедимся, что есть хотя бы стандартный шаблон
        if "default" not in templates and templates:
            # Используем первый доступный шаблон как стандартный
            default_key = list(templates.keys())[0]
            templates["default"] = templates[default_key]
        elif not templates:
            templates = DEFAULT_TEMPLATES
            
        self.logger.info(f"Загружено {len(templates)} шаблонов")
        return templates

    def _get_prompt_template(self, category: str) -> str:
        """
        Возвращает шаблон промпта для указанной категории.
        
        Args:
            category: Категория процедуры
            
        Returns:
            Шаблон промпта
        """
        # Получаем ключ для категории
        key = CATEGORY_KEY_MAP.get(category, "default")
        
        # Возвращаем шаблон по ключу или шаблон по умолчанию
        return self.templates.get(key, self.templates["default"])

    def generate_report(
        self,
        transcription: str,
        category: str = None,
        procedure_name: str = None,
        procedure_id: str = None,
        procedure_info: Dict[str, Any] = None
    ) -> str:
        """
        Генерирует отчет на основе транскрипции.
        
        Args:
            transcription: Текст транскрипции
            category: Категория процедуры
            procedure_name: Название процедуры
            procedure_id: ID процедуры в Airtable
            procedure_info: Дополнительная информация о процедуре
            
        Returns:
            Отчет в текстовом формате
        """
        # Дополнительная информация о процедуре
        additional_info = procedure_info or {}
        
        # Проверяем наличие категории
        if not category:
            category = "default"
            self.logger.warning("Категория не указана, используем значение по умолчанию")
        else:
            # Обрабатываем категории с символом "|"
            if "|" in category:
                parts = category.split("|")
                category = parts[0].strip()
                self.logger.info(f"Категория '{category}' содержит символ '|', используем первую часть: '{category}'")
        
        # Получаем шаблон промпта
        prompt_template = self._get_prompt_template(category)
        
        # Заполняем переменные в шаблоне
        prompt = prompt_template.replace("{{transcription}}", transcription)
        prompt = prompt.replace("{{procedure_name}}", additional_info.get("name", procedure_name or ""))
        prompt = prompt.replace("{{procedure_description}}", additional_info.get("description", ""))
        
        # Заполняем дополнительные переменные
        for key, value in additional_info.items():
            placeholder = f"{{{{{key}}}}}"
            if placeholder in prompt and value:
                prompt = prompt.replace(placeholder, str(value))
        
        self.logger.info(f"Генерация отчета для категории: {category}")
        
        # Вызываем OpenAI API
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,
                seed=2025
            )
            
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"Ошибка при вызове OpenAI API: {str(e)}")
            return f"Fehler bei der Berichtserstellung: {str(e)}"

@st.cache_data(
ttl=86400,
show_spinner=True, 
max_entries=100,
)
def generate_dental_report(
    transcription: str,
    category: str = None,
    procedure_name: str = None,
    procedure_id: str = None,
    procedure_info: dict = None
) -> str:
    """
    Функция-обертка для генерации стоматологического отчета.
    
    Args:
        transcription: Текст транскрипции
        category: Категория процедуры
        procedure_name: Название процедуры
        procedure_id: ID процедуры в Airtable
        procedure_info: Дополнительная информация о процедуре
        
    Returns:
        Отчет в текстовом формате
    """
    # Получаем API ключ OpenAI
    try:
        api_key = st.secrets["openai_api_key"] or os.environ.get("OPENAI_API_KEY")
    except Exception:
        api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        return "Fehler: OpenAI API-Schlüssel nicht gefunden."
    
    # Создаем генератор отчетов
    generator = ReportGenerator(api_key=api_key)
    
    # Генерируем отчет
    return generator.generate_report(
        transcription=transcription,
        category=category,
        procedure_name=procedure_name,
        procedure_id=procedure_id,
        procedure_info=procedure_info
    ) 
