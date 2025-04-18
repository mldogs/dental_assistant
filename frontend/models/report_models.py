from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union

import json


class EndodonticReport(BaseModel):
    procedure_type: str = Field(..., description="Type of procedure - will be provided in the prompt")
    
    doctor: str = Field(..., description="Doctor who performed the treatment")
    
    anamnesis: List[str] = Field(..., description="List of patient complaints and medical history in German. Format each item with 'Pat.' prefix if not already present")
    
    anamnesis_reasoning: str = Field(..., description="Citations from the transcription supporting anamnesis")
    
    diagnosis: Optional[str] = Field(None, description="The diagnosis or reason for endodontic treatment")
    
    diagnosis_reasoning: Optional[str] = Field(None, description="Citation from the transcription supporting the diagnosis")
    
    informed_consent: List[str] = Field(..., description="List of information provided to the patient in German. Format each item with 'Über' prefix if applicable")
    
    informed_consent_reasoning: str = Field(..., description="Citations from the transcription supporting informed consent")
    
    treatment_area: List[str] = Field(..., description="FDI tooth numbers for treatment, can be multiple")
    
    treatment_area_reasoning: str = Field(..., description="Citation from the transcription supporting treatment area")
    
    vitality_test: Optional[str] = Field(None, description="Pulp vitality test in format: tooth number, method, result. Example: '26, Kältespray, ++'")
    
    vitality_test_reasoning: Optional[str] = Field(None, description="Citation from the transcription supporting vitality test")
    
    anesthesia: Optional[str] = Field(None, description="Type of anesthesia and application area. Format as 'Infiltrationsanästhesie regio XX'")
    
    anesthesia_reasoning: Optional[str] = Field(None, description="Citation from the transcription supporting anesthesia")
    
    trepanation: Optional[str] = Field(None, description="Information about trepanation. Format as 'Zahn trepaniert'")
    
    trepanation_reasoning: Optional[str] = Field(None, description="Citation from the transcription supporting trepanation")
    
    canal_count: Optional[str] = Field(None, description="Information about number of canals. Format as 'VitE: Anzahl Kanäle: X' where X is the number")
    
    canal_count_reasoning: Optional[str] = Field(None, description="Citation from the transcription supporting canal count")
    
    preparation: Optional[str] = Field(None, description="Information about canal preparation and patency. Format as 'Aufbereitung: Anzahl Kanäle: X, [details]'")
    
    preparation_reasoning: Optional[str] = Field(None, description="Citation from the transcription supporting preparation")
    
    electronic_length_measurement: Optional[str] = Field(None, description="Electronic measurement of canal length. Format as 'ELM: Anzahl: X'")
    
    electronic_length_measurement_reasoning: Optional[str] = Field(None, description="Citation from the transcription supporting electronic length measurement")
    
    irrigation: Optional[str] = Field(None, description="Information about canal irrigation. Format as 'Phys: chem. Wirkung durch Spülung mit [details]'")
    
    irrigation_reasoning: Optional[str] = Field(None, description="Citation from the transcription supporting irrigation")
    
    iso_size: Optional[str] = Field(None, description="Information about ISO instrument size. Format as 'ISO 020' not 'ISO 20'")
    
    iso_size_reasoning: Optional[str] = Field(None, description="Citation from the transcription supporting ISO size")
    
    medication: Optional[str] = Field(None, description="Information about intracanal medication. Format as 'Erste Med, [medication name]'")
    
    medication_reasoning: Optional[str] = Field(None, description="Citation from the transcription supporting medication")
    
    xray: Optional[str] = Field(None, description="Information about X-rays taken during treatment. Format as 'Röntgenaufnahmen während der Behandlung: Anzahl: X, Indikation: Y, Befund: Z'")
    
    xray_reasoning: Optional[str] = Field(None, description="Citation from the transcription supporting X-rays")
    
    next_appointment: Optional[str] = Field(None, description="Information about the next appointment. Format as 'in X Woche(n)'")
    
    next_appointment_reasoning: Optional[str] = Field(None, description="Citation from the transcription supporting next appointment")
    
    planning: Optional[str] = Field(None, description="Planning for future treatment")
    
    planning_reasoning: Optional[str] = Field(None, description="Citation from the transcription supporting planning")


class ZEEingliedernReport(BaseModel):
    """
    A Pydantic model describing the structure of a "ZE Eingliedern" procedure report.
    This includes fields for patient anamnesis, clinical findings, anesthesia details,
    treatment details, and any relevant reasoning or citations from the transcription.
    """
    procedure_type: str = Field(
        ...,
        description="The name of the procedure, e.g. 'ZE Eingliedern'."
    )

    doctor: str = Field(
        ...,
        description="Name of the doctor performing the procedure."
    )

    # Anamnesis (patient complaints / medical history)
    anamnesis: List[str] = Field(
        default_factory=list,
        description="List of patient complaints or medical history in German. "
                    "Format each item with 'Pat.' prefix if not already present."
    )
    anamnesis_reasoning: Optional[str] = Field(
        default=None,
        description="Citations from the transcription supporting the anamnesis."
    )

    # Clinical findings (Befund)
    clinical_findings: Optional[str] = Field(
        default=None,
        description="Description of clinical findings or tooth status."
    )
    clinical_findings_reasoning: Optional[str] = Field(
        default=None,
        description="Citations from the transcription supporting the clinical findings."
    )

    # Patient consent / Aufklärung
    informed_consent: Optional[str] = Field(
        default=None,
        description="Information about risks, benefits, alternatives (Aufklärung)."
    )
    informed_consent_reasoning: Optional[str] = Field(
        default=None,
        description="Citations from the transcription supporting the informed consent discussion."
    )

    # Treatment areas / regions (e.g. OK, UK, tooth numbers)
    treatment_area: List[str] = Field(
        default_factory=list,
        description="List of treatment areas or tooth numbers in FDI notation."
    )
    treatment_area_reasoning: Optional[str] = Field(
        default=None,
        description="Citations supporting the chosen treatment area."
    )

    # Materials / restorations used (e.g. Zirkon, Emax, etc.)
    restoration_materials: List[str] = Field(
        default_factory=list,
        description="List of materials or type of restorations used or planned."
    )
    restoration_materials_reasoning: Optional[str] = Field(
        default=None,
        description="Citations from the transcription supporting the chosen materials."
    )

    # Anesthesia details
    anesthesia_provided: Optional[List[str]] = Field(
        default=None,
        description="Details of local infiltration or conduction anesthesia (e.g., teeth, type, etc.)."
    )
    anesthesia_provided_reasoning: Optional[str] = Field(
        default=None,
        description="Citations from the transcription supporting anesthesia decisions."
    )

    # Lab communication (if any technician/lab was involved)
    lab_communication: Optional[str] = Field(
        default=None,
        description="Any communication with a dental lab or technician."
    )
    lab_communication_reasoning: Optional[str] = Field(
        default=None,
        description="Citations from the transcription for lab communication."
    )

    # Notes on occlusion or fitting
    occlusion_notes: Optional[str] = Field(
        default=None,
        description="Notes regarding occlusion check or issues (Okklusionskontrolle)."
    )
    occlusion_notes_reasoning: Optional[str] = Field(
        default=None,
        description="Citations from the transcription supporting occlusion findings."
    )

    # Next appointment or plan
    next_appointment: Optional[str] = Field(
        default=None,
        description="Information about the next appointment date or plan."
    )
    next_appointment_reasoning: Optional[str] = Field(
        default=None,
        description="Citations from the transcription about the next appointment or plan."
    )

    # Additional notes (anything else not covered above)
    additional_notes: Optional[str] = Field(
        default=None,
        description="Any additional notes or context."
    )
    additional_notes_reasoning: Optional[str] = Field(
        default=None,
        description="Citation from the transcription for additional notes."
    )


class PaAtgMhuReport(BaseModel):
    """
    Pydantic model for Parodontologisches Aufklärungs- und Therapiegespräch (ATG)
    plus Mundhygieneunterweisung (MHU).
    Includes key data points gathered during the procedure and reasoning references from transcription.
    """
    procedure_type: str = Field(
        ...,
        description="Type of procedure, e.g., 'PA ATG + MHU'"
    )
    doctor: str = Field(
        ...,
        description="Name of the dentist performing the procedure"
    )
    anamnesis: List[str] = Field(
        ...,
        description="List of patient complaints and medical history in German. Each item should be prefixed with 'Pat.' if not already"
    )
    anamnesis_reasoning: str = Field(
        ...,
        description="Citations from the transcription supporting the anamnesis"
    )
    diagnosis: Optional[str] = Field(
        None,
        description="Diagnosis or reason for the procedure (if explicitly stated)"
    )
    diagnosis_reasoning: Optional[str] = Field(
        None,
        description="Citation from the transcription supporting the diagnosis"
    )
    atg_details: Optional[str] = Field(
        None,
        description="Details of the Parodontologisches Aufklärungs- und Therapiegespräch (ATG), such as risk factors, possible treatments, Bakteriämie influence, necessity of healthy lifestyle"
    )
    atg_details_reasoning: Optional[str] = Field(
        None,
        description="Citations from the transcription supporting the ATG details"
    )
    mhu_assessment: Optional[str] = Field(
        None,
        description="Assessment of patient's mouth hygiene (e.g. 'gut', 'mäßig', 'schlecht', 'bemüht')"
    )
    mhu_assessment_reasoning: Optional[str] = Field(
        None,
        description="Citations from the transcription supporting the mouth hygiene assessment"
    )
    mhu_instructions: Optional[List[str]] = Field(
        None,
        description="List of instructions/recommendations given to the patient for improving mouth hygiene"
    )
    mhu_instructions_reasoning: Optional[str] = Field(
        None,
        description="Citations from the transcription supporting the MHU instructions"
    )
    treatment_details: Optional[List[str]] = Field(
        None,
        description="Specific treatments performed or planned (e.g., Deep Scaling, CHX-Spülung, Politur)"
    )
    treatment_details_reasoning: Optional[str] = Field(
        None,
        description="Citations from the transcription indicating treatments performed"
    )
    prognosis: Optional[str] = Field(
        None,
        description="Prognosis for the patient after the procedure"
    )
    prognosis_reasoning: Optional[str] = Field(
        None,
        description="Citations from the transcription supporting the prognosis"
    )
    next_appointment: Optional[str] = Field(
        None,
        description="Information about the patient's next appointment if mentioned"
    )
    next_appointment_reasoning: Optional[str] = Field(
        None,
        description="Citations from the transcription regarding the next appointment"
    )
    planning: Optional[str] = Field(
        None,
        description="Planned future treatments or follow-ups"
    )
    planning_reasoning: Optional[str] = Field(
        None,
        description="Citations from the transcription supporting the planning details"
    )
    additional_notes: Optional[str] = Field(
        None,
        description="Any other relevant notes"
    )
    additional_notes_reasoning: Optional[str] = Field(
        None,
        description="Citations from the transcription supporting additional notes"
    )


class FillingPKVReport(BaseModel):
    """
    A Pydantic model capturing all key fields for a 'Füllung PKV' procedure.
    Each field has a corresponding reasoning field with citations from the transcription.
    """
    
    # BASIC METADATA
    procedure_type: str = Field(
        ...,
        description="The procedure type, e.g., 'Füllung PKV'"
    )
    doctor: str = Field(
        ...,
        description="Doctor who performed or supervised the procedure"
    )
    
    
    # ANAMNESE
    anamnesis: List[str] = Field(
        ...,
        description="List of patient complaints, medical history, or statements. Each item should be in German and prefixed with 'Pat.' if not already."
    )
    anamnesis_reasoning: str = Field(
        ...,
        description="Direct transcription citation(s) supporting the anamnesis content"
    )
    
    # INDICATION / DIAGNOSIS
    indication: Optional[str] = Field(
        None,
        description="Reason for performing the filling, e.g. 'Karies', 'Keilförmiger Defekt', etc."
    )
    indication_reasoning: Optional[str] = Field(
        None,
        description="Citation(s) from the transcription supporting the indication"
    )
    
    # TREATMENT AREA (TEETH)
    treatment_area: List[str] = Field(
        default_factory=list,
        description="List of teeth treated using FDI notation, e.g. ['24', '25']"
    )
    treatment_area_reasoning: Optional[str] = Field(
        None,
        description="Citation(s) from the transcription showing which teeth were treated"
    )
    
    # ANESTHESIA
    anesthesia_type: Optional[str] = Field(
        None,
        description="Type(s) of anesthesia used, e.g., 'Infiltrationsanästhesie', 'Leitungsanästhesie'"
    )
    anesthesia_type_reasoning: Optional[str] = Field(
        None,
        description="Citation(s) from the transcription for anesthesia type"
    )
    anesthesia_injection_sites: List[str] = Field(
        default_factory=list,
        description="List of injection sites, e.g. ['v', 'b', 'p', 'l', 'd', 'm']"
    )
    anesthesia_injection_sites_reasoning: Optional[str] = Field(
        None,
        description="Citation(s) from the transcription for injection sites"
    )
    anesthetic_used: Optional[str] = Field(
        None,
        description="Name of anesthetic used, e.g. 'Ultracain D-S', 'Artinestol'"
    )
    anesthetic_used_reasoning: Optional[str] = Field(
        None,
        description="Citation(s) from the transcription for anesthetic used"
    )
    number_of_carpules: Optional[int] = Field(
        None,
        description="Number of carpules (Zylinder) used"
    )
    number_of_carpules_reasoning: Optional[str] = Field(
        None,
        description="Citation(s) from the transcription about carpule quantity"
    )
    factor_increase_reasons: List[str] = Field(
        default_factory=list,
        description="Reasons for potential factor increase, e.g. 'Entzündliche Vorgänge', 'Kompakter Knochen'"
    )
    factor_increase_reasons_reasoning: Optional[str] = Field(
        None,
        description="Citation(s) from the transcription supporting factor increase reasons"
    )
    
    # FILLING DETAILS
    filling_class: Optional[str] = Field(
        None,
        description="Filling classification, e.g. 'F1', 'F2', 'F3', 'F4'"
    )
    filling_class_reasoning: Optional[str] = Field(
        None,
        description="Citation(s) from the transcription for filling class"
    )
    filling_material: Optional[str] = Field(
        None,
        description="Filling material used, e.g. 'Komposit', 'GIZ', 'SDR', 'Amalgam'"
    )
    filling_material_reasoning: Optional[str] = Field(
        None,
        description="Citation(s) from the transcription for filling material"
    )
    filling_steps: List[str] = Field(
        default_factory=list,
        description="Step-by-step procedures for the filling, e.g. 'Kariesexkavation', 'Füllung in Adhäsivtechnik'"
    )
    filling_steps_reasoning: Optional[str] = Field(
        None,
        description="Citation(s) from the transcription for the filling steps"
    )
    
    # PULP CAPPING (Cp / P-Behandlung) - in case of or if mentioned
    pulp_capping: Optional[bool] = Field(
        None,
        description="Indicates if indirect or direct pulp capping was performed"
    )
    pulp_capping_reasoning: Optional[str] = Field(
        None,
        description="Citation(s) from the transcription for pulp capping"
    )
    pulp_capping_material: Optional[str] = Field(
        None,
        description="Material used for pulp capping, e.g. 'Ca(OH)2', 'MTA Pulp Cap'"
    )
    pulp_capping_material_reasoning: Optional[str] = Field(
        None,
        description="Citation(s) for pulp capping material usage"
    )
    
    # POST-OP / NEXT STEPS
    post_op_instructions: Optional[str] = Field(
        None,
        description="Post-operative instructions given to the patient"
    )
    post_op_instructions_reasoning: Optional[str] = Field(
        None,
        description="Citation(s) from the transcription for post-op instructions"
    )
    next_appointment: Optional[str] = Field(
        None,
        description="Information about the next appointment"
    )
    next_appointment_reasoning: Optional[str] = Field(
        None,
        description="Citation(s) related to the next appointment"
    )

class BefundaufnahmeReport(BaseModel):
    """
    Pydantic model for the "01 Befundaufnahme nach Zahnschema" procedure.
    This model captures all relevant fields a dentist needs to track
    during this type of examination, including reasoning fields for
    audit and traceability.
    """
    procedure_type: str = Field(
        ...,
        description="Type of procedure - e.g., '01 Befundaufnahme nach Zahnschema'."
    )
    doctor: str = Field(
        ...,
        description="Name of the doctor who performed the treatment."
    )

    # Anamnese
    anamnesis: List[str] = Field(
        ...,
        description="List of patient complaints or medical history in German. "
                    "Prefix with 'Pat.' if not already present."
    )
    anamnesis_reasoning: str = Field(
        ...,
        description="Citations or transcription evidence supporting the anamnesis."
    )

    # Parodontaler Screening Index (PSI)
    psi_values: Optional[List[str]] = Field(
        None,
        description="List of PSI values (up to 6: S1-S6) if mentioned."
    )
    psi_reasoning: Optional[str] = Field(
        None,
        description="Citation from transcription supporting the PSI values."
    )

    # Mundhygiene-Status
    muhy_status: Optional[str] = Field(
        None,
        description="Mundhygiene status or notes (e.g., 'MuHy muss verbessert werden')."
    )
    muhy_status_reasoning: Optional[str] = Field(
        None,
        description="Citation from transcription supporting the Mundhygiene status."
    )

    # Vitalitätsprüfung
    vital_test: Optional[List[str]] = Field(
        None,
        description="List of vitality test results in the format 'tooth, test, result'."
    )
    vital_test_reasoning: Optional[str] = Field(
        None,
        description="Citation or evidence from transcription supporting vitality tests."
    )

    # Tooth-specific findings
    tooth_findings: Optional[List[str]] = Field(
        None,
        description="List of tooth-specific findings, e.g. '16, Krone Keramik'."
    )
    tooth_findings_reasoning: Optional[str] = Field(
        None,
        description="Citation from transcription supporting the tooth findings."
    )

    # Planning / Therapie
    planning: Optional[str] = Field(
        None,
        description="Planned therapy or next steps discussed."
    )
    planning_reasoning: Optional[str] = Field(
        None,
        description="Citation from transcription supporting the planning."
    )

    # Cost information
    cost_information: Optional[str] = Field(
        None,
        description="Information about costs, Mehrkosten, Eigenanteil, or KVA."
    )
    cost_information_reasoning: Optional[str] = Field(
        None,
        description="Citation from the transcription supporting any cost discussions."
    )

    # Next appointment / Follow-up
    next_appointment: Optional[str] = Field(
        None,
        description="Details of the next appointment or recommended recall interval."
    )
    next_appointment_reasoning: Optional[str] = Field(
        None,
        description="Citation from transcription supporting next appointment."
    )

    # Additional notes / remarks
    other_notes: Optional[str] = Field(
        None,
        description="Miscellaneous remarks or findings not covered above."
    )
    other_notes_reasoning: Optional[str] = Field(
        None,
        description="Citation from transcription for additional remarks."
    )


class ChirExtraktionReport(BaseModel):
    """
    Pydantic model for documenting a surgical tooth extraction (Chir: Extraktion).
    """
    procedure_type: str = Field(
        ...,
        description="Type of procedure, e.g. 'Chir Extraktion'."
    )
    doctor: str = Field(
        ...,
        description="Name of the performing doctor."
    )
    anamnesis: List[str] = Field(
        ...,
        description="List of patient complaints or medical history entries in German. "
                    "Each item should start with 'Pat.' if not already present."
    )
    anamnesis_reasoning: str = Field(
        ...,
        description="Direct quotations from the transcription supporting the anamnesis."
    )
    diagnosis: Optional[str] = Field(
        None,
        description="Diagnosis or reason for extraction."
    )
    diagnosis_reasoning: Optional[str] = Field(
        None,
        description="Excerpt from the transcription supporting the diagnosis."
    )

    # Fields specifically for surgical extraction
    teeth_to_extract: List[str] = Field(
        ...,
        description="List of tooth numbers (FDI notation) to be extracted."
    )
    extraction_indications: List[str] = Field(
        ...,
        description="List of indications for extraction (e.g. 'Fraktur', 'Nicht erhaltungswürdig')."
    )
    extraction_indications_reasoning: str = Field(
        ...,
        description="Citations from the transcription supporting the extraction indications."
    )

    informed_consent: bool = Field(
        ...,
        description="Whether the patient has given informed consent (True/False)."
    )
    informed_consent_reasoning: str = Field(
        ...,
        description="Citation or note from the transcription regarding the patient's consent."
    )

    risk_explanation: bool = Field(
        ...,
        description="Indicates if risk explanation was provided (True/False)."
    )
    risk_explanation_reasoning: str = Field(
        ...,
        description="Citation or note from the transcription regarding risk explanation."
    )

    # Anesthesia details
    anesthesia_type: Optional[str] = Field(
        None,
        description="Type of anesthesia used (e.g. Oberflächenanästhesie, Infiltrationsanästhesie)."
    )
    anesthesia_agent: Optional[str] = Field(
        None,
        description="Which anesthetic agent was used (e.g. Ultracain D-S (1:200000))."
    )
    anesthesia_quantity: Optional[str] = Field(
        None,
        description="Number of carpules or volume of anesthetic, e.g. '2 Zylinder'."
    )
    anesthesia_reasoning: Optional[str] = Field(
        None,
        description="Citation from transcription related to anesthesia details."
    )

    # Surgical details
    procedure_details: Optional[str] = Field(
        None,
        description="Narrative of the surgical steps for the extraction (e.g. Aufklappung, Luxation)."
    )
    procedure_details_reasoning: Optional[str] = Field(
        None,
        description="Excerpt from transcription supporting the recorded procedure details."
    )

    complications: Optional[str] = Field(
        None,
        description="Any complications that occurred during or after the extraction."
    )
    complications_reasoning: Optional[str] = Field(
        None,
        description="Citation from the transcription about complications."
    )

    # Materials used
    materials_used: Optional[List[str]] = Field(
        None,
        description="List of materials used (e.g. Kollagenkegel, CHX Spülung)."
    )
    materials_used_reasoning: Optional[str] = Field(
        None,
        description="Excerpt from transcription referencing used materials."
    )

    # Post-op instructions
    post_op_instructions: Optional[List[str]] = Field(
        None,
        description="List of post-operative care instructions given to the patient."
    )
    post_op_instructions_reasoning: Optional[str] = Field(
        None,
        description="Citation from the transcription about post-op instructions."
    )

    # Duration
    treatment_duration: Optional[str] = Field(
        None,
        description="Indication of how long the procedure took (e.g. '20 Minuten')."
    )
    treatment_duration_reasoning: Optional[str] = Field(
        None,
        description="Excerpt from transcription supporting the documented duration."
    )


class ImplantationReport(BaseModel):
    """
    A Pydantic model describing implant placement procedure report structure
    """
    procedure_type: str = Field(..., description="Type of procedure - 'Implantation'")
    doctor: str = Field(..., description="Doctor who performed the treatment")
    
    anamnesis: List[str] = Field(..., description="List of patient complaints or medical history in German")
    anamnesis_reasoning: str = Field(..., description="Citations from the transcription supporting anamnesis")
    
    planning_data: Optional[str] = Field(None, description="Implant planning data (DVT, OPG, etc.)")
    planning_data_reasoning: Optional[str] = Field(None, description="Citations supporting planning data")
    
    bone_quality: Optional[str] = Field(None, description="Information about bone quality and quantity")
    bone_quality_reasoning: Optional[str] = Field(None, description="Citations about bone assessment")
    
    implant_position: Optional[List[str]] = Field(None, description="Planned implant positions")
    implant_position_reasoning: Optional[str] = Field(None, description="Citations about implant positioning")
    
    implant_system: Optional[str] = Field(None, description="Used implant system and size")
    implant_system_reasoning: Optional[str] = Field(None, description="Citations about implant system")
    
    anesthesia: Optional[str] = Field(None, description="Information about anesthesia")
    anesthesia_reasoning: Optional[str] = Field(None, description="Citations about anesthesia")
    
    surgical_procedure: Optional[str] = Field(None, description="Description of the surgical procedure")
    surgical_procedure_reasoning: Optional[str] = Field(None, description="Citations about surgical process")
    
    bone_augmentation: Optional[str] = Field(None, description="Information about bone augmentation if performed")
    bone_augmentation_reasoning: Optional[str] = Field(None, description="Citations about augmentation")
    
    primary_stability: Optional[str] = Field(None, description="Information about achieved primary stability")
    primary_stability_reasoning: Optional[str] = Field(None, description="Citations about primary stability")
    
    wound_closure: Optional[str] = Field(None, description="Information about wound closure")
    wound_closure_reasoning: Optional[str] = Field(None, description="Citations about wound closure")
    
    post_op_instructions: Optional[List[str]] = Field(None, description="Post-operative instructions")
    post_op_instructions_reasoning: Optional[str] = Field(None, description="Citations about post-op instructions")
    
    healing_phase: Optional[str] = Field(None, description="Information about healing phase and planned exposure")
    healing_phase_reasoning: Optional[str] = Field(None, description="Citations about healing phase")
    
    next_appointment: Optional[str] = Field(None, description="Information about next appointment")
    next_appointment_reasoning: Optional[str] = Field(None, description="Citations about next appointment")


class SchmerzbehandlungReport(BaseModel):
    """
    A Pydantic model for emergency pain treatment in dentistry
    """
    procedure_type: str = Field(..., description="Type of procedure - 'Schmerzbehandlung'")
    doctor: str = Field(..., description="Doctor who performed the treatment")
    
    anamnesis: List[str] = Field(..., description="List of patient complaints or medical history in German")
    anamnesis_reasoning: str = Field(..., description="Citations from the transcription supporting anamnesis")
    
    pain_characteristics: Optional[str] = Field(None, description="Characteristics of pain (location, quality, intensity)")
    pain_characteristics_reasoning: Optional[str] = Field(None, description="Citations about pain characteristics")
    
    pain_triggers: Optional[List[str]] = Field(None, description="Factors that trigger the pain")
    pain_triggers_reasoning: Optional[str] = Field(None, description="Citations about pain triggers")
    
    pain_duration: Optional[str] = Field(None, description="Duration and course of pain")
    pain_duration_reasoning: Optional[str] = Field(None, description="Citations about pain duration")
    
    clinical_examination: Optional[str] = Field(None, description="Findings from clinical examination")
    clinical_examination_reasoning: Optional[str] = Field(None, description="Citations about clinical examination")
    
    sensitivity_tests: Optional[List[str]] = Field(None, description="Results of sensitivity tests (cold, heat, electric)")
    sensitivity_tests_reasoning: Optional[str] = Field(None, description="Citations about sensitivity tests")
    
    radiographic_findings: Optional[str] = Field(None, description="X-ray findings")
    radiographic_findings_reasoning: Optional[str] = Field(None, description="Citations about radiographic findings")
    
    diagnosis: Optional[str] = Field(None, description="Diagnosis of the pain cause")
    diagnosis_reasoning: Optional[str] = Field(None, description="Citations supporting the diagnosis")
    
    emergency_treatment: Optional[str] = Field(None, description="Emergency treatment performed")
    emergency_treatment_reasoning: Optional[str] = Field(None, description="Citations about emergency treatment")
    
    anesthesia: Optional[str] = Field(None, description="Anesthesia details if used")
    anesthesia_reasoning: Optional[str] = Field(None, description="Citations about anesthesia")
    
    trepanation: Optional[str] = Field(None, description="Trepanation details if performed")
    trepanation_reasoning: Optional[str] = Field(None, description="Citations about trepanation")
    
    medication: Optional[str] = Field(None, description="Medications prescribed or used")
    medication_reasoning: Optional[str] = Field(None, description="Citations about medication")
    
    follow_up_plan: Optional[str] = Field(None, description="Further treatment plan")
    follow_up_plan_reasoning: Optional[str] = Field(None, description="Citations about follow-up plan")
    
    prognosis: Optional[str] = Field(None, description="Prognosis assessment")
    prognosis_reasoning: Optional[str] = Field(None, description="Citations about prognosis")


class OPGDVTReport(BaseModel):
    """
    A Pydantic model for radiographic diagnostics (OPG/DVT) in dentistry
    """
    procedure_type: str = Field(..., description="Type of procedure - radiographic type (OPG, DVT)")
    doctor: str = Field(..., description="Doctor who performed the radiographic assessment")
    
    anamnesis: List[str] = Field(..., description="List of patient complaints or medical history in German")
    anamnesis_reasoning: str = Field(..., description="Citations from the transcription supporting anamnesis")
    
    indication: Optional[str] = Field(None, description="Indication for the radiographic examination")
    indication_reasoning: Optional[str] = Field(None, description="Citations about examination indication")
    
    technical_details: Optional[str] = Field(None, description="Technical details of the imaging")
    technical_details_reasoning: Optional[str] = Field(None, description="Citations about technical details")
    
    dental_status: Optional[str] = Field(None, description="Findings about dental status")
    dental_status_reasoning: Optional[str] = Field(None, description="Citations about dental status")
    
    bone_structures: Optional[str] = Field(None, description="Findings about bone structures")
    bone_structures_reasoning: Optional[str] = Field(None, description="Citations about bone structures")
    
    tmj_findings: Optional[str] = Field(None, description="Findings about temporomandibular joints")
    tmj_findings_reasoning: Optional[str] = Field(None, description="Citations about TMJ findings")
    
    sinus_findings: Optional[str] = Field(None, description="Findings about sinuses")
    sinus_findings_reasoning: Optional[str] = Field(None, description="Citations about sinus findings")
    
    pathological_findings: Optional[str] = Field(None, description="Pathological changes observed")
    pathological_findings_reasoning: Optional[str] = Field(None, description="Citations about pathological findings")
    
    implants_restorations: Optional[str] = Field(None, description="Findings about implants or restorations")
    implants_restorations_reasoning: Optional[str] = Field(None, description="Citations about implants/restorations")
    
    interpretation: Optional[str] = Field(None, description="Interpretation and diagnosis")
    interpretation_reasoning: Optional[str] = Field(None, description="Citations about interpretation")
    
    recommendations: Optional[str] = Field(None, description="Recommendations for further diagnostics or treatment")
    recommendations_reasoning: Optional[str] = Field(None, description="Citations about recommendations")
    
    differential_diagnosis: Optional[List[str]] = Field(None, description="Differential diagnoses if relevant")
    differential_diagnosis_reasoning: Optional[str] = Field(None, description="Citations about differential diagnoses")


class CMDReport(BaseModel):
    """
    A Pydantic model for Craniomandibular Dysfunction (CMD) diagnostics and therapy
    """
    procedure_type: str = Field(..., description="Type of procedure - 'CMD-Diagnostik/Therapie'")
    doctor: str = Field(..., description="Doctor who performed the CMD assessment")
    
    anamnesis: List[str] = Field(..., description="List of patient complaints or medical history in German")
    anamnesis_reasoning: str = Field(..., description="Citations from the transcription supporting anamnesis")
    
    main_complaints: Optional[List[str]] = Field(None, description="Main complaints related to CMD")
    main_complaints_reasoning: Optional[str] = Field(None, description="Citations about main complaints")
    
    pain_details: Optional[str] = Field(None, description="Details about pain (location, intensity, triggers)")
    pain_details_reasoning: Optional[str] = Field(None, description="Citations about pain details")
    
    functional_limitations: Optional[str] = Field(None, description="Functional limitations observed")
    functional_limitations_reasoning: Optional[str] = Field(None, description="Citations about functional limitations")
    
    associated_symptoms: Optional[List[str]] = Field(None, description="Associated symptoms (headaches, tinnitus, etc.)")
    associated_symptoms_reasoning: Optional[str] = Field(None, description="Citations about associated symptoms")
    
    psychosocial_factors: Optional[str] = Field(None, description="Psychosocial factors assessment")
    psychosocial_factors_reasoning: Optional[str] = Field(None, description="Citations about psychosocial factors")
    
    tmj_findings: Optional[str] = Field(None, description="TMJ examination findings (sounds, pain on palpation)")
    tmj_findings_reasoning: Optional[str] = Field(None, description="Citations about TMJ findings")
    
    movement_analysis: Optional[str] = Field(None, description="Movement analysis (mouth opening, lateral/protrusive)")
    movement_analysis_reasoning: Optional[str] = Field(None, description="Citations about movement analysis")
    
    muscular_findings: Optional[str] = Field(None, description="Muscular examination findings")
    muscular_findings_reasoning: Optional[str] = Field(None, description="Citations about muscular findings")
    
    occlusion_findings: Optional[str] = Field(None, description="Occlusion examination findings")
    occlusion_findings_reasoning: Optional[str] = Field(None, description="Citations about occlusion findings")
    
    instrumental_analysis: Optional[str] = Field(None, description="Instrumental functional analysis if performed")
    instrumental_analysis_reasoning: Optional[str] = Field(None, description="Citations about instrumental analysis")
    
    imaging_diagnostics: Optional[str] = Field(None, description="Imaging diagnostics (MRI, CT, OPG)")
    imaging_diagnostics_reasoning: Optional[str] = Field(None, description="Citations about imaging diagnostics")
    
    diagnosis: Optional[str] = Field(None, description="CMD diagnosis")
    diagnosis_reasoning: Optional[str] = Field(None, description="Citations supporting the diagnosis")
    
    therapy: Optional[List[str]] = Field(None, description="Therapy approaches (splint, physiotherapy, etc.)")
    therapy_reasoning: Optional[str] = Field(None, description="Citations about therapy")
    
    prognosis: Optional[str] = Field(None, description="Prognosis and further treatment plan")
    prognosis_reasoning: Optional[str] = Field(None, description="Citations about prognosis")


class KFOReport(BaseModel):
    """
    A Pydantic model for orthodontic treatment (KFO)
    """
    procedure_type: str = Field(..., description="Type of procedure - 'Kieferorthopädische Behandlung'")
    doctor: str = Field(..., description="Doctor who performed the orthodontic assessment")
    
    anamnesis: List[str] = Field(..., description="List of patient complaints or medical history in German")
    anamnesis_reasoning: str = Field(..., description="Citations from the transcription supporting anamnesis")
    
    patient_age: Optional[str] = Field(None, description="Patient's age")
    patient_age_reasoning: Optional[str] = Field(None, description="Citations about patient's age")
    
    growth_phase: Optional[str] = Field(None, description="Growth phase assessment")
    growth_phase_reasoning: Optional[str] = Field(None, description="Citations about growth phase")
    
    extraoral_findings: Optional[str] = Field(None, description="Extraoral examination findings")
    extraoral_findings_reasoning: Optional[str] = Field(None, description="Citations about extraoral findings")
    
    intraoral_findings: Optional[str] = Field(None, description="Intraoral examination findings")
    intraoral_findings_reasoning: Optional[str] = Field(None, description="Citations about intraoral findings")
    
    functional_findings: Optional[str] = Field(None, description="Functional examination findings")
    functional_findings_reasoning: Optional[str] = Field(None, description="Citations about functional findings")
    
    model_analysis: Optional[str] = Field(None, description="Model analysis findings")
    model_analysis_reasoning: Optional[str] = Field(None, description="Citations about model analysis")
    
    radiological_findings: Optional[str] = Field(None, description="Radiological findings (cephalometric, OPG)")
    radiological_findings_reasoning: Optional[str] = Field(None, description="Citations about radiological findings")
    
    angle_class: Optional[str] = Field(None, description="Angle classification")
    angle_class_reasoning: Optional[str] = Field(None, description="Citations about Angle class")
    
    skeletal_classification: Optional[str] = Field(None, description="Skeletal classification")
    skeletal_classification_reasoning: Optional[str] = Field(None, description="Citations about skeletal classification")
    
    specific_anomalies: Optional[List[str]] = Field(None, description="Specific orthodontic anomalies")
    specific_anomalies_reasoning: Optional[str] = Field(None, description="Citations about specific anomalies")
    
    treatment_goals: Optional[List[str]] = Field(None, description="Treatment goals")
    treatment_goals_reasoning: Optional[str] = Field(None, description="Citations about treatment goals")
    
    appliance_type: Optional[str] = Field(None, description="Type of appliance (fixed/removable)")
    appliance_type_reasoning: Optional[str] = Field(None, description="Citations about appliance type")
    
    estimated_duration: Optional[str] = Field(None, description="Estimated treatment duration")
    estimated_duration_reasoning: Optional[str] = Field(None, description="Citations about estimated duration")
    
    extractions: Optional[str] = Field(None, description="Information about necessary extractions")
    extractions_reasoning: Optional[str] = Field(None, description="Citations about extractions")
    
    implemented_measures: Optional[List[str]] = Field(None, description="Implemented orthodontic measures")
    implemented_measures_reasoning: Optional[str] = Field(None, description="Citations about implemented measures")
    
    patient_compliance: Optional[str] = Field(None, description="Assessment of patient compliance")
    patient_compliance_reasoning: Optional[str] = Field(None, description="Citations about patient compliance")
    
    oral_hygiene_status: Optional[str] = Field(None, description="Oral hygiene status")
    oral_hygiene_status_reasoning: Optional[str] = Field(None, description="Citations about oral hygiene")
    
    next_appointment: Optional[str] = Field(None, description="Information about next appointment")
    next_appointment_reasoning: Optional[str] = Field(None, description="Citations about next appointment")
    
    planned_measures: Optional[str] = Field(None, description="Planned measures for next appointment")
    planned_measures_reasoning: Optional[str] = Field(None, description="Citations about planned measures")


class KinderReport(BaseModel):
    """
    A Pydantic model for pediatric dentistry procedures
    """
    procedure_type: str = Field(..., description="Type of procedure - pediatric dental treatment type")
    doctor: str = Field(..., description="Doctor who performed the pediatric treatment")
    
    anamnesis: List[str] = Field(..., description="List of patient/parent complaints or medical history in German")
    anamnesis_reasoning: str = Field(..., description="Citations from the transcription supporting anamnesis")
    
    child_age: Optional[str] = Field(None, description="Age of the child")
    child_age_reasoning: Optional[str] = Field(None, description="Citations about child's age")
    
    cooperation: Optional[str] = Field(None, description="Child's cooperation and behavior")
    cooperation_reasoning: Optional[str] = Field(None, description="Citations about cooperation")
    
    dental_status: Optional[str] = Field(None, description="Current dental status and findings")
    dental_status_reasoning: Optional[str] = Field(None, description="Citations about dental status")
    
    caries_defects: Optional[List[str]] = Field(None, description="Caries/defects with tooth numbers")
    caries_defects_reasoning: Optional[str] = Field(None, description="Citations about caries/defects")
    
    development_status: Optional[str] = Field(None, description="Dentition development status")
    development_status_reasoning: Optional[str] = Field(None, description="Citations about development status")
    
    oral_hygiene: Optional[str] = Field(None, description="Oral hygiene status")
    oral_hygiene_reasoning: Optional[str] = Field(None, description="Citations about oral hygiene")
    
    behavior_management: Optional[List[str]] = Field(None, description="Behavior management techniques applied")
    behavior_management_reasoning: Optional[str] = Field(None, description="Citations about behavior management")
    
    materials_used: Optional[List[str]] = Field(None, description="Child-friendly materials used")
    materials_used_reasoning: Optional[str] = Field(None, description="Citations about materials")
    
    special_techniques: Optional[List[str]] = Field(None, description="Special techniques (Tell-Show-Do, etc.)")
    special_techniques_reasoning: Optional[str] = Field(None, description="Citations about special techniques")
    
    preventive_measures: Optional[List[str]] = Field(None, description="Preventive measures (fluoridation, sealants)")
    preventive_measures_reasoning: Optional[str] = Field(None, description="Citations about preventive measures")
    
    parent_recommendations: Optional[List[str]] = Field(None, description="Recommendations for parents/caregivers")
    parent_recommendations_reasoning: Optional[str] = Field(None, description="Citations about parent recommendations")
    
    next_appointment: Optional[str] = Field(None, description="Next appointment and recall interval")
    next_appointment_reasoning: Optional[str] = Field(None, description="Citations about next appointment")

