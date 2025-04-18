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

def format_endo_report(report: EndodonticReport) -> str:
    """
    Convert EndodonticReport model instance to a readable text format in German.
    """
    lines = []
    # Title and Doctor
    lines.append(f"{report.procedure_type}")
    lines.append(f"Behandler: {report.doctor}")
    lines.append("")

    # Anamnesis
    if report.anamnesis:
        lines.append("Anamnese:")
        for item in report.anamnesis:
            lines.append(f"- {item}")
        lines.append("")

    # Diagnosis
    if report.diagnosis:
        lines.append("Diagnose:")
        lines.append(f"{report.diagnosis}")
        lines.append("")

    # Informed consent
    if report.informed_consent:
        lines.append("Aufklärung:")
        for item in report.informed_consent:
            lines.append(f"- {item}")
        lines.append("")

    # Treatment area
    if report.treatment_area:
        lines.append(f"Behandlungsgebiet: {', '.join(report.treatment_area)}")

    # Vitality test
    if report.vitality_test:
        lines.append(f"ViPr: {report.vitality_test}")

    # Anesthesia
    if report.anesthesia:
        lines.append(f"{report.anesthesia}")

    # Trepanation
    if report.trepanation:
        lines.append(f"{report.trepanation}")

    # Canal count
    if report.canal_count:
        lines.append(f"{report.canal_count}")

    # Preparation
    if report.preparation:
        lines.append(f"{report.preparation}")

    # Electronic length measurement
    if report.electronic_length_measurement:
        lines.append(f"{report.electronic_length_measurement}")

    # Irrigation
    if report.irrigation:
        lines.append(f"{report.irrigation}")

    # ISO size
    if report.iso_size:
        lines.append(f"ISO {report.iso_size}")

    # Medication
    if report.medication:
        lines.append(f"{report.medication}")

    # X-ray
    if report.xray:
        lines.append(f"{report.xray}")

    # Next appointment
    if report.next_appointment:
        lines.append(f"Nächster Termin: {report.next_appointment}")

    # Planning
    if report.planning:
        lines.append("")
        lines.append("Planung:")
        lines.append(f"{report.planning}")

    return "\n".join(lines)


def format_ze_eingliedern_report(report: ZEEingliedernReport) -> str:
    """
    Convert ZEEingliedernReport model instance to a readable text format in German.
    """
    lines = []
    # Title and Doctor
    lines.append(f"{report.procedure_type}")
    lines.append(f"Behandler: {report.doctor}")
    lines.append("")

    # Anamnesis
    if report.anamnesis:
        lines.append("Anamnese:")
        for item in report.anamnesis:
            lines.append(f"- {item}")
        lines.append("")

    # Clinical findings
    if report.clinical_findings:
        lines.append("Befund:")
        lines.append(f"{report.clinical_findings}")
        lines.append("")

    # Informed consent
    if report.informed_consent:
        lines.append("Aufklärung:")
        lines.append(f"{report.informed_consent}")
        lines.append("")

    # Treatment area
    if report.treatment_area:
        lines.append("Behandlungsgebiet / Region:")
        lines.append(", ".join(report.treatment_area))
        lines.append("")

    # Restoration materials
    if report.restoration_materials:
        lines.append("Verwendete Materialien / Restaurationen:")
        lines.append(", ".join(report.restoration_materials))
        lines.append("")

    # Anesthesia details
    if report.anesthesia_provided and len(report.anesthesia_provided) > 0:
        lines.append("Anästhesie:")
        for detail in report.anesthesia_provided:
            lines.append(f"- {detail}")
        lines.append("")

    # Lab communication
    if report.lab_communication:
        lines.append("Laborkommunikation:")
        lines.append(report.lab_communication)
        lines.append("")

    # Occlusion notes
    if report.occlusion_notes:
        lines.append("Okklusion / Passung:")
        lines.append(report.occlusion_notes)
        lines.append("")

    # Next appointment
    if report.next_appointment:
        lines.append("Nächster Termin:")
        lines.append(report.next_appointment)
        lines.append("")

    # Additional notes
    if report.additional_notes:
        lines.append("Zusätzliche Hinweise:")
        lines.append(report.additional_notes)
        lines.append("")

    return "\n".join(lines)

def format_filling_pkv_report(report: FillingPKVReport) -> str:
    """
    Converts a FillingPKVReport into a structured, human-readable text.
    """
    lines = []
    
    # HEADER
    lines.append(f"{report.procedure_type}")
    lines.append(f"Behandler: {report.doctor}")
    lines.append("")
    
    
    # ANAMNESE
    if report.anamnesis:
        lines.append("Anamnese:")
        for item in report.anamnesis:
            lines.append(f" - {item}")
        lines.append("")
    
    # INDICATION
    if report.indication:
        lines.append(f"Indikation: {report.indication}")
        lines.append("")
    
    # TREATMENT AREA
    if report.treatment_area:
        lines.append("Behandlungsgebiet (Zahn/ Zähne):")
        lines.append(", ".join(report.treatment_area))
        lines.append("")
    
    # ANESTHESIA
    if report.anesthesia_type:
        lines.append(f"Anästhesie: {report.anesthesia_type}")
  
    if report.anesthesia_injection_sites:
        lines.append(f"Einstichstellen: {', '.join(report.anesthesia_injection_sites)}")
    
    if report.anesthetic_used:
        lines.append(f"Anästhetikum: {report.anesthetic_used}")
    
    if report.number_of_carpules:
        lines.append(f"Anzahl Zylinder: {report.number_of_carpules}")
    
    if report.factor_increase_reasons:
        lines.append("Grund für Faktorsteigerung:")
        for reason in report.factor_increase_reasons:
            lines.append(f" - {reason}")
    lines.append("")
    
    # FILLING
    if report.filling_class:
        lines.append(f"Füllungsklasse: {report.filling_class}")
        lines.append("")
    if report.filling_material:
        lines.append(f"Füllungsmaterial: {report.filling_material}")
        lines.append("")
    if report.filling_steps:
        lines.append("Behandlungsschritte für Füllung:")
        for step in report.filling_steps:
            lines.append(f" - {step}")
        lines.append("")
    
    # PULP CAPPING
    if report.pulp_capping:
        lines.append("Pulpencapping wurde durchgeführt.")
        if report.pulp_capping_material:
            lines.append(f"Verwendetes Material: {report.pulp_capping_material}")
        lines.append("")
    
    # POST-OP
    if report.post_op_instructions:
        lines.append("Postoperative Hinweise:")
        lines.append(report.post_op_instructions)
        lines.append("")
    
    # NEXT APPOINTMENT
    if report.next_appointment:
        lines.append(f"Nächster Termin: {report.next_appointment}")
        lines.append("")
    
    # JOIN AND RETURN
    return "\n".join(lines).strip()

def format_pa_atg_mhu_report(report: PaAtgMhuReport) -> str:
    """
    Converts a PaAtgMhuReport model instance into a readable text report.
    """
    lines = []
    lines.append(f"{report.procedure_type}")
    lines.append(f"Behandler: {report.doctor}")
    lines.append("")

    if report.anamnesis:
        lines.append("Anamnese:")
        for item in report.anamnesis:
            lines.append(f" - {item}")
        lines.append("")

    if report.diagnosis:
        lines.append(f"Diagnose: {report.diagnosis}")
        lines.append("")

    if report.atg_details:
        lines.append("Details Parodontologisches Aufklärungs- und Therapiegespräch (ATG):")
        lines.append(report.atg_details)
        lines.append("")

    if report.mhu_assessment:
        lines.append(f"Mundhygiene-Bewertung: {report.mhu_assessment}")
        lines.append("")

    if report.mhu_instructions:
        lines.append("MHU-Anweisungen:")
        for instr in report.mhu_instructions:
            lines.append(f" - {instr}")
        lines.append("")

    if report.treatment_details:
        lines.append("Behandlung:")
        for detail in report.treatment_details:
            lines.append(f" - {detail}")
        lines.append("")

    if report.prognosis:
        lines.append(f"Prognose: {report.prognosis}")
        lines.append("")

    if report.next_appointment:
        lines.append(f"Nächster Termin: {report.next_appointment}")
        lines.append("")

    if report.planning:
        lines.append(f"Planung: {report.planning}")
        lines.append("")

    if report.additional_notes:
        lines.append(f"Weitere Hinweise: {report.additional_notes}")
        lines.append("")

    return "\n".join(lines)


def format_befundaufnahme_report(report: BefundaufnahmeReport) -> str:
    """
    Converts the BefundaufnahmeReport model into a human-readable text.
    """
    lines = []
    lines.append(f"{report.procedure_type}")
    lines.append(f"Behandler: {report.doctor}")
    lines.append("")

    # Anamnese
    if report.anamnesis:
        lines.append("Anamnese:")
        for item in report.anamnesis:
            lines.append(f"  - {item}")
        lines.append("")

    # PSI
    if report.psi_values:
        psi_str = ", ".join(report.psi_values)
        lines.append(f"PSI-Werte: {psi_str}")
        lines.append("")

    # Mundhygiene
    if report.muhy_status:
        lines.append(f"Mundhygiene-Status: {report.muhy_status}")
        lines.append("")

    # Vitalitätstests
    if report.vital_test:
        lines.append("Vitalitätstest:")
        for vt in report.vital_test:
            lines.append(f"  - {vt}")
        lines.append("")

    # Tooth findings
    if report.tooth_findings:
        lines.append("Zahn-Befunde:")
        for finding in report.tooth_findings:
            lines.append(f"  - {finding}")
        lines.append("")

    # Planning
    if report.planning:
        lines.append(f"Therapieplanung: {report.planning}")
        lines.append("")

    # Costs
    if report.cost_information:
        lines.append(f"Kosten / Mehrkosten: {report.cost_information}")
        lines.append("")

    # Next appointment
    if report.next_appointment:
        lines.append(f"Nächster Termin: {report.next_appointment}")
        lines.append("")

    # Other notes
    if report.other_notes:
        lines.append("Sonstige Bemerkungen:")
        lines.append(f"  {report.other_notes}")
        lines.append("")

    return "\n".join(lines)


def format_chir_extraktion_report(report: ChirExtraktionReport) -> str:
    """
    Formats a ChirExtraktionReport into a multi-line German text report.
    """
    lines = []
    lines.append(f"{report.procedure_type}")
    lines.append(f"Behandler: {report.doctor}")
    lines.append("")

    if report.anamnesis:
        lines.append("Anamnese:")
        for a in report.anamnesis:
            lines.append(f" - {a}")
        lines.append("")

    if report.diagnosis:
        lines.append(f"Diagnose: {report.diagnosis}")
        lines.append("")

    if report.teeth_to_extract:
        lines.append("Zu extrahierende Zähne:")
        lines.append(", ".join(report.teeth_to_extract))
        lines.append("")

    if report.extraction_indications:
        lines.append("Extraktionsindikationen:")
        for ind in report.extraction_indications:
            lines.append(f" - {ind}")
        lines.append("")

    lines.append(f"Aufklärung eingeholt: {'Ja' if report.informed_consent else 'Nein'}")
    lines.append(f"Risikohinweise gegeben: {'Ja' if report.risk_explanation else 'Nein'}")
    lines.append("")

    if report.anesthesia_type or report.anesthesia_agent:
        lines.append("Anästhesie:")
        if report.anesthesia_type:
            lines.append(f" - Typ: {report.anesthesia_type}")
        if report.anesthesia_agent:
            lines.append(f" - Mittel: {report.anesthesia_agent}")
        if report.anesthesia_quantity:
            lines.append(f" - Menge: {report.anesthesia_quantity}")
        lines.append("")

    if report.procedure_details:
        lines.append("Verlauf der Extraktion:")
        lines.append(report.procedure_details)
        lines.append("")

    if report.complications:
        lines.append(f"Komplikationen: {report.complications}")
        lines.append("")

    if report.materials_used:
        lines.append("Verwendete Materialien:")
        for mat in report.materials_used:
            lines.append(f" - {mat}")
        lines.append("")

    if report.post_op_instructions:
        lines.append("Postoperative Hinweise:")
        for hint in report.post_op_instructions:
            lines.append(f" - {hint}")
        lines.append("")

    if report.treatment_duration:
        lines.append(f"Behandlungsdauer: {report.treatment_duration}")
        lines.append("")

    return "\n".join(lines)

def format_implantation_report(report: ImplantationReport) -> str:
    """
    Formats an ImplantationReport into a readable text in German
    """
    lines = []
    lines.append(f"{report.procedure_type}")
    lines.append(f"Behandler: {report.doctor}")
    lines.append("")
    
    if report.anamnesis:
        lines.append("Anamnese:")
        for item in report.anamnesis:
            lines.append(f" - {item}")
        lines.append("")
    
    if report.planning_data:
        lines.append("Planungsdaten:")
        lines.append(f"{report.planning_data}")
        lines.append("")
    
    if report.bone_quality:
        lines.append(f"Knochenqualität und -quantität: {report.bone_quality}")
        lines.append("")
    
    if report.implant_position:
        lines.append("Geplante Implantatpositionen:")
        lines.append(", ".join(report.implant_position))
        lines.append("")
    
    if report.implant_system:
        lines.append(f"Implantatsystem: {report.implant_system}")
        lines.append("")
    
    if report.anesthesia:
        lines.append(f"Anästhesie: {report.anesthesia}")
        lines.append("")
    
    if report.surgical_procedure:
        lines.append("Implantationsprozess:")
        lines.append(report.surgical_procedure)
        lines.append("")
    
    if report.bone_augmentation:
        lines.append(f"Knochenaugmentation: {report.bone_augmentation}")
        lines.append("")
    
    if report.primary_stability:
        lines.append(f"Primärstabilität: {report.primary_stability}")
        lines.append("")
    
    if report.wound_closure:
        lines.append(f"Wundverschluss: {report.wound_closure}")
        lines.append("")
    
    if report.post_op_instructions:
        lines.append("Postoperative Anweisungen:")
        for instruction in report.post_op_instructions:
            lines.append(f" - {instruction}")
        lines.append("")
    
    if report.healing_phase:
        lines.append(f"Heilungsphase: {report.healing_phase}")
        lines.append("")
    
    if report.next_appointment:
        lines.append(f"Nächster Termin: {report.next_appointment}")
        lines.append("")
    
    return "\n".join(lines)


def format_schmerzbehandlung_report(report: SchmerzbehandlungReport) -> str:
    """
    Formats a SchmerzbehandlungReport into a readable text in German
    """
    lines = []
    lines.append(f"{report.procedure_type}")
    lines.append(f"Behandler: {report.doctor}")
    lines.append("")
    
    if report.anamnesis:
        lines.append("Schmerzanamnese:")
        for item in report.anamnesis:
            lines.append(f" - {item}")
        lines.append("")
    
    if report.pain_characteristics:
        lines.append(f"Schmerzcharakteristik: {report.pain_characteristics}")
        lines.append("")
    
    if report.pain_triggers:
        lines.append("Auslöser:")
        for trigger in report.pain_triggers:
            lines.append(f" - {trigger}")
        lines.append("")
    
    if report.pain_duration:
        lines.append(f"Dauer und Verlauf: {report.pain_duration}")
        lines.append("")
    
    if report.clinical_examination:
        lines.append("Klinische Untersuchung:")
        lines.append(report.clinical_examination)
        lines.append("")
    
    if report.sensitivity_tests:
        lines.append("Sensibilitätstests:")
        for test in report.sensitivity_tests:
            lines.append(f" - {test}")
        lines.append("")
    
    if report.radiographic_findings:
        lines.append(f"Röntgenbefund: {report.radiographic_findings}")
        lines.append("")
    
    if report.diagnosis:
        lines.append(f"Diagnose: {report.diagnosis}")
        lines.append("")
    
    if report.emergency_treatment:
        lines.append("Notfallbehandlung:")
        lines.append(report.emergency_treatment)
        lines.append("")
    
    if report.anesthesia:
        lines.append(f"Anästhesie: {report.anesthesia}")
        lines.append("")
    
    if report.trepanation:
        lines.append(f"Trepanation: {report.trepanation}")
        lines.append("")
    
    if report.medication:
        lines.append(f"Medikation: {report.medication}")
        lines.append("")
    
    if report.follow_up_plan:
        lines.append(f"Weiterführender Behandlungsplan: {report.follow_up_plan}")
        lines.append("")
    
    if report.prognosis:
        lines.append(f"Prognose: {report.prognosis}")
        lines.append("")
    
    return "\n".join(lines)


def format_opg_dvt_report(report: OPGDVTReport) -> str:
    """
    Formats an OPGDVTReport into a readable text in German
    """
    lines = []
    lines.append(f"{report.procedure_type}")
    lines.append(f"Behandler: {report.doctor}")
    lines.append("")
    
    if report.anamnesis:
        lines.append("Anamnese:")
        for item in report.anamnesis:
            lines.append(f" - {item}")
        lines.append("")
    
    if report.indication:
        lines.append(f"Indikation: {report.indication}")
        lines.append("")
    
    if report.technical_details:
        lines.append(f"Technische Details: {report.technical_details}")
        lines.append("")
    
    lines.append("Befunde:")
    
    if report.dental_status:
        lines.append(f" - Zahnstatus: {report.dental_status}")
    
    if report.bone_structures:
        lines.append(f" - Knochenstrukturen: {report.bone_structures}")
    
    if report.tmj_findings:
        lines.append(f" - Kiefergelenke: {report.tmj_findings}")
    
    if report.sinus_findings:
        lines.append(f" - Kieferhöhlen: {report.sinus_findings}")
    
    if report.pathological_findings:
        lines.append(f" - Pathologische Veränderungen: {report.pathological_findings}")
    
    if report.implants_restorations:
        lines.append(f" - Implantate/Restaurationen: {report.implants_restorations}")
    
    lines.append("")
    
    if report.interpretation:
        lines.append(f"Interpretation und Diagnose: {report.interpretation}")
        lines.append("")
    
    if report.recommendations:
        lines.append(f"Empfehlungen: {report.recommendations}")
        lines.append("")
    
    if report.differential_diagnosis:
        lines.append("Differentialdiagnosen:")
        for dd in report.differential_diagnosis:
            lines.append(f" - {dd}")
        lines.append("")
    
    return "\n".join(lines)


def format_cmd_report(report: CMDReport) -> str:
    """
    Formats a CMDReport into a readable text in German
    """
    lines = []
    lines.append(f"{report.procedure_type}")
    lines.append(f"Behandler: {report.doctor}")
    lines.append("")
    
    if report.anamnesis:
        lines.append("Anamnese:")
        for item in report.anamnesis:
            lines.append(f" - {item}")
        lines.append("")
    
    if report.main_complaints:
        lines.append("Hauptbeschwerden:")
        for complaint in report.main_complaints:
            lines.append(f" - {complaint}")
        lines.append("")
    
    if report.pain_details:
        lines.append(f"Schmerzdetails: {report.pain_details}")
        lines.append("")
    
    if report.functional_limitations:
        lines.append(f"Funktionseinschränkungen: {report.functional_limitations}")
        lines.append("")
    
    if report.associated_symptoms:
        lines.append("Begleiterscheinungen:")
        for symptom in report.associated_symptoms:
            lines.append(f" - {symptom}")
        lines.append("")
    
    if report.psychosocial_factors:
        lines.append(f"Psychosoziale Faktoren: {report.psychosocial_factors}")
        lines.append("")
    
    lines.append("Untersuchungsbefunde:")
    
    if report.tmj_findings:
        lines.append(f" - Kiefergelenksbefund: {report.tmj_findings}")
    
    if report.movement_analysis:
        lines.append(f" - Bewegungsanalyse: {report.movement_analysis}")
    
    if report.muscular_findings:
        lines.append(f" - Muskulärer Befund: {report.muscular_findings}")
    
    if report.occlusion_findings:
        lines.append(f" - Okklusionsbefund: {report.occlusion_findings}")
    
    lines.append("")
    
    if report.instrumental_analysis:
        lines.append(f"Instrumentelle Funktionsanalyse: {report.instrumental_analysis}")
        lines.append("")
    
    if report.imaging_diagnostics:
        lines.append(f"Bildgebende Diagnostik: {report.imaging_diagnostics}")
        lines.append("")
    
    if report.diagnosis:
        lines.append(f"Diagnose: {report.diagnosis}")
        lines.append("")
    
    if report.therapy:
        lines.append("Therapie:")
        for item in report.therapy:
            lines.append(f" - {item}")
        lines.append("")
    
    if report.prognosis:
        lines.append(f"Prognose: {report.prognosis}")
        lines.append("")
    
    return "\n".join(lines)


def format_kfo_report(report: KFOReport) -> str:
    """
    Formats a KFOReport into a readable text in German
    """
    lines = []
    lines.append(f"{report.procedure_type}")
    lines.append(f"Behandler: {report.doctor}")
    lines.append("")
    
    if report.anamnesis:
        lines.append("Anamnese:")
        for item in report.anamnesis:
            lines.append(f" - {item}")
        lines.append("")
    
    if report.patient_age:
        lines.append(f"Alter des Patienten: {report.patient_age}")
        lines.append("")
    
    if report.growth_phase:
        lines.append(f"Wachstumsphase: {report.growth_phase}")
        lines.append("")
    
    lines.append("Diagnostik:")
    
    if report.extraoral_findings:
        lines.append(f" - Extraorale Befunde: {report.extraoral_findings}")
    
    if report.intraoral_findings:
        lines.append(f" - Intraorale Befunde: {report.intraoral_findings}")
    
    if report.functional_findings:
        lines.append(f" - Funktionsbefunde: {report.functional_findings}")
    
    if report.model_analysis:
        lines.append(f" - Modellanalyse: {report.model_analysis}")
    
    if report.radiological_findings:
        lines.append(f" - Röntgenologische Befunde: {report.radiological_findings}")
    
    lines.append("")
    
    if report.angle_class:
        lines.append(f"Angle-Klasse: {report.angle_class}")
        lines.append("")
    
    if report.skeletal_classification:
        lines.append(f"Skelettale Klassifikation: {report.skeletal_classification}")
        lines.append("")
    
    if report.specific_anomalies:
        lines.append("Spezifische Anomalien:")
        for anomaly in report.specific_anomalies:
            lines.append(f" - {anomaly}")
        lines.append("")
    
    if report.treatment_goals:
        lines.append("Behandlungsziele:")
        for goal in report.treatment_goals:
            lines.append(f" - {goal}")
        lines.append("")
    
    if report.appliance_type:
        lines.append(f"Apparatur: {report.appliance_type}")
        lines.append("")
    
    if report.estimated_duration:
        lines.append(f"Voraussichtliche Behandlungsdauer: {report.estimated_duration}")
        lines.append("")
    
    if report.extractions:
        lines.append(f"Extraktionen: {report.extractions}")
        lines.append("")
    
    if report.implemented_measures:
        lines.append("Durchgeführte Maßnahmen:")
        for measure in report.implemented_measures:
            lines.append(f" - {measure}")
        lines.append("")
    
    if report.patient_compliance:
        lines.append(f"Patientencompliance: {report.patient_compliance}")
        lines.append("")
    
    if report.oral_hygiene_status:
        lines.append(f"Mundhygienestatus: {report.oral_hygiene_status}")
        lines.append("")
    
    if report.next_appointment:
        lines.append(f"Nächster Termin: {report.next_appointment}")
        lines.append("")
    
    if report.planned_measures:
        lines.append(f"Geplante Maßnahmen: {report.planned_measures}")
        lines.append("")
    
    return "\n".join(lines)


def format_kinder_report(report: KinderReport) -> str:
    """
    Formats a KinderReport into a readable text in German
    """
    lines = []
    lines.append(f"{report.procedure_type}")
    lines.append(f"Behandler: {report.doctor}")
    lines.append("")
    
    if report.child_age:
        lines.append(f"Alter des Kindes: {report.child_age}")
        lines.append("")
    
    if report.anamnesis:
        lines.append("Anamnese:")
        for item in report.anamnesis:
            lines.append(f" - {item}")
        lines.append("")
    
    if report.cooperation:
        lines.append(f"Kooperationsverhalten: {report.cooperation}")
        lines.append("")
    
    if report.dental_status:
        lines.append(f"Zahnstatus: {report.dental_status}")
        lines.append("")
    
    if report.caries_defects:
        lines.append("Karies/Defekte:")
        for item in report.caries_defects:
            lines.append(f" - {item}")
        lines.append("")
    
    if report.development_status:
        lines.append(f"Entwicklungsstand des Gebisses: {report.development_status}")
        lines.append("")
    
    if report.oral_hygiene:
        lines.append(f"Mundhygienestatus: {report.oral_hygiene}")
        lines.append("")
    
    if report.behavior_management:
        lines.append("Angewandte verhaltensführende Techniken:")
        for technique in report.behavior_management:
            lines.append(f" - {technique}")
        lines.append("")
    
    if report.materials_used:
        lines.append("Verwendete Materialien:")
        for material in report.materials_used:
            lines.append(f" - {material}")
        lines.append("")
    
    if report.special_techniques:
        lines.append("Spezielle Techniken:")
        for technique in report.special_techniques:
            lines.append(f" - {technique}")
        lines.append("")
    
    if report.preventive_measures:
        lines.append("Prophylaxemaßnahmen:")
        for measure in report.preventive_measures:
            lines.append(f" - {measure}")
        lines.append("")
    
    if report.parent_recommendations:
        lines.append("Empfehlungen für Eltern/Betreuer:")
        for rec in report.parent_recommendations:
            lines.append(f" - {rec}")
        lines.append("")
    
    if report.next_appointment:
        lines.append(f"Nächster Termin: {report.next_appointment}")
        lines.append("")
    
    return "\n".join(lines)
