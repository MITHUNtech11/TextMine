from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any
from enum import Enum


class Address(BaseModel):
    street_address: Optional[str] = None
    taluk: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    pincode: Optional[str] = None


class Language(BaseModel):
    language: str
    can_read: str = Field(description="Must be 'yes' or 'no'.")
    can_speak: str = Field(description="Must be 'yes' or 'no'.")
    can_write: str = Field(description="Must be 'yes' or 'no'.")


class EmploymentEntry(BaseModel):
    endDate: Optional[str] = Field(None, description="End date in YYYY-MM format, or null if current.")
    startDate: Optional[str] = Field(None, description="Start date in YYYY-MM format.")
    department: Optional[str] = None
    current_ctc: Optional[str] = None
    designation: Optional[str] = None
    job_profile: Optional[str] = Field(None, description="Brief description of the role.")
    company_name: Optional[str] = None
    employment_type: Optional[Literal['full-time', 'part-time', 'internship', 'contract', 'freelance']] = None
    relevant_experience: Optional[str] = None


class QualificationEntry(BaseModel):
    search: Optional[str] = Field(None, description="The name of the institution/university.")
    percentage: Optional[str] = None
    qualification: Optional[str] = None
    specialization: Optional[str] = None
    registration_no: Optional[str] = None
    university_name: Optional[str] = None
    college_or_school: Optional[str] = None
    year_of_completion: Optional[str] = Field(None, description="Completion year in YYYY-MM format.")


class DocumentSection(BaseModel):
    heading: Optional[str] = Field(None, description="Section heading or topic.")
    content: str = Field(..., description="Cleaned, readable text content of this section.")


class DocumentExtractionRoot(BaseModel):
    readable_text: str = Field(..., description="The complete, restored, clean, readable text recovered from the document.")
    document_title: Optional[str] = Field(None, description="Inferred document title or document category.")
    summary: Optional[str] = Field(None, description="A concise summary of the recovered document.")
    sections: List[DocumentSection] = Field(default_factory=list, description="Identified document sections with their clean readable text.")
    key_information: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Key entities such as names, organizations, dates, contacts, numbers.")
    quality_assessment: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Assessment of original quality and text restoration confidence.")
    resume_data: Optional[Dict[str, Any]] = Field(None, description="Structured resume data if the document is a resume or CV.")


class ResumeRoot(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    name: Optional[str] = Field(None, description="The candidate's full name.")
    initial: Optional[str] = Field(
        None,
        description="The primary initial, determined by prioritizing standalone single letters, or then last name's first letter."
    )
    email: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[str] = Field(None, description="Date in YYYY-MM-DD format.")
    gender: Optional[Literal['male', 'female']] = None
    marital_status: Optional[Literal['single', 'married', 'divorced', 'separated', 'widowed']] = None
    nationality: Optional[str] = None
    father_name: Optional[str] = Field(None, description="The full name of the candidate's father, if specified in the resume.")
    summary: Optional[str] = Field(None, description="A brief professional summary of the candidate's qualifications and experience.")
    address: Optional[Address] = None
    highest_qualification: Optional[str] = None
    skills: List[str] = Field(default_factory=list, description="A list of all skills found.")
    hobbies: List[str] = Field(default_factory=list)
    languages: List[Language] = Field(default_factory=list)
    work_status: Optional[Literal['freshers', 'experienced']] = None
    employment: List[EmploymentEntry] = Field(default_factory=list)
    qualifications: List[QualificationEntry] = Field(default_factory=list)


class ProcessingStage(str, Enum):
    VALIDATION = "validation"
    CONVERSION = "conversion"
    OCR = "ocr"
    PARSING = "parsing"
    COMPLETE = "complete"
    FAILED = "failed"

