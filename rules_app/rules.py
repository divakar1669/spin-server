from typing import List, Dict, Any
from datetime import datetime
import re


class Rule:
    id: str
    description: str
    enabled: bool = True
    severity: str = "error"

    def __init__(self, id: str, description: str, enabled: bool = True, severity: str = "error"):
        self.id = id
        self.description = description
        self.enabled = enabled
        self.severity = severity

    def evaluate(self, claim: Dict[str, Any]) -> List[Dict[str, Any]]:
        raise NotImplementedError()


class ServiceDateRule(Rule):
    """Rule R001: service_date <= submission_date"""

    def __init__(self):
        super().__init__("R001", "Service Date must be on or before Submission Date", True, "error")

    def evaluate(self, claim):
        errs = []
        sd = claim.get("service_date")
        sub = claim.get("submission_date")
        if sd and sub:
            try:
                d1 = datetime.fromisoformat(sd)
                d2 = datetime.fromisoformat(sub)
                if d1 > d2:
                    errs.append({"field": "service_date", "rule_id": self.id, "message": "Service date cannot be after submission date", "severity": self.severity})
            except Exception:
                errs.append({"field": "service_date", "rule_id": self.id, "message": "Invalid date format; use ISO format", "severity": self.severity})
        return errs


class CPTDiagnosisRule(Rule):
    """Rule R002: diagnosis must be compatible with CPT (simple mocked mapping)"""

    CPT_TO_DX = {
        "99214": ["M54.2", "M54.5"],
        "99213": ["R51", "M54.2"],
    }

    def __init__(self):
        super().__init__("R002", "Diagnosis code must be compatible with procedure code", True, "error")

    def evaluate(self, claim):
        errs = []
        dx = claim.get("diagnosis_codes") or []
        px = claim.get("procedure_codes") or []
        for p in px:
            allowed = self.CPT_TO_DX.get(p)
            if allowed:
                for d in dx:
                    if d not in allowed:
                        errs.append({"field": "diagnosis_codes", "rule_id": self.id, "message": f"{d} is not a typical diagnosis for CPT {p}", "severity": self.severity})
        return errs


class ProviderFormatRule(Rule):
    """Rule R003: provider id must match PRV-### and exist in known providers"""

    KNOWN = {"PRV-001", "PRV-002", "PRV-123"}

    def __init__(self):
        super().__init__("R003", "Provider ID format and existence", True, "error")

    def evaluate(self, claim):
        errs = []
        pid = claim.get("provider_id")
        if not pid:
            errs.append({"field": "provider_id", "rule_id": self.id, "message": "provider_id is required", "severity": self.severity})
            return errs
        if not re.match(r"^PRV-\d{3}$", pid):
            errs.append({"field": "provider_id", "rule_id": self.id, "message": "provider_id must match format PRV-###", "severity": self.severity})
        elif pid not in self.KNOWN:
            errs.append({"field": "provider_id", "rule_id": self.id, "message": "Unknown provider_id (not in provider registry)", "severity": self.severity})
        return errs


class RequiredFieldsRule(Rule):
    """Rule R004: required fields present"""

    REQUIRED = ["claim_id", "member_id", "procedure_codes"]

    def __init__(self):
        super().__init__("R004", "Required fields must be present", True, "error")

    def evaluate(self, claim):
        errs = []
        for f in self.REQUIRED:
            v = claim.get(f)
            if v is None or (isinstance(v, list) and len(v) == 0) or (isinstance(v, str) and v.strip() == ""):
                errs.append({"field": f, "rule_id": self.id, "message": f"{f} is required", "severity": self.severity})
        return errs


class DuplicateRule(Rule):
    """Rule R005: simple in-memory duplicate detection based on a seen set"""

    def __init__(self, seen: set):
        super().__init__("R005", "Duplicate claim detection", True, "warning")
        self.seen = seen

    def _key(self, claim):
        return (claim.get("member_id"), claim.get("provider_id"), claim.get("service_date"), tuple(claim.get("procedure_codes") or []))

    def evaluate(self, claim):
        key = self._key(claim)
        if key in self.seen:
            return [{"field": "claim", "rule_id": self.id, "message": "Potential duplicate claim detected", "severity": self.severity}]
        self.seen.add(key)
        return []


def get_default_rules(seen=None):
    if seen is None:
        seen = set()
    return [ServiceDateRule(), CPTDiagnosisRule(), ProviderFormatRule(), RequiredFieldsRule(), DuplicateRule(seen)]
