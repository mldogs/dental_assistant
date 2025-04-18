import streamlit as st
import requests
import json
import math
from io import BytesIO
import os
import base64
import hmac
import openai
import tempfile
import yaml
import sys
from datetime import datetime
import pandas as pd
from pyairtable import Api
from pyairtable.formulas import match
from pyairtable.api.table import Table

# Добавляем корневой каталог проекта в sys.path
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from frontend.models.process_report import process_dental_transcription_universal, REPORT_MAPPING

# from pydub import AudioSegment
import wave
# AudioSegment.converter = "/usr/bin/ffmpeg"

# Словарь для маппинга категорий на типы отчетов
CATEGORY_KEY_MAP = {
    # Точные названия категорий из Airtable
    "Aufklärung": "befundaufnahme",  
    "Befundaufnahme": "befundaufnahme",
    "Endo": "endo",
    "Füllungen": "fullungen",
    "Implantation": "implantation",
    "Kinder": "kinder",
    "PA": "pa_pzr",
    "PZR": "pa_pzr",
    "Smerzbehandlung": "schmerzbehandlung",
    "Schmerzbehandlung": "schmerzbehandlung",
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
    "Zahnprothetik": "ze",
    "Prothetik": "ze",
    "Röntgendiagnostik": "opg_dvt",
    "Kieferorthopädie": "kfo",
    "Chirurgische Eingriffe": "chirurgie",
    
    # Значение по умолчанию
    "default": "endo"  # По умолчанию используем endo
}

api_key = st.secrets["openai_api_key"] or os.environ.get("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

@st.cache_data(ttl=86400, show_spinner=True, max_entries=100)
def generate_dental_report(
    transcription: str,
    category: str = None,
    procedure_name: str = None,
    procedure_info: dict = None,
    doctor_name: str = "Dr. Zahnarzt"
) -> str:
    """
    Функция-обертка для генерации стоматологического отчета через process_dental_transcription_universal
    
    Args:
        transcription: Текст транскрипции
        category: Категория процедуры
        procedure_name: Название процедуры
        procedure_info: Дополнительная информация о процедуре
        doctor_name: Имя врача (по умолчанию "Dr. Zahnarzt")
        
    Returns:
        Отчет в текстовом формате
    """
      
    # Получаем дополнительную информацию о процедуре
    additional_info = procedure_info or {}
    
       
    # Получаем тип отчета на основе категории
    report_type = get_report_type_from_category(category)
    
    # Получаем название процедуры
    proc_name = additional_info.get("name", procedure_name or "")
    
    # Получаем описание процедуры
    proc_description = additional_info.get("description", "")
    
    print(f"Генерация отчета типа {report_type} для категории: {category}")
    
    try:
        # Вызываем универсальную функцию
        formatted_report, _ = process_dental_transcription_universal(
            transcription=transcription,
            procedure_name=proc_name,
            doctor_name=doctor_name,
            procedure_description=proc_description,
            report_type=report_type,
            model="gpt-4.1-2025-04-14",
            client=client
        )
        
        return formatted_report
        
    except Exception as e:
        print(f"Ошибка при создании отчета: {str(e)}")
        return f"Fehler bei der Berichtserstellung: {str(e)}"

def get_report_type_from_category(category: str) -> str:
    """
    Определяет тип отчета на основе категории процедуры
    
    Args:
        category: Категория процедуры
        
    Returns:
        Тип отчета для использования в process_dental_transcription_universal
    """
    # Обрабатываем категории с символом "|"
    if category and "|" in category:
        parts = category.split("|")
        category = parts[0].strip()
        print(f"Категория '{category}' содержит символ '|', используем первую часть: '{category}'")
    
    # Получаем тип отчета для категории или значение по умолчанию
    return CATEGORY_KEY_MAP.get(category, CATEGORY_KEY_MAP["default"])

# Настройка страницы
st.set_page_config(
    page_title="Zahnarztpraxis System",
    page_icon="🦷",
    layout="centered"
)

# Загружаем CSS из внешнего файла
def load_css(css_file):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(current_dir, css_file)
    with open(css_path, 'r', encoding='utf-8') as f:
        css_content = f.read()
        return css_content

# Применяем стили из внешнего файла
try:
    css_content = load_css('styles.css')
    st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)
except Exception as e:
    st.warning(f"Не удалось загрузить файл стилей: {str(e)}")

# Настройка системы аутентификации
# Инициализация состояния аутентификации
if 'auth_status' not in st.session_state:
    st.session_state.auth_status = "unverified"

# Установка пароля (предпочтительно использовать secrets)
# Проверяем наличие пароля в secrets, иначе используем значение по умолчанию
try:
    APP_PASSWORD = st.secrets["password"]
except Exception:
    # Для локальной разработки используем пароль по умолчанию
    APP_PASSWORD = ""

# Функция проверки пароля
def check_password():
    """Проверяет введенный пароль и обновляет статус аутентификации"""
    if hmac.compare_digest(st.session_state.password, APP_PASSWORD):
        st.session_state.auth_status = "verified"
    else:
        st.session_state.auth_status = "incorrect"
        # st.session_state.password = APP_PASSWORD

# Функция отображения формы входа
def login_prompt():
    """Отображает форму для ввода пароля"""
    # Удаляем стандартный заголовок страницы
    
    # Создаем контейнер с центрированной формой
    with st.container():
        # Создаем колонки для центрирования формы
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Стилизованный контейнер для формы логина
            st.markdown("""
            <div style="padding: 30px; border-radius: 12px; border: 1px solid #e6e6e6; 
                        margin-top: 50px; box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1); 
                        background-color: white;">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #2c3e50; font-size: 28px; margin-bottom: 5px;">🦷 Zahnarztpraxis</h1>
                    <p style="color: #7f8c8d; font-size: 16px;">Bitte melden Sie sich an, um fortzufahren</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Добавляем декоративную линию-разделитель
            st.markdown("""
            <div style="border-bottom: 1px solid #eaeaea; margin-bottom: 25px;"></div>
            """, unsafe_allow_html=True)
            
            # Форма входа
            with st.form("login_form"):
                st.text_input(
                    "Passwort", 
                    type="password", 
                    key="password",
                    help="Geben Sie das Passwort ein, um auf das System zuzugreifen"
                )
                
                # Стилизованная кнопка входа со светло-зеленым цветом
                submit = st.form_submit_button(
                    "Anmelden", 
                    use_container_width=True,
                    type="primary"
                )
                
                # Применяем пользовательский стиль для кнопки
                st.markdown("""
                <style>
                    .stButton button[data-testid="FormSubmitButton"] {
                        background-color: #4CAF50 !important;
                        color: white !important;
                        border: none !important;
                    }
                    .stButton button[data-testid="FormSubmitButton"]:hover {
                        background-color: #45a049 !important;
                        color: white !important;
                    }
                </style>
                """, unsafe_allow_html=True)
                
                if submit:
                    check_password()
                    st.rerun()  # Перезагрузка страницы после проверки пароля
            
            # Отображение ошибки при неверном пароле
            if st.session_state.auth_status == "incorrect":
                st.error("❌ Falsches Passwort. Bitte versuchen Sie es erneut.")
            
            # Закрывающий тег для контейнера
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Добавляем информацию о версии и копирайт внизу
            st.markdown("""
            <div style="text-align: center; margin-top: 20px; color: #95a5a6; font-size: 12px;">
                <p>Version 1.0.0 © 2024 Dental System</p>
            </div>
            """, unsafe_allow_html=True)

# Функция выхода из системы
def logout():
    """Сбрасывает статус авторизации"""
    st.session_state.auth_status = "unverified"
    st.rerun()

# Проверка авторизации перед отображением основного контента
if st.session_state.auth_status != "verified":
    login_prompt()
    st.stop()  # Останавливаем выполнение, если пользователь не авторизован

# Заголовок приложения
col1, col2 = st.columns([5, 1])
with col1:
    st.title("🦷 Zahnarztpraxis System")
with col2:
    st.button("Abmelden", on_click=logout, key="logout_button")

# Настройка Airtable
try:
    # Пытаемся получить API ключи из secrets
    AIRTABLE_API_KEY = st.secrets["airtable_api_key"]
    AIRTABLE_BASE_ID = st.secrets["airtable_base_id"]
    # Пытаемся получить ключ OpenAI из secrets
    OPENAI_API_KEY = st.secrets["openai_api_key"]
    openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
except Exception:
    # Выводим предупреждение в режиме разработки
    if os.environ.get("STREAMLIT_ENV") == "development":
        print("Внимание: Используются значения API по умолчанию. В продакшене используйте secrets.")

# Инициализация Airtable API
airtable = Api(AIRTABLE_API_KEY)

# Функция для получения промпта для транскрипции из Airtable
def get_transcription_prompt():
    """Retrieves the transcription prompt from Airtable or templates.yaml file, or returns a default prompt."""
    # Default prompt in case retrieval fails
    default_prompt = """
    Das ist eine Aufnahme eines Gesprächs in einer Zahnarztpraxis. Die Aufnahme kann zahnärztliche Verfahren, Diagnosen, Anamnesen und zahnmedizinische Terminologie enthalten. Bitte transkribieren Sie den Inhalt so genau wie möglich, mit besonderem Fokus auf zahnmedizinische Fachbegriffe und Verfahren, Zahnnummern, Materialien, Diagnosen und Anweisungen an den Patienten.
    """
    
    try:
        # Try to get the template from templates.yaml first
        templates_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                     "prompts", "templates.yaml")
        
        # Check if file exists
        if os.path.exists(templates_file):
            with open(templates_file, 'r', encoding='utf-8') as file:
                templates = yaml.safe_load(file)
                if templates and 'transcription' in templates:
                    print(f"Loaded transcription prompt from templates.yaml")
                    return templates['transcription']
        
        # If template not found in yaml file, try Airtable
        if AIRTABLE_API_KEY and AIRTABLE_BASE_ID:
            try:
                table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, "Prompts")
                records = table.all(formula="FIND('transcription', LOWER({category}))>0")
                
                if records and len(records) > 0 and 'fields' in records[0] and 'template_content' in records[0]['fields']:
                    prompt = records[0]['fields']['template_content']
                    print(f"Loaded transcription prompt from Airtable")
                    return prompt
            except Exception as e:
                print(f"Error fetching transcription prompt from Airtable: {e}")
    except Exception as e:
        print(f"Error loading transcription prompt: {e}")
    
    print(f"Using default transcription prompt")
    return default_prompt



def split_audio_into_chunks(uploaded_file, chunk_duration_sec=90):
    """
    Разбивает Streamlit UploadedFile (audio/wav) на чанки по chunk_duration_sec секунд.
    Возвращает список байтовых объектов (каждый — валидный WAV-файл).
    """
    # Универсально: если это bytes — обернуть в BytesIO, если file-like — использовать напрямую
    if hasattr(uploaded_file, "seek"):
        uploaded_file.seek(0)
        wav_source = uploaded_file
    else:
        wav_source = BytesIO(uploaded_file)
    with wave.open(wav_source, 'rb') as wf:
        params = wf.getparams()
        framerate = wf.getframerate()
        sampwidth = wf.getsampwidth()
        nchannels = wf.getnchannels()
        total_frames = wf.getnframes()
        chunk_frames = int(chunk_duration_sec * framerate)
        chunks = []
        for start in range(0, total_frames, chunk_frames):
            wf.setpos(start)
            frames = wf.readframes(min(chunk_frames, total_frames - start))
            out_buf = BytesIO()
            with wave.open(out_buf, 'wb') as out_wf:
                out_wf.setnchannels(nchannels)
                out_wf.setsampwidth(sampwidth)
                out_wf.setframerate(framerate)
                out_wf.writeframes(frames)
            out_buf.seek(0)
            chunks.append(out_buf.read())
    return chunks

def transcribe_audio_with_openai(audio_file):
    """
    Транскрибирует аудио с использованием модели Whisper от OpenAI.

    :param audio_bytes: Аудиоданные в байтах.
    :return: Текст транскрипции.
    """
    try:
        # Разбиваем аудио на чанки
        # Преобразуем UploadedFile в байты, если нужно
        if hasattr(audio_file, 'read'):
            audio_bytes = audio_file.read()
        else:
            audio_bytes = audio_file
            
        chunks = split_audio_into_chunks(audio_bytes)
        
        all_transcriptions = []
        for i, chunk in enumerate(chunks):
            print(f"Transcribing chunk {i+1}/{len(chunks)}")
            
            # Экспортируем чанк в байты
            # chunk_io = BytesIO()
            # chunk.export(chunk_io, format="mp3")  # Используем формат MP3 для уменьшения размера
            # chunk_data = chunk_io.getvalue()
            
            # Формируем промпт с учетом предыдущего контекста
            current_prompt = """
        Das ist eine Aufnahme eines Gesprächs in einer Zahnarztpraxis. Die Aufnahme kann zahnärztliche Verfahren, Diagnosen, Anamnesen und zahnmedizinische Terminologie    enthalten. Bitte transkribieren Sie den Inhalt so genau wie möglich, mit besonderem Fokus auf zahnmedizinische Fachbegriffe und Verfahren, Zahnnummern, Materialien, Diagnosen und Anweisungen an den Patienten.
             """
            if i > 0 and all_transcriptions:
                # Добавляем последние 100 символов предыдущей транскрипции как контекст
                last_text = '[chunk]'.join(all_transcriptions)
                current_prompt += f"\n\nVorheriger Kontext: {last_text}"
            
            # Транскрибируем чанк
            transcription = openai_client.audio.transcriptions.create(
                model="gpt-4o-transcribe",
                # file=("audio.mp3", chunk),
                file=("audio.wav", BytesIO(chunk)),
                prompt=current_prompt,
                language="de"
            )
            all_transcriptions.append(transcription.text)
        
        # Объединяем все транскрипции
        result = " ".join(all_transcriptions)
        
        print(f"Transcription length: {len(result)}")
        if len(result) > 100:
            print(f"Transcription beginning: {result[:100]}...")
        else:
            print(f"Transcription: {result}")
        
        return result
    except Exception as e:
        import traceback
        print(f"Error during transcription: {e}")
        print(traceback.format_exc())  # Выводим полный стек ошибки для отладки
        return f"Fehler bei der Transkription: {str(e)}"

# Пример использования
# audio_bytes = ... # Ваши аудиоданные в байтах

# Результат транскрипции
# transcription_result = transcribe_audio_with_openai(audio_bytes)

# Функции для работы с Airtable
def get_doctors():
    """Получает список докторов из Airtable"""
    try:
        table = airtable.table(AIRTABLE_BASE_ID, "Doctors")
        records = table.all()
        
        doctors = []
        for record in records:
            # Проверяем, есть ли поле fields и необходимые данные
            if "fields" in record:
                doctors.append({
                    "id": record["fields"].get("doctorId", ""),
                    "name": record["fields"].get("name", "Без имени"),
                    "specialization": record["fields"].get("specialization", "")
                })
        
        print(f"Загружено {len(doctors)} докторов")
        return pd.DataFrame(doctors)
    except Exception as e:
        print(f"Ошибка при получении списка докторов: {str(e)}")
        # Возвращаем пустой DataFrame с правильной структурой
        return pd.DataFrame(columns=["id", "name", "specialization"])

def get_patients():
    """Получает список пациентов из Airtable"""
    try:
        table = airtable.table(AIRTABLE_BASE_ID, "Patients")
        records = table.all()
        
        patients = []
        for record in records:
            # Проверяем, есть ли поле fields и необходимые данные
            if "fields" in record:
                # ID пациента хранится как число в Airtable
                patient_id = record["fields"].get("patientId")
                patients.append({
                    "id": patient_id,
                    "patient_code": patient_id  # ID пациента как число
                })
        
        print(f"Загружено {len(patients)} пациентов")
        return pd.DataFrame(patients)
    except Exception as e:
        print(f"Ошибка при получении списка пациентов: {str(e)}")
        # Возвращаем пустой DataFrame с правильной структурой
        return pd.DataFrame(columns=["id", "patient_code"])

def create_patient(patient_code=None):
    """Создает нового пациента в Airtable используя порядковые номера"""
    table = airtable.table(AIRTABLE_BASE_ID, "Patients")
    
    # Получаем текущий максимальный ID пациента
    patients_df = get_patients()
    
    # Если номер пациента не указан, генерируем порядковый номер
    if not patient_code:
        # Находим максимальный номер пациента из существующих ID
        if not patients_df.empty:
            # Преобразуем строковые ID в числа, игнорируя нечисловые
            patient_ids = []
            for pid in patients_df["id"]:
                try:
                    if isinstance(pid, (str, int)) and str(pid).isdigit():
                        patient_ids.append(int(pid))
                except:
                    pass
            
            if patient_ids:
                next_num = max(patient_ids) + 1
            else:
                next_num = 1
        else:
            next_num = 1
        
        # Используем простой порядковый номер как число
        patient_code = next_num
    else:
        # Если код передан как строка, преобразуем его в число
        try:
            patient_code = int(patient_code)
        except ValueError:
            return {
                "success": False,
                "error": "Patienten-ID muss eine Zahl sein"
            }
    
    # Данные для создания записи
    patient_data = {
        "patientId": patient_code,  # Числовой ID
        "createdAt": datetime.now().strftime("%Y-%m-%d")
    }
    
    try:
        # Создаем запись в Airtable
        record = table.create(patient_data)
        
        return {
            "success": True,
            "patientId": patient_code,
            "record_id": record["id"]
        }
    except Exception as e:
        print(f"Fehler beim Erstellen des Patienten: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

def get_procedures():
    """Получает список процедур из Airtable"""
    table = airtable.table(AIRTABLE_BASE_ID, "Procedures")
    records = table.all()
    
    procedures = []
    for record in records:
        procedures.append({
            "id": record["fields"].get("procedureId"),
            "category": record["fields"].get("category"),
            "name": record["fields"].get("name"),
            "description": record["fields"].get("description")
        })
    
    return pd.DataFrame(procedures)

def create_session(doctor_id, patient_id):
    """Создает новую сессию в Airtable"""
    try:
        # Отладочный вывод для проверки входных данных
        print(f"Создание сессии с параметрами: doctor_id={doctor_id}, patient_id={patient_id}")
        print(f"Типы данных: doctor_id={type(doctor_id)}, patient_id={type(patient_id)}")
        
        # Получаем таблицу Sessions
        sessions_table = airtable.table(AIRTABLE_BASE_ID, "Sessions")
        
        # Получаем запись доктора по doctorId
        doctors_table = airtable.table(AIRTABLE_BASE_ID, "Doctors")
        doctors = doctors_table.all(formula=f"{{doctorId}}='{doctor_id}'")
        
        if not doctors:
            return {
                "success": False,
                "message": f"Доктор с ID {doctor_id} не найден"
            }
        
        doctor_record_id = doctors[0]["id"]
        
        # Получаем запись пациента по patientId (учитываем, что это число)
        patients_table = airtable.table(AIRTABLE_BASE_ID, "Patients")
        
        # Формируем запрос в зависимости от типа patient_id
        if isinstance(patient_id, str) and patient_id.isdigit():
            # Если это строка с числом, преобразуем в число
            formula = f"{{patientId}}={int(patient_id)}"
        elif isinstance(patient_id, (int, float)):
            # Если это число, используем как есть
            formula = f"{{patientId}}={patient_id}"
        else:
            # В остальных случаях, используем как строку
            formula = f"{{patientId}}='{patient_id}'"
        
        patients = patients_table.all(formula=formula)
        
        if not patients:
            return {
                "success": False,
                "message": f"Пациент с ID {patient_id} не найден"
            }
        
        patient_record_id = patients[0]["id"]
        
        # Генерация уникального ID сессии
        session_id = f"S{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Подготовка данных для записи с использованием правильного формата для связей
        record_data = {
            "sessionId": session_id,  # Используем строковый идентификатор
            "date": datetime.now().strftime("%Y-%m-%d"),
            "doctorId": [doctor_record_id],  # Массив с ID записи доктора
            "patientId": [patient_record_id]  # Массив с ID записи пациента
        }
        
        print(f"Данные для создания записи: {record_data}")
        
        # Создание записи
        record = sessions_table.create(record_data)
        
        # Возвращаем успешный результат
        return {
            "success": True,
            "sessionId": session_id,
            "record_id": record["id"]
        }
    except Exception as e:
        print(f"Ошибка при создании сессии: {str(e)}")
        return {
            "success": False,
            "message": f"Ошибка при создании сессии: {str(e)}"
        }

def add_procedure_to_session(session_id, procedure_id, procedure_name):
    """Добавляет информацию о выбранной процедуре к сессии"""
    try:
        # Отладочный вывод для проверки входных данных
        print(f"Добавление процедуры: session_id={session_id}, procedure_id={procedure_id}")
        
        # Получаем запись сеанса по sessionId
        sessions_table = airtable.table(AIRTABLE_BASE_ID, "Sessions")
        session_records = sessions_table.all(formula=match({"sessionId": session_id}))
        
        if not session_records:
            return {
                "success": False,
                "message": f"Сессия с ID {session_id} не найдена"
            }
        
        session_record = session_records[0]
        
        # Получаем запись процедуры по procedureId
        procedures_table = airtable.table(AIRTABLE_BASE_ID, "Procedures")
        
        # ID процедуры всегда используем как строку
        formula = f"{{procedureId}}='{procedure_id}'"
        procedure_records = procedures_table.all(formula=formula)
        
        if not procedure_records:
            return {
                "success": False,
                "message": f"Процедура с ID {procedure_id} не найдена"
            }
        
        procedure_record_id = procedure_records[0]["id"]
        
        # Обновляем запись сессии, добавляя ID выбранной процедуры в формате массива
        sessions_table.update(
            session_record["id"], 
            {"procedureId": [procedure_record_id]}
        )
        
        return {
            "success": True,
            "sessionId": session_id,
            "procedureId": procedure_id
        }
    except Exception as e:
        print(f"Ошибка при добавлении процедуры к сессии: {str(e)}")
        return {
            "success": False,
            "message": f"Ошибка при добавлении процедуры к сессии: {str(e)}"
        }

def save_transcription(session_id, procedure_id, text):
    """Сохраняет транскрипцию в Airtable"""
    try:
        # Отладочный вывод для проверки входных данных
        print(f"Сохранение транскрипции: session_id={session_id}, procedure_id={procedure_id}")
        print(f"Типы данных: session_id={type(session_id)}, procedure_id={type(procedure_id)}")
        
        # Таблица транскрипций
        transcriptions_table = airtable.table(AIRTABLE_BASE_ID, "Transcriptions")
        
        # Получаем запись сеанса по sessionId
        sessions_table = airtable.table(AIRTABLE_BASE_ID, "Sessions")
        session_records = sessions_table.all(formula=match({"sessionId": session_id}))
        
        if not session_records:
            return {
                "success": False,
                "message": f"Сессия с ID {session_id} не найдена"
            }
        
        session_record_id = session_records[0]["id"]
        
        # Получаем запись процедуры по procedureId, если она указана
        procedure_record_id = None
        if procedure_id:
            procedures_table = airtable.table(AIRTABLE_BASE_ID, "Procedures")
            # ID процедуры всегда используем как строку
            formula = f"{{procedureId}}='{procedure_id}'"
            procedure_records = procedures_table.all(formula=formula)
            
            if procedure_records:
                procedure_record_id = procedure_records[0]["id"]
        
        # Генерация ID для транскрипции
        transcription_id = f"T{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Подготовка данных для записи
        record_data = {
            "transcriptionId": transcription_id,
            "sessionId": [session_record_id],  # Массив с ID записи сессии
            "text": text,
            "createdAt": datetime.now().strftime("%Y-%m-%d")
        }
        
        # Добавляем ссылку на процедуру, если она найдена
        if procedure_record_id:
            record_data["procedureId"] = [procedure_record_id]
                
        print(f"Данные для создания записи транскрипции: {record_data}")
        
        # Создание записи
        record = transcriptions_table.create(record_data)
        
        return {
            "success": True,
            "record_id": record["id"]
        }
    except Exception as e:
        print(f"Ошибка при сохранении транскрипции: {str(e)}")
        return {
            "success": False,
            "message": f"Ошибка при сохранении транскрипции: {str(e)}"
        }

# Функция для экспорта отчета в PDF
def create_download_button(text, button_text, file_name):
    """Создает кнопку для скачивания текста как файла"""
    # Конвертируем строку в base64
    b64 = base64.b64encode(text.encode()).decode()
    
    # Создаем HTML кнопку
    button_html = f'''
    <a href="data:file/txt;base64,{b64}" download="{file_name}" target="_blank">
        <button style="background-color: #4CAF50; color: white; padding: 12px 20px; 
        border: none; border-radius: 4px; cursor: pointer; font-size: 16px; width: 100%;">
            {button_text} 📥
        </button>
    </a>
    '''
    return button_html

# Инициализация состояния сессии
if 'step' not in st.session_state:
    st.session_state.step = 'input_data'
if 'doctor_id' not in st.session_state:
    st.session_state.doctor_id = ''
if 'doctor_name' not in st.session_state:
    st.session_state.doctor_name = ''
if 'patient_id' not in st.session_state:
    st.session_state.patient_id = ''
if 'session_id' not in st.session_state:
    st.session_state.session_id = ''
if 'selected_procedure' not in st.session_state:
    st.session_state.selected_procedure = None
if 'procedure_confirmed' not in st.session_state:  # Новое состояние для подтверждения процедуры
    st.session_state.procedure_confirmed = False
if 'audio_data' not in st.session_state:
    st.session_state.audio_data = None
if 'transcription' not in st.session_state:
    st.session_state.transcription = ""
if 'generated_report' not in st.session_state:  # Добавляем переменную для хранения отчета
    st.session_state.generated_report = None
if 'new_patient_mode' not in st.session_state:
    st.session_state.new_patient_mode = False
if 'new_patient_pending' not in st.session_state:
    st.session_state.new_patient_pending = False
if 'custom_patient_code' not in st.session_state:
    st.session_state.custom_patient_code = None
if 'show_table_info' not in st.session_state:
    st.session_state.show_table_info = False

# Функция для получения информации о структуре таблицы
def get_table_structure(table_name):
    """Получает структуру таблицы Airtable"""
    try:
        table = airtable.table(AIRTABLE_BASE_ID, table_name)
        records = table.all(max_records=1)
        
        if records:
            record = records[0]
            fields = record.get("fields", {})
            structure = {}
            
            for key, value in fields.items():
                structure[key] = {
                    "value": value,
                    "type": type(value).__name__
                }
                
            return {
                "success": True,
                "structure": structure
            }
        else:
            return {
                "success": False,
                "error": "Таблица пуста или не существует"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# Функции для навигации
def go_to_step(step):
    st.session_state.step = step
    st.rerun()

# Функция для переключения в режим добавления нового пациента
def toggle_new_patient_mode():
    st.session_state.new_patient_mode = not st.session_state.new_patient_mode
    st.rerun()

# Шаг 1: Ввод данных врача и пациента
if st.session_state.step == 'input_data':
    st.subheader("Eingabe der Daten")
    
    # Загрузка списков докторов и пациентов
    doctors_df = get_doctors()
    patients_df = get_patients()
    
    # Проверка наличия данных
    if doctors_df.empty:
        st.warning("⚠️ In der Datenbank wurden keine Ärzte gefunden. Bitte überprüfen Sie die Airtable-Konfiguration.")
        
    if patients_df.empty and not st.session_state.new_patient_mode:
        st.info("ℹ️ Es gibt keine Patienten in der Datenbank. Sie können einen neuen Patienten hinzufügen.")
    
    # Переключатель для добавления нового пациента (вне формы)
    new_patient_mode = st.checkbox("Neuer Patient", value=st.session_state.new_patient_mode, key="new_patient_checkbox")
    
    # Обновляем state и перезагружаем при изменении
    if new_patient_mode != st.session_state.new_patient_mode:
        st.session_state.new_patient_mode = new_patient_mode
        st.rerun()
    
    with st.form("patient_form"):
        # Выбор доктора из списка
        doctor_options = doctors_df["id"].tolist()
        doctor_id = st.selectbox(
            "Wählen Sie einen Arzt", 
            options=doctor_options,
            format_func=lambda x: f"{x} - {doctors_df[doctors_df['id'] == x]['name'].iloc[0] if not doctors_df[doctors_df['id'] == x].empty else 'Kein Name'}"
        ) if doctor_options else st.text_input("Arzt-ID")
        
        if st.session_state.new_patient_mode:
            # Форма для создания нового пациента (без имени)
            custom_patient_code = st.text_input(
                "Patienten-ID (optional)", 
                placeholder="Wenn nicht angegeben, wird automatisch generiert"
            )
            patient_id = None
        else:
            # Выбор пациента из списка
            patient_options = patients_df["id"].tolist()
            patient_id = st.selectbox(
                "Wählen Sie einen Patienten", 
                options=patient_options,
                format_func=lambda x: f"Patient #{x}" 
            ) if patient_options else None
            custom_patient_code = None
        
        submit_button = st.form_submit_button("Weiter")
        
        if submit_button:
            if doctor_id:
                # Сохраняем данные в состоянии сессии
                st.session_state.doctor_id = doctor_id
                if doctor_options:
                    st.session_state.doctor_name = doctors_df[doctors_df["id"] == doctor_id]["name"].values[0]
                
                # Обработка данных пациента
                if st.session_state.new_patient_mode:
                    # Сохраняем код пациента в сессии для создания после подтверждения
                    st.session_state.custom_patient_code = custom_patient_code
                    st.session_state.new_patient_pending = True
                    go_to_step('confirm_data')
                else:
                    # Выбор существующего пациента
                    if patient_id:
                        st.session_state.patient_id = patient_id
                        go_to_step('confirm_data')
                    else:
                        st.error("Bitte wählen Sie einen Patienten")
            else:
                st.error("Bitte wählen Sie einen Arzt")

# Шаг 2: Подтверждение данных
elif st.session_state.step == 'confirm_data':
    st.subheader("Datenbestätigung")
    
    st.info("Bitte überprüfen Sie die eingegebenen Daten:")
    
    st.write(f"**Arzt:** {st.session_state.doctor_name} (ID: {st.session_state.doctor_id})")
    
    # Отображаем информацию о новом пациенте или выбранном пациенте
    if hasattr(st.session_state, 'new_patient_pending') and st.session_state.new_patient_pending:
        patient_code_display = st.session_state.custom_patient_code if st.session_state.custom_patient_code else "Automatisch generierte ID"
        st.write(f"**Patient:** Neuer Patient ({patient_code_display})")
    else:
        st.write(f"**Patient:** #{st.session_state.patient_id}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Bestätigen"):
            # Если ожидается создание нового пациента, создаем его сейчас
            if hasattr(st.session_state, 'new_patient_pending') and st.session_state.new_patient_pending:
                response = create_patient(st.session_state.custom_patient_code)
                if response.get("success"):
                    # Сохраняем ID нового пациента
                    st.session_state.patient_id = response.get("patientId")
                    st.success(f"Neuer Patient mit ID #{response.get('patientId')} erstellt")
                    # Сбрасываем флаг ожидания создания
                    st.session_state.new_patient_pending = False
                    # Удаляем временные данные
                    if hasattr(st.session_state, 'custom_patient_code'):
                        del st.session_state.custom_patient_code
                else:
                    st.error(f"Fehler beim Erstellen des Patienten: {response.get('error', 'Unbekannter Fehler')}")
                    go_to_step('input_data')
                    st.stop()  # Останавливаем выполнение вместо return
            
            # Создание сессии напрямую через Airtable
            response = create_session(
                st.session_state.doctor_id,
                st.session_state.patient_id
            )
            
            if response.get("success"):
                st.session_state.session_id = response.get("sessionId")
                st.success("Daten erfolgreich gespeichert!")
                go_to_step('select_procedure')
            else:
                st.error(f"Fehler bei der Datenverarbeitung: {response.get('message', 'Unbekannter Fehler')}")
    
    with col2:
        if st.button("🔄 Bearbeiten"):
            # Сбрасываем флаг ожидания создания пациента
            st.session_state.new_patient_pending = False
            go_to_step('input_data')

# Шаг 3: Выбор процедуры
elif st.session_state.step == 'select_procedure':
    st.subheader("Verfahrensauswahl")
    
    # Отображение информации о сессии
    st.info(f"""
    **Arzt:** {st.session_state.doctor_name} (ID: {st.session_state.doctor_id})
    **Patient:** #{st.session_state.patient_id}
    **Session ID:** {st.session_state.session_id}
    """)
    
    # Разделитель для отделения информации о сессии от выбора процедуры
    st.markdown("<hr/>", unsafe_allow_html=True)
    
    # Загрузка списка процедур
    procedures_df = get_procedures()
    
    # Фильтрация по категориям
    categories = procedures_df['category'].unique().tolist()
    
    # Создаем вкладки для категорий вместо выпадающего списка
    st.markdown("<h3 class='category-heading'>Wählen Sie eine Verfahrenskategorie</h3>", unsafe_allow_html=True)
    
    # Если категорий меньше 5, используем вкладки, иначе выпадающее меню
    if len(categories) <= 5:
        # Создаем вкладки для каждой категории
        selected_category = st.tabs(categories)
        
        # Для каждой вкладки отображаем процедуры соответствующей категории
        for i, category in enumerate(categories):
            with selected_category[i]:
                # Фильтрация процедур по выбранной категории
                filtered_procedures = procedures_df[procedures_df['category'] == category]
                
                if filtered_procedures.empty:
                    st.info(f"Keine verfügbaren Verfahren in der Kategorie '{category}'.")
                else:
                    # Преобразуем DataFrame в список словарей для удобства использования
                    procedures_list = filtered_procedures.to_dict('records')
                    
                    # Отображаем заголовок
                    st.markdown("### Wählen Sie ein Verfahren")
                    
                    # Создаем контейнер для списка процедур
                    for procedure in procedures_list:
                        # Создаем строку с процедурой и кнопкой справа
                        col1, col2 = st.columns([4, 1])
                        
                        with col1:
                            st.markdown(f"""
                            <div class="procedure-item">
                                <strong class="procedure-name">{procedure['name']}</strong>
                                <p class="procedure-description">
                                    {procedure['description'][:80]}{'...' if len(procedure['description']) > 80 else ''}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            # Кнопка выбора для каждой процедуры
                            if st.button("Wählen", key=f"select_{category}_{procedure['id']}", use_container_width=True):
                                st.session_state.selected_procedure = procedure
                                
                                # Добавление информации о процедуре к сессии
                                response = add_procedure_to_session(
                                    st.session_state.session_id,
                                    procedure['id'],
                                    procedure['name']
                                )
                                
                                if response.get("success"):
                                    st.success(f"Verfahren '{procedure['name']}' ausgewählt!")
                                    go_to_step('confirm_procedure')
                                else:
                                    st.error(f"Fehler bei der Verfahrensauswahl: {response.get('error', 'Unbekannter Fehler')}")
                        
                        # Добавляем экспандер с полным описанием
                        with st.expander("📋 Mehr Details zum Verfahren"):
                            st.markdown(f"""
                            <div class="procedure-details">
                                <h4>{procedure['name']}</h4>
                                <p>{procedure['description']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Добавляем небольшой отступ между процедурами
                        st.markdown("<div class='procedure-spacer'></div>", unsafe_allow_html=True)
    else:
        # Если категорий много, используем выпадающий список
        selected_category = st.selectbox("Wählen Sie eine Kategorie", categories)
        
        # Фильтрация процедур по выбранной категории
        filtered_procedures = procedures_df[procedures_df['category'] == selected_category]
        
        if not filtered_procedures.empty:
            # Преобразуем DataFrame в список словарей для удобства использования
            procedures_list = filtered_procedures.to_dict('records')
            
            # Отображаем заголовок
            st.markdown("### Wählen Sie ein Verfahren")
            
            # Создаем контейнер для списка процедур
            for procedure in procedures_list:
                # Создаем строку с процедурой и кнопкой справа
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class="procedure-item">
                        <strong class="procedure-name">{procedure['name']}</strong>
                        <p class="procedure-description">
                            {procedure['description'][:80]}{'...' if len(procedure['description']) > 80 else ''}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Кнопка выбора для каждой процедуры
                    if st.button("Wählen", key=f"select_{selected_category}_{procedure['id']}", use_container_width=True):
                        st.session_state.selected_procedure = procedure
                        
                        # Добавление информации о процедуре к сессии
                        response = add_procedure_to_session(
                            st.session_state.session_id,
                            procedure['id'],
                            procedure['name']
                        )
                        
                        if response.get("success"):
                            st.success(f"Verfahren '{procedure['name']}' ausgewählt!")
                            go_to_step('confirm_procedure')
                        else:
                            st.error(f"Fehler bei der Verfahrensauswahl: {response.get('error', 'Unbekannter Fehler')}")
                
                # Добавляем экспандер с полным описанием
                with st.expander("📋 Mehr Details zum Verfahren"):
                    st.markdown(f"""
                    <div class="procedure-details">
                        <h4>{procedure['name']}</h4>
                        <p>{procedure['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Добавляем небольшой отступ между процедурами
                st.markdown("<div class='procedure-spacer'></div>", unsafe_allow_html=True)
        else:
            st.info(f"Keine verfügbaren Verfahren in der Kategorie '{selected_category}'.")
    
    # Кнопка для возврата к предыдущему шагу
    st.markdown("<hr/>", unsafe_allow_html=True)  # Разделитель
    if st.button("⬅️ Zurück", use_container_width=True):
        go_to_step('confirm_data')

# Шаг 4: Подтверждение выбора процедуры
elif st.session_state.step == 'confirm_procedure':
    st.subheader("Bestätigung der Verfahrensauswahl")
    
    # Отображение информации о сессии
    st.info(f"""
    **Arzt:** {st.session_state.doctor_name} (ID: {st.session_state.doctor_id})
    **Patient:** #{st.session_state.patient_id}
    **Session ID:** {st.session_state.session_id}
    """)
    
    # Отображение информации о выбранной процедуре
    st.markdown("### Ausgewähltes Verfahren")
    
    # Создаем карточку с выбранной процедурой, используя CSS-класс
    st.markdown(f"""
    <div class="selected-procedure-card">
        <h3>{st.session_state.selected_procedure['name']}</h3>
        <p><strong>Kategorie:</strong> {st.session_state.selected_procedure['category']}</p>
        <p>{st.session_state.selected_procedure['description']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Кнопки для навигации
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("⬅️ Zurück zur Verfahrensauswahl"):
            go_to_step('select_procedure')
    
    with col2:
        if st.button("✅ Bestätigen und fortfahren", use_container_width=True):
            st.session_state.procedure_confirmed = True
            go_to_step('record_voice')

# Шаг 5: Запись голоса
elif st.session_state.step == 'record_voice':
    # Проверяем, была ли подтверждена процедура
    if not st.session_state.procedure_confirmed:
        st.warning("Zuerst müssen Sie die Verfahrensauswahl bestätigen")
        go_to_step('confirm_procedure')
    else:
        st.subheader("Sprachaufzeichnung")
        
        # Отображение информации о сессии
        st.info(f"""
        **Arzt:** {st.session_state.doctor_name} (ID: {st.session_state.doctor_id})
        **Patient:** #{st.session_state.patient_id}
        **Verfahren:** {st.session_state.selected_procedure['name']}
        """)
        
        # Запись аудио
        st.write("### Sprachaufzeichnung des Arztes")
        
        # Используем стандартный компонент Streamlit для записи аудио
        try:
            # Используем компонент st.audio_input для записи аудио
            audio_data = st.audio_input("Klicken Sie, um die Aufnahme zu starten")
            
            if audio_data is not None:
                # Сохраняем аудио данные в состояние сессии
                st.session_state.audio_data = audio_data
                
                # Отображаем записанное аудио
                st.audio(audio_data, format="audio/wav")
                
                # Кнопка для отправки аудио на транскрибацию
                if st.button("📝 Transkribieren"):
                    st.info("Audio wird zur Transkription gesendet...")
                    
                    with st.spinner("Transkription läuft..."):
                        # Используем OpenAI API для транскрипции
                        if not openai_client:
                            st.error("OpenAI API nicht konfiguriert. Bitte in den Einstellungen konfigurieren.")
                            st.session_state.transcription = "OpenAI API nicht konfiguriert. Beispieltext wird verwendet."
                        else:
                            try:
                                # Транскрибируем аудио через OpenAI API
                                transcription_result = transcribe_audio_with_openai(audio_data)
                                
                                if transcription_result.startswith("Ошибка:"):
                                    st.error(transcription_result)
                                    st.session_state.transcription = "Beispiel für transkribierten Text. In einem realen Projekt wird hier der vom Spracherkennungsmodell erhaltene Text stehen."
                                else:
                                    st.success("Transkription erfolgreich!")
                                    st.session_state.transcription = transcription_result
                            except Exception as e:
                                st.error(f"Fehler bei der Transkription: {str(e)}")
                                st.session_state.transcription = "Beispiel für transkribierten Text. In einem realen Projekt wird hier der vom Spracherkennungsmodell erhaltene Text stehen."
                    
                    # Переход к следующему шагу
                    go_to_step('show_transcription')
        except Exception as e:
            st.error(f"Fehler bei der Audioaufnahme: {str(e)}")
        
        # Кнопка для возврата к выбору процедуры
        if st.button("⬅️ Zurück zur Verfahrensauswahl"):
            go_to_step('select_procedure')

# Шаг 6: Отображение транскрибации
elif st.session_state.step == 'show_transcription':
    st.subheader("Transkriptionsergebnis")
    
    # Отображение информации о сессии
    st.info(f"""
    **Arzt:** {st.session_state.doctor_name} (ID: {st.session_state.doctor_id})
    **Patient:** #{st.session_state.patient_id}
    **Verfahren:** {st.session_state.selected_procedure['name']}
    """)
    
    # Отображение транскрибированного текста
    st.write("### Transkribierter Text")
    
    # Текстовое поле для редактирования транскрибации
    transcription = st.text_area(
        "Sie können den Text bei Bedarf bearbeiten:",
        value=st.session_state.transcription,
        height=200
    )
    
    # Генератор отчетов
    with st.expander("Bericht generieren", expanded=True):
        output_format = st.selectbox(
            "Ausgabeformat",
            options=['markdown', 'json'],
            format_func=lambda x: 'Markdown (lesbarer Text)' if x == 'markdown' else 'JSON (strukturierte Daten)'
        )
        
        if st.button("Bericht generieren"):
            if not transcription:
                st.error("Bitte geben Sie einen Transkriptionstext ein.")
            else:
                with st.spinner("Bericht wird generiert..."):
                    try:
                        # Подготовка данных о процедуре
                        procedure_info = {
                            "id": st.session_state.selected_procedure['id'],
                            "category": st.session_state.selected_procedure['category'],
                            "name": st.session_state.selected_procedure['name'],
                            "description": st.session_state.selected_procedure.get('description', '')
                        }
                        
                        # Генерация отчета только на немецком языке
                        report = generate_dental_report(
                            transcription=transcription,
                            category=procedure_info['category'],
                            procedure_name=procedure_info['name'],
                            procedure_info=procedure_info,
                            doctor_name=st.session_state.doctor_name
                        )
                        print(report)
                        
                        # Отображение результата
                        if output_format == 'markdown':
                            st.markdown(report)
                            
                            # Добавляем кнопки для скачивания отчета
                            st.markdown("### Bericht herunterladen")
                            
                            # Кнопка для скачивания в формате Markdown
                            md_filename = f"bericht_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                            st.markdown(create_download_button(report, "Als Markdown herunterladen", md_filename), unsafe_allow_html=True)
                            
                            # Кнопка для скачивания в формате JSON
                            json_filename = f"bericht_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                            st.markdown(create_download_button(json.dumps(report, ensure_ascii=False, indent=2), 
                                                              "Als JSON herunterladen", json_filename), unsafe_allow_html=True)
                        else:
                            st.json(report)
                            
                            # Кнопка для скачивания в формате JSON
                            json_filename = f"bericht_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                            st.markdown(create_download_button(json.dumps(report, ensure_ascii=False, indent=2), 
                                                              "Als JSON herunterladen", json_filename), unsafe_allow_html=True)
                        
                        # Сохраняем отчет в состоянии
                        st.session_state.generated_report = report
                        
                    except Exception as e:
                        st.error(f"Fehler bei der Berichtsgenerierung: {str(e)}")
    
    # Кнопки для навигации
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("⬅️ Zurück zur Aufnahme"):
            go_to_step('record_voice')
    
    with col2:
        if st.button("✅ Speichern und beenden"):
            # Сохранение транскрибации напрямую в Airtable
            response = save_transcription(
                st.session_state.session_id,
                st.session_state.selected_procedure['id'],
                transcription
            )
            
            if response.get("success"):
                st.success("Transkription erfolgreich gespeichert!")
                # Сброс состояния для новой сессии
                for key in ['doctor_id', 'doctor_name', 'patient_id', 'session_id', 
                           'selected_procedure', 'procedure_confirmed', 'audio_data', 
                           'transcription', 'generated_report']:
                    if key in st.session_state:
                        st.session_state[key] = '' if key in ['doctor_id', 'doctor_name', 'patient_id', 
                                                              'session_id', 'transcription'] else None
                go_to_step('input_data')
            else:
                st.error(f"Fehler beim Speichern der Transkription: {response.get('error', 'Unbekannter Fehler')}")

# Отображение текущего состояния (для отладки)
with st.expander("Debug-Informationen"):
    st.write("Aktueller Status:")
    debug_info = {
        "step": st.session_state.step,
        "doctor_id": st.session_state.doctor_id,
        "doctor_name": st.session_state.doctor_name,
        "patient_id": st.session_state.patient_id,
        "session_id": st.session_state.session_id,
        "selected_procedure": st.session_state.selected_procedure,
        "procedure_confirmed": st.session_state.procedure_confirmed,
        "has_audio_data": st.session_state.audio_data is not None,
        "transcription_length": len(st.session_state.transcription) if st.session_state.transcription else 0,
        "new_patient_mode": st.session_state.new_patient_mode,
        "new_patient_pending": st.session_state.new_patient_pending,
        "custom_patient_code": st.session_state.custom_patient_code,
        "openai_api_configured": openai_client is not None
    }
    st.json(debug_info)
    
    # Статус API ключей
    st.write("### API Status")
    api_status = {
        "airtable_api": bool(AIRTABLE_API_KEY),
        "openai_api": bool(OPENAI_API_KEY),
        "openai_client_initialized": openai_client is not None
    }
    st.json(api_status)
    
    # Отображение структуры таблиц
    st.write("### Airtable-Tabelleninformationen")
    show_table_info = st.checkbox("Tabellenstruktur anzeigen", value=st.session_state.show_table_info)
    st.session_state.show_table_info = show_table_info
    
    if show_table_info:
        tables = ["Doctors", "Patients", "Sessions", "Procedures", "Transcriptions"]
        
        for table_name in tables:
            st.write(f"#### Tabelle: {table_name}")
            result = get_table_structure(table_name)
            
            if result["success"]:
                st.json(result["structure"])
            else:
                st.error(f"Fehler beim Abrufen der Tabellenstruktur {table_name}: {result['error']}")


# end
                
                