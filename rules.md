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



