from typing import Dict, Optional, Any
import os
import logging
from pathlib import Path
import json
import openai
from pydantic import BaseModel
import streamlit as st



class AirtableClient:
    """
    Клиент для работы с Airtable API.
    """
    
    def __init__(self, api_key: Optional[str] = None, base_id: Optional[str] = None):
        """
        Инициализация клиента Airtable.
        
        Args:
            api_key: API ключ Airtable
            base_id: ID базы Airtable
        """
        from pyairtable import Api
        
        # Попытка получить ключи из Streamlit secrets
        try:
            self.api_key = api_key or st.secrets["airtable_api_key"] or os.environ.get("AIRTABLE_API_KEY")
            self.base_id = base_id or st.secrets["airtable_base_id"] or os.environ.get("AIRTABLE_BASE_ID", "appZLoCCz0Oez1qMh")
        except Exception:
            # Если не удалось получить из Streamlit secrets, используем переменные окружения
            self.api_key = api_key or os.environ.get("AIRTABLE_API_KEY")
            self.base_id = base_id or os.environ.get("AIRTABLE_BASE_ID", "appZLoCCz0Oez1qMh")
        
        if self.api_key:
            self.api = Api(self.api_key)
            self.logger = logging.getLogger("airtable_client")
        else:
            self.api = None
            self.logger = logging.getLogger("airtable_client")
            self.logger.warning("API ключ Airtable не указан, функциональность ограничена")
    
    def get_procedure_by_id(self, procedure_id: str) -> Optional[Dict[str, Any]]:
        """
        Получает информацию о процедуре по ID.
        
        Args:
            procedure_id: ID процедуры
            
        Returns:
            Информация о процедуре или None
        """
        if not self.api:
            self.logger.warning("API ключ Airtable не указан, не удалось получить информацию о процедуре")
            return None
        
        try:
            table = self.api.table(self.base_id, "Procedures")
            formula = f"{{procedureId}}='{procedure_id}'"
            records = table.all(formula=formula)
            
            if records:
                return records[0]["fields"]
            else:
                self.logger.warning(f"Процедура с ID {procedure_id} не найдена в Airtable")
                return None
        except Exception as e:
            self.logger.error(f"Ошибка при получении процедуры из Airtable: {str(e)}")
            return None

    def get_procedure_by_category_name(self, category: str, name: str) -> Optional[Dict[str, Any]]:
        """
        Получает информацию о процедуре по категории и названию.
        
        Args:
            category: Категория процедуры
            name: Название процедуры
            
        Returns:
            Информация о процедуре или None
        """
        if not self.api:
            self.logger.warning("API ключ Airtable не указан, не удалось получить информацию о процедуре")
            return None
        
        try:
            table = self.api.table(self.base_id, "Procedures")
            formula = f"AND({{category}}='{category}', {{name}}='{name}')"
            records = table.all(formula=formula)
            
            if records:
                return records[0]["fields"]
            else:
                self.logger.warning(f"Процедура с категорией '{category}' и названием '{name}' не найдена в Airtable")
                return None
        except Exception as e:
            self.logger.error(f"Ошибка при получении процедуры из Airtable: {str(e)}")
            return None

class ReportAnalyzer:
    """
    Класс для анализа и структурирования отчетов по стоматологическим процедурам.
    """
    
    # Маппинг категорий из Airtable на имена директорий с промптами
    CATEGORY_DIR_MAP = {
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
        
        # Русские эквиваленты категорий
        "Консультация": "aufklarung",
        "Обследование": "aufklarung",
        "Эндодонтия": "endo",
        "Пломбы": "fullungen",
        "Имплантация": "implantation",
        "Детская стоматология": "kinder",
        "Пародонтология": "pa_pzr",
        "Профессиональная чистка": "pa_pzr",
        "Болевое лечение": "schmerzbehandlung",
        "Протезирование": "ze",
        "Рентгенография": "opg_dvt",
        "ВНЧС": "cmd", 
        "Ортодонтия": "kfo",
        "Хирургия": "chirurgie",
        
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
        "default": "aufklarung"  # использовать как шаблон по умолчанию
    }
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Инициализация анализатора отчетов.
        
        Args:
            api_key: API ключ OpenAI (опционально, по умолчанию из переменных окружения)
            model: Модель OpenAI (опционально, по умолчанию из переменных окружения или gpt-4o)
        """
        # Инициализация API ключа (сначала проверяем Streamlit secrets, затем аргументы, затем переменные окружения)
        try:
            self.api_key = api_key or st.secrets["openai_api_key"] or os.environ.get("OPENAI_API_KEY")
        except Exception:
            # Если не удалось получить из Streamlit secrets, используем переданный ключ или переменную окружения
            self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
            
        if not self.api_key:
            raise ValueError("API ключ OpenAI не указан и не найден в Streamlit secrets или переменных окружения")
            
        # Используем тестовый режим, если ключ начинается с "sk-test"
        self.test_mode = self.api_key.startswith("sk-test")
        
        # Инициализация модели
        self.model = model or os.environ.get("OPENAI_MODEL", "gpt-4o")
        
        # Настройка логгирования
        self.logger = logging.getLogger("report_analyzer")
        
        # Инициализация клиента Airtable (если не в тестовом режиме)
        if not self.test_mode:
            self.airtable_client = AirtableClient()
        else:
            self.logger.info("Запущен в тестовом режиме, Airtable не будет использоваться")
            self.airtable_client = None
        
        # Директория с промптами
        # Находим абсолютный путь к директории, в которой находится файл report_generator.py
        current_file_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        # Определяем путь к директории prompts относительно расположения файла
        self.prompts_dir = current_file_dir.parent.parent / "prompts"
        self.logger.info(f"Директория с промптами: {self.prompts_dir}")
        
        # Кэш для загруженных шаблонов
        self.prompt_cache = {}
        
        self.logger.debug(f"Инициализирован ReportAnalyzer с model={self.model}, test_mode={self.test_mode}")
        
        # Заполняем кэш промптов при инициализации
        self._preload_prompt_templates()
    
    def _preload_prompt_templates(self):
        """
        Предварительно загружает шаблоны промптов в кэш только для немецкого языка.
        """
        # Используем только немецкий язык
        language = "de"
        lang_dir = self.prompts_dir / language
        
        self.logger.info(f"Загрузка шаблонов из директории: {lang_dir}")
        
        if not lang_dir.exists() or not lang_dir.is_dir():
            self.logger.warning(f"Директория с промптами для немецкого языка не найдена: {lang_dir}")
            return
                
        # Обходим все поддиректории категорий
        for category_dir in lang_dir.iterdir():
            if not category_dir.is_dir():
                continue
                
            category_name = category_dir.name
            
            # Ищем файл template.md в директории категории
            template_path = category_dir / "template.md"
            
            self.logger.info(f"Проверяем наличие шаблона: {template_path}")
            
            if template_path.exists() and template_path.is_file():
                try:
                    with open(template_path, "r", encoding="utf-8") as f:
                        template_content = f.read()
                        cache_key = category_name  # Убираем префикс языка, т.к. используем только немецкий
                        self.prompt_cache[cache_key] = template_content
                        self.logger.info(f"Предзагружен шаблон для категории {category_name}: {template_path}")
                except Exception as e:
                    self.logger.error(f"Ошибка при загрузке шаблона {template_path}: {str(e)}")
            else:
                self.logger.warning(f"Файл шаблона не найден: {template_path}")
        
        # Записываем список доступных шаблонов в лог
        self.logger.info(f"Предзагружено {len(self.prompt_cache)} шаблонов промптов:")
        for key in sorted(self.prompt_cache.keys()):
            self.logger.debug(f"  - {key}")
    
    def load_prompt(self, category: str, language: str = "de") -> str:
        """
        Загружает шаблон промпта для указанной категории.
        Параметр language игнорируется, всегда используется немецкий.
        
        Args:
            category: Категория стоматологической процедуры
            language: Параметр сохранен для обратной совместимости (игнорируется)
            
        Returns:
            Содержимое файла промпта
        """
        # Всегда используем немецкий язык
        language = "de"
        
        # Получаем директорию с промптами для категории
        category_dir = self.CATEGORY_DIR_MAP.get(category, self.CATEGORY_DIR_MAP["default"])
        
        # Кэш-ключ для шаблона (без префикса языка)
        cache_key = category_dir
        
        # Проверяем, загружен ли уже этот шаблон
        if cache_key in self.prompt_cache:
            self.logger.debug(f"Используем шаблон из кэша для '{category}' (директория '{category_dir}')")
            return self.prompt_cache[cache_key]
        
        # Путь к шаблону категории
        template_path = self.prompts_dir / language / category_dir / "template.md"
        
        self.logger.info(f"Пытаемся загрузить шаблон: {template_path}")
        
        # Проверяем существование директории
        template_dir = self.prompts_dir / language / category_dir
        if not template_dir.exists() or not template_dir.is_dir():
            self.logger.warning(f"Директория категории не найдена: {template_dir}")
        
        # Если файл существует, загружаем его
        if template_path.exists() and template_path.is_file():
            try:
                # Загружаем шаблон из файла
                with open(template_path, "r", encoding="utf-8") as f:
                    template_content = f.read()
                    
                # Сохраняем в кэш
                self.prompt_cache[cache_key] = template_content
                self.logger.info(f"Загружен шаблон: {template_path}")
                return template_content
            except Exception as e:
                self.logger.error(f"Ошибка при чтении файла шаблона {template_path}: {str(e)}")
                # Возвращаем динамический шаблон вместо вызова исключения
                self.logger.info("Возвращаем динамический шаблон из-за ошибки чтения файла")
                template_content = self._get_dynamic_template()
                self.prompt_cache[cache_key] = template_content
                return template_content
        else:
            # Если шаблон не найден, возвращаем динамический шаблон
            self.logger.warning(f"Шаблон для категории '{category}' (директория '{category_dir}') не найден, используем динамический шаблон")
            template_content = self._get_dynamic_template()
            self.prompt_cache[cache_key] = template_content
            return template_content
    
    def _get_dynamic_template(self, language: str = "de") -> str:
        """
        Возвращает динамический шаблон промпта на немецком языке.
        Параметр language игнорируется.
        
        Args:
            language: Параметр сохранен для обратной совместимости (игнорируется)
            
        Returns:
            Шаблон промпта на немецком языке
        """
        return """
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

    def call_api(self, prompt: str, output_model=None):
        """
        Вызывает API OpenAI для генерации структурированного отчета.
        
        Args:
            prompt: Промпт для генерации
            output_model: Класс модели для преобразования ответа
            
        Returns:
            Структурированный отчет
        """
        if self.test_mode:
            self.logger.info("Тестовый режим: возвращаем тестовый отчет")
            # Тестовый отчет для разных языков
            test_report = {
                "title": "Тестовый отчет о стоматологической процедуре",
                "patient": {
                    "complaints": "Тестовые жалобы пациента",
                    "examination": "Тестовые результаты осмотра"
                },
                "procedure": {
                    "name": "Тестовая процедура",
                    "description": "Описание тестовой процедуры"
                },
                "materials": ["Тестовый материал 1", "Тестовый материал 2"],
                "treatment_plan": "Тестовый план лечения",
                "additional_info": "Тестовая дополнительная информация",
                "next_appointment": "Тестовая информация о следующем визите"
            }
            
            # Если нужен формат модели, преобразуем словарь к модели
            if output_model:
                return output_model(**test_report)
            return test_report
        
        try:
            openai_client = openai.OpenAI(api_key=self.api_key)
            self.logger.debug(f"Вызываем API с моделью {self.model}")
            
            response = openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Вы - стоматолог-эксперт, который создает структурированные отчеты о медицинских процедурах."},
                    {"role": "user", "content": prompt}
                ],
                # response_format=output_model
            )
            self.logger.info(f"Ответ от API: {response}")
            
            # Получаем JSON из ответа
            content = response.choices[0].message.content
            # data = json.loads(json_content)
            self.logger.info(f"Содержимое ответа: {content}")

            return content
        except Exception as e:
            self.logger.error(f"Ошибка при вызове API: {str(e)}")
            # В случае ошибки API, все равно возвращаем какой-то результат
            error_response = {
                "title": "Ошибка генерации отчета",
                "patient": {},
                "procedure": {},
                "materials": [],
                "treatment_plan": f"Произошла ошибка при генерации отчета: {str(e)}",
                "additional_info": "",
                "next_appointment": ""
            }
            
            if output_model:
                return output_model(**error_response)
            return error_response

    def analyze(
        self,
        transcription: str,
        language: str = "de",  # Параметр сохранен для обратной совместимости
        category: str = None,
        procedure: str = None,
        procedure_id: Optional[str] = None,
        procedure_name: Optional[str] = None,
        procedure_info: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Анализирует и структурирует отчет на основе транскрипции.
        
        Args:
            transcription: Текст транскрипции
            language: Параметр сохранен для обратной совместимости, но всегда используется немецкий язык
            category: Категория процедуры для шаблона промпта
            procedure: Название процедуры для шаблона промпта (не используется для поиска промпта, только для информации)
            procedure_id: ID процедуры в Airtable
            procedure_name: Название процедуры для запроса в Airtable
            procedure_info: Дополнительная информация о процедуре
            
        Returns:
            Структурированный отчет
        """
        # Игнорируем переданный язык, всегда используем немецкий
        language = "de"
        
        # Получаем информацию о процедуре из Airtable
        additional_info = {}
        
        if not self.test_mode and self.airtable_client:
            if procedure_id:
                # Получаем информацию по ID
                procedure_data = self.airtable_client.get_procedure_by_id(procedure_id)
                if procedure_data:
                    # Обновляем категорию и имя процедуры
                    category = category or procedure_data.get("category")
                    procedure = procedure or procedure_data.get("name")
                    additional_info = procedure_data
                    self.logger.info(f"Получена информация о процедуре из Airtable по ID: {procedure_id}")
            elif category and procedure_name:
                # Получаем информацию по категории и имени
                procedure_data = self.airtable_client.get_procedure_by_category_name(category, procedure_name)
                if procedure_data:
                    # Обновляем имя процедуры
                    procedure = procedure or procedure_data.get("name")
                    additional_info = procedure_data
                    self.logger.info(f"Получена информация о процедуре из Airtable по категории/имени: {category}/{procedure_name}")
        
        # Дополнительная информация о процедуре (приоритет над Airtable)
        if procedure_info:
            additional_info.update(procedure_info)
            # Обновляем category и procedure, если они указаны в procedure_info
            category = category or procedure_info.get("category")
            procedure = procedure or procedure_info.get("name")
        
        # Проверяем наличие категории
        if not category:
            category = "default"
            self.logger.warning(f"Категория не указана, используем значение по умолчанию")
        else:
            # Обрабатываем категории с символом "|" (например, "PA | PZR")
            # Берем первую часть категории до символа "|" и удаляем пробелы
            if "|" in category:
                parts = category.split("|")
                # Используем первую часть категории (до символа "|")
                clean_category = parts[0].strip()
                self.logger.info(f"Категория '{category}' содержит символ '|', используем первую часть: '{clean_category}'")
                category = clean_category
        
        # Загружаем шаблон промпта только на основе категории
        prompt_template = self.load_prompt(category)
        
        # Заполняем переменные в шаблоне
        prompt = prompt_template.replace("{{transcription}}", transcription)
        prompt = prompt.replace("{{procedure_name}}", additional_info.get("name", procedure or ""))
        prompt = prompt.replace("{{procedure_description}}", additional_info.get("description", ""))
        
        # Заполняем дополнительные переменные
        for key, value in additional_info.items():
            placeholder = f"{{{{{key}}}}}"
            if placeholder in prompt and value:
                prompt = prompt.replace(placeholder, str(value))
        
        # Вызываем API для генерации отчета
        self.logger.info(f"Генерация отчета для категории '{category}' на языке {language}, промпт: {prompt}")
        
        # Используем DentalReport для структурированного ответа
        try:
            result = self.call_api(prompt)
            self.logger.info(f"Отчет успешно сгенерирован")
            return result
        except Exception as e:
            self.logger.error(f"Ошибка при вызове API: {str(e)}")
            # В случае ошибки API или отсутствия класса DentalReport
            result = self.call_api(prompt)
            self.logger.info(f"Отчет сгенерирован без модели DentalReport")
            return result 

def generate_dental_report(
    transcription: str,
    language: str = "de",  # Параметр оставлен для обратной совместимости
    category: str = None,
    procedure: str = None,
    procedure_id: str = None,
    procedure_name: str = None,
    procedure_info: dict = None
) -> dict:
    """
    Функция-обертка для генерации стоматологического отчета на основе транскрипции.
    
    Args:
        transcription: Текст транскрипции
        language: Параметр сохранен для обратной совместимости, отчет всегда генерируется на немецком языке
        category: Категория процедуры для шаблона промпта
        procedure: Название процедуры для шаблона промпта
        procedure_id: ID процедуры в Airtable
        procedure_name: Название процедуры для запроса в Airtable
        procedure_info: Дополнительная информация о процедуре
        
    Returns:
        Структурированный отчет в виде словаря
    """
    # Получаем API ключ OpenAI из Streamlit secrets или переменных окружения
    try:
        api_key = st.secrets["openai_api_key"] or os.environ.get("OPENAI_API_KEY")
    except Exception:
        # Если не удалось получить из Streamlit secrets, используем только переменные окружения
        api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        # Если API ключ не найден, возвращаем сообщение об ошибке
        logging.warning("API ключ OpenAI не найден в Streamlit secrets или переменных окружения")
        return {
            "title": "Fehler bei der Berichtserstellung",
            "error": "OpenAI API-Schlüssel wurde nicht in Streamlit-Secrets oder Umgebungsvariablen gefunden",
            "patient": {},
            "procedure": {
                "name": procedure or procedure_name or "",
                "category": category or ""
            },
            "treatment_plan": "Bericht konnte nicht erstellt werden: OpenAI API-Schlüssel fehlt"
        }
    
    # Создаем экземпляр ReportAnalyzer
    analyzer = ReportAnalyzer(api_key=api_key)
    
    # Анализируем транскрипцию и генерируем отчет - всегда используем немецкий язык
    try:
        result = analyzer.analyze(
            transcription=transcription,
            language="de",  # Всегда используем немецкий язык
            category=category,
            procedure=procedure,
            procedure_id=procedure_id,
            procedure_name=procedure_name,
            procedure_info=procedure_info
        )
        
        return result
    except Exception as e:
        logging.error(f"Ошибка при генерации отчета: {str(e)}")
        return {
            "title": "Fehler bei der Berichtserstellung",
            "error": str(e),
            "patient": {},
            "procedure": {
                "name": procedure or procedure_name or "",
                "category": category or ""
            },
            "treatment_plan": f"Bei der Erstellung des Berichts ist ein Fehler aufgetreten: {str(e)}"
        } 