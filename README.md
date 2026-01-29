# spin-server



You’re designing a modular, AI-augmented claim validation engine for a large-scale healthtech platform.
Every day, thousands of claims are submitted by healthcare providers. Your job is to build a backend microservice that:
Validates batches of claims using configurable business rules


Suggests corrections for invalid claims using an LLM (like Azure OpenAI)


It is designed for scalability, extensibility, and testability


Think of this as building one of the core microservices in a production-grade backend. This is not a CRUD app — focus on clean design, logic separation, and real-world reliability.

This microservice will eventually be deployed in a high-volume claims pipeline. It should serve as a pre-processing engine before claims hit the core adjudication or payment system — catching errors and improving data quality early.


🧪 What We Expect You to Deliver
✅ A runnable pYHTON backend microservice or any language you are comfortable with


✅ A POST endpoint that accepts a batch of claims and returns validation results


✅ Modular rule evaluation


✅ AI integration (real or mocked) to suggest corrections


✅ Unit + integration test coverage


✅ A README explaining:


Design decisions


How to run/test


Key assumptions and tradeoffs



Your service must:
Accept a batch of claims (e.g., 10–1000) in JSON


Validate each claim against multiple business rules


Mark claims as valid/invalid with structured error messages


If a claim is invalid, use a large language model (LLM) to suggest possible corrections


Support configurable rule behavior (e.g., severity, toggle on/off, etc.)


Tech constraints:
Language: pYTHON 


AI: Azure OpenAI (preferred), or any mockable GPT-like interface


No database required (use in-memory/mock data)


No frontend — this is a backend system only



The exact structure of errors, status, and ai_suggestion is up to you. This is one possible approach.

📥 Example Input (Claim Batch – High Level)
[
  {
    "claim_id": "CLM-001",
    "member_id": "MBR-123",
    "provider_id": "PRV-001",
    "submission_date": "2025-09-15",
    "service_date": "2025-09-16",
    "diagnosis_codes": ["R51"],
    "procedure_codes": ["99214"]
  },
  {
    "claim_id": "CLM-002",
    ...
  }
]
Feel free to define your own structure — this is only a starting point.

📤 Example Output (Validation Result – High Level)
[
  {
    "claim_id": "CLM-001",
    "status": "invalid",
    "errors": [
      {
        "field": "service_date",
        "rule_id": "R001",
        "message": "Service date cannot be after submission date"
      },
      {
        "field": "diagnosis_codes",
        "rule_id": "R003",
        "message": "R51 is not a valid diagnosis for CPT 99214"
      }
    ],
    "ai_suggestion": {
      "corrected_fields": {
        "service_date": "2025-09-14",
        "diagnosis_codes": ["M54.2"]
      },
      "note": "These values are more appropriate based on prior data patterns."
    }
  }
]

Rules

🔹 Rule 1: 
Service Date ≤ Submission Date
Field: service_date, submission_date


Type: Date validation


Severity: Error


Rationale: A claim can’t report a service in the future compared to when it was submitted.



🔹 Rule 2: 
Diagnosis Code Must Match CPT Code
Fields: diagnosis_codes, procedure_codes


Type: CPT-DX compatibility


Severity: Error or warning (depending on policy)


Example: CPT 99214 is usually valid for diagnosis codes like M54.2 (low back pain), but not R51 (headache).



🔹 Rule 3: 
Provider ID Format Must Be Valid
Field: provider_id


Type: Format or existence check


Severity: Error


Rationale: IDs must follow a specific format, e.g., PRV-###, and be present in your known list of providers (mocked).



🔹 Rule 4: 
Required Fields Must Be Present
Field(s): claim_id, member_id, procedure_codes, etc.


Type: Completeness


Severity: Error


Rationale: Claims missing critical fields should be flagged as structurally invalid.



🔹 Rule 5: 
Duplicate Claim Detection (Optional/Advanced)
Field(s): member_id, provider_id, service_date, procedure_codes


Type: Deduplication check


Severity: Warning or soft-fail


Rationale: Detect and warn if the same claim was already submitted (based on combination of fields).




