from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
from .models import Claim, ValidationResult, RuleError, AISuggestion
from .rules import get_default_rules
from .ai import AIClient

app = FastAPI(title="Spin Claim Validator")

ai_client = AIClient()


class ClaimsPayload(BaseModel):
    claims: List[Claim]


@app.post("/validate")
def validate(payload: ClaimsPayload):
    seen = set()
    rules = get_default_rules(seen)
    results = []
    for claim in payload.claims:
        c = claim.dict()
        errors = []
        for r in rules:
            if not r.enabled:
                continue
            errs = r.evaluate(c)
            errors.extend(errs)
        status = "valid" if len(errors) == 0 else "invalid"
        ai_sugg = None
        if status == "invalid":
            suggestion = ai_client.suggest_correction(c, errors)
            ai_sugg = AISuggestion(corrected_fields=suggestion.get("corrected_fields", {}), note=suggestion.get("note"))
        vr = ValidationResult(claim_id=c.get("claim_id"), status=status, errors=[RuleError(**e) for e in errors], ai_suggestion=ai_sugg)
        results.append(vr)
    return results
