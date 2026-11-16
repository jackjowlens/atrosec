import json
from enum import Enum

from pydantic import BaseModel

class DangerEn(str,Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class StatusResponse(str,Enum):
    SECURE='SECURE'
    VULNERABLE='VULNERABLE'
    LITTLE_CONTEXT='LITTLE CONTEXT'
    
class Vulnerability(BaseModel):
    title: str
    cwe_id: str
    danger: DangerEn
    line_number: int | None = None
    description: str
    recomend_fix: str

class UserRequest(BaseModel):
    code_str: str 
    language: str = 'python'
    temperature: float = 0.52

class SecurityResponse(BaseModel):
    status: StatusResponse
    vulnerabilities: list[Vulnerability]
    safe_code: str | None=None
    summary: str



