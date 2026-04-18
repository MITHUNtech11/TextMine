from pydantic import BaseModel, Field
from typing import List, Optional, Literal
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


class ResumeRoot(BaseModel):
    first_name: str
    last_name: str
    name: str = Field(description="The candidate's full name.")
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
