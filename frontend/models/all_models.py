from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class BaseReport(BaseModel):
    """Базовая модель для всех отчетов о стоматологических процедурах"""
    
    title: str = Field(
        description="Название процедуры"
    )
    
    aufklarung: List[str] = Field(
        description="Информирование пациента, анамнез, жалобы. Список строк, каждая строка - отдельный пункт."
    )
    
    befund: List[str] = Field(
        description="Результаты обследования, диагностики. Список строк, каждая строка - отдельный пункт."
    )
    
    verwendete_materialien: List[str] = Field(
        description="Использованные материалы и инструменты. Список строк, каждая строка - отдельный пункт."
    )
    
    durchfuhrung: List[str] = Field(
        description="Описание проведенной процедуры. Список строк, каждая строка - отдельный пункт."
    )
    
    therapieplanung: List[str] = Field(
        description="План дальнейшего лечения и рекомендации. Список строк, каждая строка - отдельный пункт."
    )
    
    sonstiges: Optional[List[str]] = Field(
        None,
        description="Дополнительная информация. Список строк, каждая строка - отдельный пункт."
    )
    
    nachster_termin: Optional[List[str]] = Field(
        None,
        description="Информация о следующем визите. Список строк, каждая строка - отдельный пункт."
    )


class EndoReport(BaseReport):
    """Модель для отчетов об эндодонтических процедурах"""
    
    zahnnummer: str = Field(
        description="Номер зуба по международной классификации"
    )
    
    kanalanzahl: Optional[str] = Field(
        None,
        description="Количество обнаруженных каналов"
    )
    
    arbeitslange: Optional[Dict[str, str]] = Field(
        None,
        description="Рабочая длина каждого канала. Ключ - название канала (например, MB, DB), значение - длина в мм"
    )
    
    masterfile: Optional[Dict[str, str]] = Field(
        None,
        description="Размер мастер-файла для каждого канала. Ключ - название канала, значение - размер файла"
    )
    
    aufbereitungstechnik: Optional[str] = Field(
        None,
        description="Техника обработки каналов"
    )
    
    spulprotokoll: Optional[List[str]] = Field(
        None,
        description="Протокол ирригации. Список используемых растворов и последовательность их применения"
    )
    
    obturation: Optional[Dict[str, str]] = Field(
        None,
        description="Данные об обтурации каналов. Ключ - название канала, значение - метод/материал обтурации"
    )
    
    provisorische_versorgung: Optional[str] = Field(
        None,
        description="Временная реставрация зуба после эндодонтического лечения"
    )
    
    rontgenkontrolle: Optional[str] = Field(
        None,
        description="Информация о рентгенологическом контроле"
    )


class PaPzrReport(BaseReport):
    """Модель для отчетов о пародонтологических процедурах и профессиональной гигиене"""
    
    parodontalstatus: Optional[Dict[str, str]] = Field(
        None,
        description="Пародонтальный статус. Ключи могут быть номерами зубов или квадрантами, значения - описания"
    )
    
    indizes: Optional[Dict[str, str]] = Field(
        None,
        description="Индексы оценки состояния пародонта (PSI, API, SBI и др.). Ключ - название индекса, значение - показатель"
    )
    
    taschentiefen: Optional[Dict[str, str]] = Field(
        None,
        description="Глубина пародонтальных карманов. Ключ - зуб/область, значение - глубина в мм"
    )
    
    bluten_bei_sondierung: Optional[str] = Field(
        None,
        description="Кровоточивость при зондировании (в %)"
    )
    
    lockerungsgrad: Optional[Dict[str, str]] = Field(
        None,
        description="Степень подвижности зубов. Ключ - зуб, значение - степень подвижности"
    )
    
    rezession: Optional[Dict[str, str]] = Field(
        None,
        description="Рецессия десны. Ключ - зуб, значение - степень рецессии в мм"
    )
    
    furkationsbefall: Optional[Dict[str, str]] = Field(
        None,
        description="Вовлечение фуркаций. Ключ - зуб, значение - степень вовлечения"
    )
    
    behandelte_bereiche: Optional[List[str]] = Field(
        None,
        description="Обработанные области/квадранты"
    )
    
    anasthesie: Optional[Dict[str, str]] = Field(
        None,
        description="Информация об анестезии. Ключи могут включать 'тип', 'препарат', 'дозировка'"
    )
    
    medikamente: Optional[List[Dict[str, str]]] = Field(
        None,
        description="Использованные медикаменты. Список словарей с ключами 'название', 'дозировка', 'способ применения'"
    )
    
    mundhygieneempfehlungen: Optional[List[str]] = Field(
        None,
        description="Рекомендации по гигиене полости рта"
    )
    
    recall_intervall: Optional[str] = Field(
        None,
        description="Рекомендуемый интервал для поддерживающей терапии"
    )


class ChirurgieReport(BaseReport):
    """Модель для отчетов о хирургических стоматологических процедурах"""
    
    zahne: Optional[List[str]] = Field(
        None,
        description="Обработанные зубы"
    )
    
    anasthesie: Dict[str, str] = Field(
        description="Информация об анестезии. Ключи могут включать 'тип', 'препарат', 'дозировка'"
    )
    
    zugang: Optional[str] = Field(
        None,
        description="Хирургический доступ и разрез"
    )
    
    lappenbildung: Optional[str] = Field(
        None,
        description="Формирование и отслаивание лоскута"
    )
    
    knochenentfernung: Optional[str] = Field(
        None,
        description="Удаление костной ткани"
    )
    
    extraktion: Optional[Dict[str, str]] = Field(
        None,
        description="Детали экстракции. Ключи могут включать 'техника', 'осложнения', 'состояние лунки'"
    )
    
    alveolenmunagement: Optional[str] = Field(
        None,
        description="Обработка лунки после удаления"
    )
    
    nahttechnik: Optional[Dict[str, str]] = Field(
        None,
        description="Техника ушивания раны. Ключи могут включать 'тип шва', 'материал', 'количество'"
    )
    
    hamostase: Optional[str] = Field(
        None,
        description="Методы гемостаза"
    )
    
    komplikationen: Optional[List[str]] = Field(
        None,
        description="Осложнения и их устранение"
    )
    
    postoperative_anweisungen: Optional[List[str]] = Field(
        None,
        description="Послеоперационные инструкции"
    )
    
    medikamente: Optional[List[Dict[str, str]]] = Field(
        None,
        description="Назначенные медикаменты. Список словарей с ключами 'название', 'дозировка', 'режим'"
    )
    
    nahtentfernung: Optional[str] = Field(
        None,
        description="Информация о снятии швов"
    )


class FüllungenReport(BaseReport):
    """Модель для отчетов о пломбировании"""
    
    zahnnummer: str = Field(
        description="Номер зуба по международной классификации"
    )
    
    behandelte_flachen: Optional[List[str]] = Field(
        None,
        description="Обработанные поверхности зуба (O, M, D, B, L)"
    )
    
    fullungsmaterial: Optional[Dict[str, str]] = Field(
        None,
        description="Информация о пломбировочном материале. Ключи могут включать 'тип', 'производитель', 'оттенок'"
    )
    
    kavitatenklasse: Optional[str] = Field(
        None,
        description="Класс полости по Блэку (I-VI)"
    )
    
    pulpenschutz: Optional[str] = Field(
        None,
        description="Информация о защите пульпы (прокладке)"
    )
    
    anasthesie: Optional[Dict[str, str]] = Field(
        None,
        description="Информация об анестезии. Ключи могут включать 'тип', 'препарат', 'дозировка'"
    )
    
    kofferdam: Optional[str] = Field(
        None,
        description="Информация об использовании коффердама"
    )
    
    matrizentyp: Optional[str] = Field(
        None,
        description="Тип использованной матрицы"
    )


class KfoReport(BaseReport):
    """Модель для отчетов об ортодонтических процедурах"""
    
    behandlung_typ: str = Field(
        description="Тип ортодонтического лечения (брекеты, элайнеры и т.д.)"
    )
    
    gerate_anpassung: Optional[Dict[str, str]] = Field(
        None,
        description="Информация о настройке/адаптации аппаратуры"
    )
    
    aktivierung: Optional[Dict[str, str]] = Field(
        None,
        description="Детали активации ортодонтической аппаратуры"
    )
    
    extraorale_apparaturen: Optional[List[str]] = Field(
        None,
        description="Информация о внеротовых аппаратах"
    )
    
    intraorale_apparaturen: Optional[List[str]] = Field(
        None,
        description="Информация о внутриротовых аппаратах"
    )
    
    aligner_tracking: Optional[Dict[str, str]] = Field(
        None,
        description="Информация о текущем этапе лечения элайнерами"
    )


class KinderReport(BaseReport):
    """Модель для отчетов о детской стоматологии"""
    
    alter_des_kindes: str = Field(
        description="Возраст ребенка"
    )
    
    zahne: Optional[List[str]] = Field(
        None,
        description="Обработанные зубы (по молочной или постоянной нумерации)"
    )
    
    verhaltensfuhrung: Optional[List[str]] = Field(
        None,
        description="Методы управления поведением"
    )
    
    fluoridierung: Optional[Dict[str, str]] = Field(
        None,
        description="Информация о фторировании"
    )
    
    versiegelung: Optional[List[str]] = Field(
        None,
        description="Информация о герметизации фиссур"
    )
    
    elternberatung: Optional[List[str]] = Field(
        None,
        description="Консультация родителей"
    )


class ZeReport(BaseReport):
    """Модель для отчетов о протезировании"""
    
    prothetik_typ: str = Field(
        description="Тип протезирования (коронка, мост, съемный протез, имплантат)"
    )
    
    behandelte_zahne: Optional[List[str]] = Field(
        None,
        description="Обработанные зубы"
    )
    
    abdruckmaterial: Optional[Dict[str, str]] = Field(
        None,
        description="Информация об оттискном материале"
    )
    
    provisorium: Optional[Dict[str, str]] = Field(
        None,
        description="Информация о временной конструкции"
    )
    
    zahnfarbe: Optional[str] = Field(
        None,
        description="Определение цвета зубов"
    )
    
    material: Optional[Dict[str, str]] = Field(
        None,
        description="Материал постоянной конструкции"
    )
    
    okklusion: Optional[Dict[str, str]] = Field(
        None,
        description="Информация о проверке окклюзии"
    )


class OpgDvtReport(BaseReport):
    """Модель для отчетов о рентгенологических исследованиях"""
    
    untersuchungstyp: str = Field(
        description="Тип исследования (OPG, DVT, внутриротовая рентгенография)"
    )
    
    indikation: List[str] = Field(
        description="Показания к исследованию"
    )
    
    befundungsbereiche: List[str] = Field(
        description="Исследуемые области"
    )
    
    strahlendosis: Optional[str] = Field(
        None,
        description="Доза облучения"
    )
    
    gerateeinstellungen: Optional[Dict[str, str]] = Field(
        None,
        description="Настройки рентгеновского аппарата"
    )


class CmdReport(BaseReport):
    """Модель для отчетов о лечении ВНЧС (краниомандибулярной дисфункции)"""
    
    symptome: List[str] = Field(
        description="Симптомы пациента"
    )
    
    palpationsbefunde: Optional[Dict[str, str]] = Field(
        None,
        description="Результаты пальпации мышц и ВНЧС"
    )
    
    beweglichkeit: Optional[Dict[str, str]] = Field(
        None,
        description="Подвижность нижней челюсти"
    )
    
    gelenkgerausche: Optional[Dict[str, str]] = Field(
        None,
        description="Суставные шумы"
    )
    
    schienentyp: Optional[str] = Field(
        None,
        description="Тип назначенной шины"
    )
    
    physiotherapie: Optional[List[str]] = Field(
        None,
        description="Рекомендации по физиотерапии"
    )
    
    medikation: Optional[List[Dict[str, str]]] = Field(
        None,
        description="Назначенные медикаменты"
    )


class SchmerzbehandlungReport(BaseReport):
    """Модель для отчетов о лечении боли"""
    
    schmerzlokalisation: List[str] = Field(
        description="Локализация боли"
    )
    
    schmerzcharakter: Dict[str, str] = Field(
        description="Характер боли (тип, интенсивность, длительность)"
    )
    
    diagnose: str = Field(
        description="Диагноз"
    )
    
    medikation: List[Dict[str, str]] = Field(
        description="Назначенные обезболивающие препараты"
    )
    
    diagnosestellung: Optional[List[str]] = Field(
        None,
        description="Методы диагностики"
    )
    
    differentialdiagnosen: Optional[List[str]] = Field(
        None,
        description="Дифференциальные диагнозы"
    )


# Все модели отчетов
REPORT_MODELS = {
    "base": BaseReport,
    "endo": EndoReport,
    "pa_pzr": PaPzrReport,
    "chirurgie": ChirurgieReport,
    "fullungen": FüllungenReport,
    "kfo": KfoReport,
    "kinder": KinderReport,
    "ze": ZeReport,
    "opg_dvt": OpgDvtReport,
    "cmd": CmdReport,
    "schmerzbehandlung": SchmerzbehandlungReport
} 