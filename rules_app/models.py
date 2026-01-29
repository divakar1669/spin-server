from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class Claim(BaseModel):
    claim_id: str
    member_id: Optional[str]
    provider_id: Optional[str]
    submission_date: Optional[str]
    service_date: Optional[str]
    diagnosis_codes: Optional[List[str]] = []
    procedure_codes: Optional[List[str]] = []


class RuleError(BaseModel):
    field: str
    rule_id: str
    message: str
    severity: str = "error"


class AISuggestion(BaseModel):
    corrected_fields: Dict[str, Any] = {}
    note: Optional[str]


class ValidationResult(BaseModel):
    claim_id: str
    status: str
    errors: List[RuleError] = []
    ai_suggestion: Optional[AISuggestion] = None
