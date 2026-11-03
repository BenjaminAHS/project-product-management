# S3 v0.2 verification · 3 November 2026

Run from the repository root on macOS:

```sh
python scripts/verify_s3.py
```

The dependency-free checker uses the system JavaScriptCore engine and a minimal DOM. It verifies the 20 CSV fixtures and seven proposed eligible labels, policy references, document links, HTML/JavaScript element IDs and the shared brief/annex criterion. Interaction assertions cover both-source inspection, approval, edit invalidation, manual fallback, ticket switching, ambiguity, required handover reason/note, timestamped authorized handover, compliance routing, denied data and reset.

This checks scripted state transitions; it does not render the page, establish keyboard accessibility, validate backend security, measure model quality or replace a participant session. Browser rendering and a screenshot are unverified because the browser execution tool is unavailable in this session.
