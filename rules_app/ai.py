from typing import Dict, Any, List


class AIClient:
    """Simple mockable AI client. In a real setup this would call Azure OpenAI."""

    DX_REPLACEMENTS = {
        "R51": "M54.2",
    }

    def suggest_correction(self, claim: Dict[str, Any], errors: List[Dict[str, Any]]) -> Dict[str, Any]:
        corrected = {}
        notes = []
        for e in errors:
            if e.get("rule_id") == "R001":
                # service_date > submission_date: suggest making service_date = submission_date
                corrected["service_date"] = claim.get("submission_date")
                notes.append("Set service_date to submission_date")
            if e.get("rule_id") == "R002":
                # map first offending dx code to a replacement if available
                dxs = claim.get("diagnosis_codes") or []
                for d in dxs:
                    if d in self.DX_REPLACEMENTS:
                        corrected.setdefault("diagnosis_codes", [self.DX_REPLACEMENTS[d]])
                        notes.append(f"Replace {d} with {self.DX_REPLACEMENTS[d]}")
            if e.get("rule_id") == "R003":
                corrected["provider_id"] = "PRV-123"
                notes.append("Normalize provider_id to PRV-123")
            if e.get("rule_id") == "R004":
                # suggest simple placeholders for missing required fields
                field = e.get("field")
                if field == "procedure_codes":
                    corrected.setdefault("procedure_codes", ["99214"])
                    notes.append("Add placeholder procedure code 99214")
                else:
                    corrected.setdefault(field, "UNKNOWN")
                    notes.append(f"Add placeholder for {field}")
        return {"corrected_fields": corrected, "note": "; ".join(notes) if notes else "No suggestion"}
