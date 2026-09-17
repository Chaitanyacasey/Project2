from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

class PersonalInfo(BaseModel):
    full_name: str = Field(..., example="Alex Mercer")
    email: str = Field(..., example="alex.mercer@example.com")
    phone: str = Field(..., example="+1 (555) 234-5678")
    location: str = Field(..., example="San Francisco, CA")
    linkedin: Optional[str] = Field(None, example="linkedin.com/in/alexmercer")
    github: Optional[str] = Field(None, example="github.com/alexmercer")
    portfolio: Optional[str] = Field(None, example="alexmercer.dev")

class WorkExperience(BaseModel):
    company: str = Field(..., example="TechCorp Solutions")
    position: str = Field(..., example="Senior Software Engineer")
    location: str = Field(..., example="San Francisco, CA")
    start_date: str = Field(..., example="Jan 2022")
    end_date: str = Field(..., example="Present")
    bullets: List[str] = Field(..., min_items=1)

class Education(BaseModel):
    institution: str = Field(..., example="University of California, Berkeley")
    degree: str = Field(..., example="Bachelor of Science")
    field_of_study: str = Field(..., example="Computer Science")
    graduation_year: str = Field(..., example="2021")
    gpa: Optional[str] = Field(None, example="3.85 / 4.0")

class SkillCategory(BaseModel):
    category_name: str = Field(..., example="Languages & Frameworks")
    skills: List[str] = Field(..., example=["Python", "FastAPI", "React", "TypeScript", "Docker"])

class ProjectItem(BaseModel):
    title: str = Field(..., example="ResumeForge-API")
    description: str = Field(..., example="Automated resume compilation microservice using Pydantic and Jinja2.")
    tech_stack: List[str] = Field(..., example=["Python", "FastAPI", "Pydantic", "Docker"])
    link: Optional[str] = Field(None, example="github.com/alexmercer/resumeforge")

class ResumePayload(BaseModel):
    target_job_title: str = Field(default="Senior Software Engineer", example="Senior Backend Engineer")
    target_job_description: Optional[str] = Field(None, example="Seeking Python engineer with FastAPI, microservices, and RAG pipeline experience.")
    personal_info: PersonalInfo
    summary: str = Field(..., example="Results-driven Software Engineer with 4+ years of experience building high-throughput distributed APIs and async microservices.")
    experience: List[WorkExperience]
    education: List[Education]
    skills: List[SkillCategory]
    projects: List[ProjectItem] = Field(default_factory=list)
