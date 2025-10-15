# Detailed Customer Context

## Overview
Create a structured customer brief by gathering the latest context for a company and outputting a filled Markdown template for downstream sharing.

## Inputs
- `query`: Company name or identifier. If missing, ask the user to provide the company.


## Steps
1. **Capture company**
   - Use the provided `query`.
   - If empty, request the company name from the user before continuing.
2. **Gather context**
   - Use available knowledge, notes linked to `10-Projects`, and meeting logs in `_Meetings` folder to summarize use cases, people, and compute stack for the company.
   - Identify the business problem each use case addresses and capture measurable or directional impact (revenue, efficiency, risk mitigation, etc.).
   - Highlight where information is unknown or needs follow-up.
3. **Produce Markdown**
   - Populate every section in the output template.
   - Include concrete details when known and leave TODOs for gaps.
   - Return the completed Markdown document as the command output.

## Output
- Markdown-formatted customer context document based on the template below.

## Output Template
```
# Use Cases
- **Use case name**
  - Business problem: What pain point or goal this solves, including affected teams or workflows.
  - Solution: Ray components (Ray Core/Data/Train/Tune/etc.), workload type, environment (prod/pilot/POC), deployment notes.
  - Impact: Quantify revenue/cost/time savings or describe directional impact; add TODOs where data is missing.
- Add additional use cases as separate bullet groups following the same structure.

# Key People & Teams
- Name — Title: Two-line summary of current initiatives and responsibilities. Mark the primary point of contact.
- Additional contacts as needed.

# Compute Strategy
- Summarize platforms (AWS Sagemaker, Anyscale Cloud, Kubernetes/KubeRay/EKS, GCP, Azure, Databricks, on-prem, etc.).
- Capture deployment details (regions, clusters, orchestration) and note any gaps or TODOs.
```
