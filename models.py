from pydantic import BaseModel
from typing import Optional, List


class PersonalInfo(BaseModel):
    name: str
    location: Optional[str] = None
    phone: Optional[str] = None
    email: str
    links: List[str] = []


class Education(BaseModel):
    school: str
    location: str
    degree: str
    date: str


class Experience(BaseModel):
    company: str
    location: Optional[str] = None
    role: str
    dates: str
    bullets: List[str]


class Project(BaseModel):
    name: str
    tech: str
    bullets: List[str]


class SkillCategory(BaseModel):
    category: str
    items: str


class HonoursAward(BaseModel):
    title: str
    organization: Optional[str] = None
    date: Optional[str] = None


class Publication(BaseModel):
    title: str
    venue: str
    date: str


class Reference(BaseModel):
    name: str
    title: str
    institution: str
    email: str


class CV(BaseModel):
    personal: PersonalInfo
    summary: Optional[str] = None
    education: List[Education] = []
    experience: List[Experience] = []
    projects: List[Project] = []
    skills: List[SkillCategory] = []
    honours_awards: List[HonoursAward] = []
    publications: List[Publication] = []
    references: List[Reference] = []
