from frontend.models.report_models import (
    EndodonticReport, 
    ZEEingliedernReport, 
    FillingPKVReport, 
    PaAtgMhuReport, 
    BefundaufnahmeReport, 
    ChirExtraktionReport,
    ImplantationReport,
    SchmerzbehandlungReport,
    OPGDVTReport,
    CMDReport,
    KFOReport,
    KinderReport
)

from frontend.models.reports import (
    format_endo_report,
    format_ze_eingliedern_report,
    format_filling_pkv_report,
    format_pa_atg_mhu_report,
    format_befundaufnahme_report,
    format_chir_extraktion_report,
    format_implantation_report,
    format_schmerzbehandlung_report,
    format_opg_dvt_report,
    format_cmd_report,
    format_kfo_report,
    format_kinder_report
)

import openai
import json
import streamlit as st
client = openai.Client(api_key=st.secrets["openai_api_key"])

# Словарь соответствий для типов отчетов, моделей и функций форматирования
REPORT_MAPPING = {
    "endo": {
        "model": EndodonticReport,
        "format_func": format_endo_report,
        "prompt": """
            # ENDODONTIC TREATMENT REPORT EXTRACTION WITH REASONS

            You are a dental assistant AI specialized in extracting precise information from transcriptions.
            
            ## TASK
            Extract ONLY information explicitly mentioned in the transcription and format it according to the EndodonticReport model.
            
            ## EXTRACTION RULES
            1. Extract ONLY information EXPLICITLY mentioned in the transcription
            2. Fix tooth number format (e.g., "2,6" to "26")
            3. For vitality tests, use the format "26, Kältespray, ++"
            4. For ISO sizes, write "020" (not "20")
            5. Use exactly the dental terminology and abbreviations from the transcription
            6. For each piece of information, provide the reason/citation from the transcription
            7. Multiple teeth may be mentioned - include all in treatment_area as a list
            8. Leave optional fields as null if not mentioned in the transcription
            9. Use the provided doctor name in the report: {doctor_name}
            Procedure type is: {procedure_name}.
            
            ## FORMAT OF RESPONSE
            Return a valid object that strictly conforms to the EndodonticReport model schema.
        """
    },
    "ze": {
        "model": ZEEingliedernReport,
        "format_func": format_ze_eingliedern_report,
        "prompt": """
            You are a dental assistant AI specialized in extracting precise information for a ZE-Eingliedern procedure.
            Only extract the information EXPLICITLY mentioned in the transcription. 
            Follow these rules:
            1. Extract ONLY info explicitly mentioned.
            2. Use FDI notation for teeth (e.g., "4.2" should be "42", "3.4.3" might not be valid, fix if obvious).
            3. Return a valid JSON object that strictly conforms to the ZEEingliedernReport schema, including reasoning fields.
            4. For each piece of data, add timing or textual citations from the transcription in the corresponding '..._reasoning' field.
            5. Leave optional fields as null if not mentioned.
            6. Carefully preserve German medical terms found in the text.
            Use the provided doctor name: {doctor_name}.
            Procedure type is: {procedure_name}.
        """
    },
    "fullungen": {
        "model": FillingPKVReport,
        "format_func": format_filling_pkv_report,
        "prompt": """
            You are a dental assistant AI specialized in extracting precise information from transcriptions.

            ## TASK
            Extract ONLY information EXPLICITLY mentioned in the transcription and format it according to the model.

            ## EXTRACTION RULES
            1. Extract ONLY information EXPLICITLY mentioned in the transcription
            2. Fix tooth number format (e.g., "2,6" to "26") using FDI notation if possible
            3. For vitality tests, use the format "26, Kältespray, ++" if relevant (though not always needed in fillings)
            4. For ISO sizes, write "020" (not "20") if endodontic references appear
            5. Use exactly the dental terminology and abbreviations from the transcription
            6. For each piece of information, provide the reason/citation from the transcription
            7. Multiple teeth may be mentioned - include all in treatment_area as a list
            8. Leave optional fields as null if not mentioned in the transcription

            Use the provided doctor name in the report: {doctor_name}
            Procedure type is: {procedure_name}.

            ## FORMAT OF RESPONSE
            Return a valid JSON object that strictly conforms to the FillingPKVReport model schema.
        """
    },
    "pa_pzr": {
        "model": PaAtgMhuReport,
        "format_func": format_pa_atg_mhu_report,
        "prompt": """
            You are a specialized AI assistant for dentists, extracting information from German transcripts.
            
            ## YOUR TASK
            Extract ONLY information EXPLICITLY mentioned in the transcript and structure it according to the 'PaAtgMhuReport' model.
            
            ## EXTRACTION RULES
            1. Extract only information explicitly mentioned in the transcript.
            2. If tooth numbers are mentioned, format them according to FDI schema (e.g., 2,6 -> 26).
            3. For findings or specifications (if relevant) use original terminology from the transcript.
            4. For all fields, add supporting evidence from the transcript where available (e.g., field_reasoning).
            5. If a field is not mentioned in the transcript, set it to null.
            6. Use the provided doctor name: {doctor_name}.
            
            Procedure type is: {procedure_name}.
            
            ## MODEL FORMAT
            Return the result strictly as JSON, valid for the Pydantic model 'PaAtgMhuReport'.
        """
    },
    "befundaufnahme": {
        "model": BefundaufnahmeReport,
        "format_func": format_befundaufnahme_report,
        "prompt": """
            You are a dental assistant AI specialized in extracting precise information from transcriptions.
            
            ## TASK
            Extract ONLY information explicitly mentioned in the transcription and format it according to the model.
            
            ## EXTRACTION RULES
            1. Extract ONLY information EXPLICITLY mentioned in the transcription
            2. Fix tooth number format (e.g., "2,6" to "26")
            3. For vitality tests, use the format "26, Kältespray, ++"
            4. For ISO sizes, write "020" (not "20")
            5. Use exactly the dental terminology and abbreviations from the transcription
            6. For each piece of information, provide the reason/citation from the transcription
            7. Multiple teeth may be mentioned - include all in tooth_findings if relevant
            8. Leave optional fields as null if not mentioned in the transcription
            
            Use the provided doctor name in the report: {doctor_name}
            Procedure type is: {procedure_name}.
                
            ## FORMAT OF RESPONSE
            Return a valid object that strictly conforms to the BefundaufnahmeReport model schema.
        """
    },
    "chirurgie": {
        "model": ChirExtraktionReport,
        "format_func": format_chir_extraktion_report,
        "prompt": """
            You are an AI assistant for dentists, specialized in 'Chir Extraktion' (surgical extraction).
            
            ## TASK
            1. Extract only information EXPLICITLY mentioned in the transcript.
            2. Summarize the data in the ChirExtraktionReport schema.
            3. Pay attention to FDI tooth designations (e.g., "3,6" -> "36").
            4. For indications, procedures, etc., use the original terms from the transcript (German terminology).
            5. For each field, use quotes from the transcript under 'reasoning' where possible.
            6. Optional fields remain null if not mentioned.
            7. Use the procedure_name for procedure_type: {procedure_name}.
            8. Use the doctor_name parameter as the doctor's name: {doctor_name}.
            
            ## FORMAT OF RESPONSE
            Create ONLY a JSON that strictly adheres to this schema.
        """
    },
    "implantation": {
        "model": ImplantationReport,
        "format_func": format_implantation_report,
        "prompt": """
            You are a dental assistant AI specialized in extracting precise information from dental implantation transcriptions.
            
            ## TASK
            Extract ONLY information explicitly mentioned in the transcription and format it according to the ImplantationReport model.
            
            ## EXTRACTION RULES
            1. Extract ONLY information EXPLICITLY mentioned in the transcription
            2. Fix tooth number format (e.g., "2,6" to "26")
            3. Use exactly the dental terminology and abbreviations from the transcription
            4. For each piece of information, provide the reason/citation from the transcription in the corresponding reasoning field
            5. Pay special attention to implant system details, bone quality/quantity, and surgical procedure
            6. Multiple implant positions may be mentioned - include all if relevant
            7. Leave optional fields as null if not mentioned in the transcription
            
            Use the provided doctor name in the report: {doctor_name}
            Procedure type is: {procedure_name}.
                
            ## FORMAT OF RESPONSE
            Return a valid object that strictly conforms to the ImplantationReport model schema.
        """
    },
    "schmerzbehandlung": {
        "model": SchmerzbehandlungReport,
        "format_func": format_schmerzbehandlung_report,
        "prompt": """
            You are a dental assistant AI specialized in extracting precise information about dental pain management.
            
            ## TASK
            Extract ONLY information explicitly mentioned in the transcription and format it according to the SchmerzbehandlungReport model.
            
            ## EXTRACTION RULES
            1. Extract ONLY information EXPLICITLY mentioned in the transcription
            2. Fix tooth number format (e.g., "2,6" to "26")
            3. Capture all details about pain characteristics, triggers, duration, and clinical examination
            4. For sensitivity tests, use the format similar to "26, Kältespray, ++"
            5. Document any emergency treatment procedures performed
            6. Use exactly the dental terminology and abbreviations from the transcription
            7. For each piece of information, provide the reason/citation from the transcription
            8. Leave optional fields as null if not mentioned in the transcription
            
            Use the provided doctor name in the report: {doctor_name}
            Procedure type is: {procedure_name}.
                
            ## FORMAT OF RESPONSE
            Return a valid object that strictly conforms to the SchmerzbehandlungReport model schema.
        """
    },
    "opg_dvt": {
        "model": OPGDVTReport,
        "format_func": format_opg_dvt_report,
        "prompt": """
            You are a dental assistant AI specialized in extracting precise information about radiographic diagnostics.
            
            ## TASK
            Extract ONLY information explicitly mentioned in the transcription and format it according to the OPGDVTReport model.
            
            ## EXTRACTION RULES
            1. Extract ONLY information EXPLICITLY mentioned in the transcription
            2. Fix tooth number format (e.g., "2,6" to "26")
            3. Capture technical details of imaging if mentioned (device, settings)
            4. Document all findings mentioned about dental status, bone structures, TMJ, sinuses, and pathological changes
            5. Note any interpretation, diagnosis, or recommendations based on the radiographic findings
            6. Use exactly the dental terminology and abbreviations from the transcription
            7. For each piece of information, provide the reason/citation from the transcription
            8. Leave optional fields as null if not mentioned in the transcription
            
            Use the provided doctor name in the report: {doctor_name}
            Procedure type is: {procedure_name}.
                
            ## FORMAT OF RESPONSE
            Return a valid object that strictly conforms to the OPGDVTReport model schema.
        """
    },
    "cmd": {
        "model": CMDReport,
        "format_func": format_cmd_report,
        "prompt": """
            You are a dental assistant AI specialized in extracting precise information about CMD diagnostics and therapy.
            
            ## TASK
            Extract ONLY information explicitly mentioned in the transcription and format it according to the CMDReport model.
            
            ## EXTRACTION RULES
            1. Extract ONLY information EXPLICITLY mentioned in the transcription
            2. Capture all details about main complaints, pain characteristics, and functional limitations
            3. Document examination findings about TMJ, movement, muscles, and occlusion
            4. Note any instrumental analysis, imaging diagnostics, and therapy approaches mentioned
            5. Use exactly the dental terminology and abbreviations from the transcription
            6. For each piece of information, provide the reason/citation from the transcription
            7. Leave optional fields as null if not mentioned in the transcription
            
            Use the provided doctor name in the report: {doctor_name}
            Procedure type is: {procedure_name}.
                
            ## FORMAT OF RESPONSE
            Return a valid object that strictly conforms to the CMDReport model schema.
        """
    },
    "kfo": {
        "model": KFOReport,
        "format_func": format_kfo_report,
        "prompt": """
            You are a dental assistant AI specialized in extracting precise information about orthodontic treatment.
            
            ## TASK
            Extract ONLY information explicitly mentioned in the transcription and format it according to the KFOReport model.
            
            ## EXTRACTION RULES
            1. Extract ONLY information EXPLICITLY mentioned in the transcription
            2. Fix tooth number format (e.g., "2,6" to "26")
            3. Capture details about patient age, growth phase, and all diagnostic findings
            4. Document Angle class, skeletal classification, and specific anomalies if mentioned
            5. Note treatment goals, appliance type, and estimated duration
            6. Record implemented measures and patient compliance
            7. Use exactly the orthodontic terminology and abbreviations from the transcription
            8. For each piece of information, provide the reason/citation from the transcription
            9. Leave optional fields as null if not mentioned in the transcription
            
            Use the provided doctor name in the report: {doctor_name}
            Procedure type is: {procedure_name}.
                
            ## FORMAT OF RESPONSE
            Return a valid object that strictly conforms to the KFOReport model schema.
        """
    },
    "kinder": {
        "model": KinderReport,
        "format_func": format_kinder_report,
        "prompt": """
            You are a dental assistant AI specialized in extracting precise information about pediatric dentistry.
            
            ## TASK
            Extract ONLY information explicitly mentioned in the transcription and format it according to the KinderReport model.
            
            ## EXTRACTION RULES
            1. Extract ONLY information EXPLICITLY mentioned in the transcription
            2. Fix tooth number format (e.g., "2,6" to "26"), accounting for both permanent and primary teeth
            3. Capture details about child's age, cooperation level, and dental status
            4. Document behavior management techniques, special techniques, and materials used
            5. Note preventive measures and recommendations given to parents/caregivers
            6. Use exactly the pediatric dental terminology and abbreviations from the transcription
            7. For each piece of information, provide the reason/citation from the transcription
            8. Leave optional fields as null if not mentioned in the transcription
            
            Use the provided doctor name in the report: {doctor_name}
            Procedure type is: {procedure_name}.
                
            ## FORMAT OF RESPONSE
            Return a valid object that strictly conforms to the KinderReport model schema.
        """
    }
}

def process_dental_transcription_universal(
    transcription: str,
    procedure_name: str,
    doctor_name: str,
    procedure_description: str,
    report_type: str = None,
    model: str = "gpt-4o",
    client = client
):
    """
    Универсальная функция для обработки стоматологической транскрипции и создания отчета.
    
    Args:
        transcription (str): Текст транскрипции
        procedure_name (str): Название процедуры
        doctor_name (str): Имя врача
        procedure_description (str): Описание процедуры
        report_type (str, optional): Тип отчета (ключ из REPORT_MAPPING). Если не указан, 
                                    будет определен автоматически на основе procedure_name
        model (str, optional): Модель LLM для использования. По умолчанию "gpt-4o"
        client: Клиент API для запросов к LLM
        
    Returns:
        tuple: (formatted_report, report_object)
    """
    
    # Если тип отчета не указан, определим его на основе procedure_name
    if report_type is None:
        # Простое сопоставление по ключевым словам в названии процедуры
        if "endo" in procedure_name.lower():
            report_type = "endo"
        elif "ze" in procedure_name.lower() or "eingliedern" in procedure_name.lower():
            report_type = "ze"
        elif "füll" in procedure_name.lower() or "füllung" in procedure_name.lower() or "pkv" in procedure_name.lower():
            report_type = "fullungen"
        elif "pa" in procedure_name.lower() or "atg" in procedure_name.lower() or "mhu" in procedure_name.lower():
            report_type = "pa_pzr"
        elif "befund" in procedure_name.lower() or "01" in procedure_name:
            report_type = "befundaufnahme"
        elif "chir" in procedure_name.lower() or "extraktion" in procedure_name.lower():
            report_type = "chirurgie"
        elif "implant" in procedure_name.lower():
            report_type = "implantation"
        elif "schmerz" in procedure_name.lower():
            report_type = "schmerzbehandlung"
        elif "opg" in procedure_name.lower() or "dvt" in procedure_name.lower() or "röntgen" in procedure_name.lower():
            report_type = "opg_dvt"
        elif "cmd" in procedure_name.lower():
            report_type = "cmd"
        elif "kfo" in procedure_name.lower() or "ortho" in procedure_name.lower():
            report_type = "kfo"
        elif "kind" in procedure_name.lower() or "päd" in procedure_name.lower():
            report_type = "kinder"
        else:
            # По умолчанию используем endo, но лучше бросить исключение или запросить у пользователя
            report_type = "endo"
    
    # Проверяем, что такой тип отчета поддерживается
    if report_type not in REPORT_MAPPING:
        raise ValueError(f"Unsupported report type: {report_type}")
    
    # Получаем информацию о модели и функции форматирования
    report_info = REPORT_MAPPING[report_type]
    
    # Форматируем prompt, подставляя необходимые параметры
    system_prompt = report_info["prompt"].format(
        doctor_name=doctor_name,
        procedure_name=procedure_name
    )
    
    # Формируем user message
    user_message = f"""
    Verfahren: {procedure_name}
    {procedure_description}
    
    Transkription:
    {transcription}
    """
    
    # Делаем запрос к API
    response = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        response_format=report_info["model"],
        temperature=0,
        seed=42
    )
    
    # Извлекаем отчет из ответа
    report = response.choices[0].message.parsed
    
    # Форматируем отчет с помощью соответствующей функции
    formatted_report = report_info["format_func"](report)
    
    return formatted_report, report
