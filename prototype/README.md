# FlowAssist · S3 clickable surface

Open `index.html` in a browser; `app.js` must remain beside it. No dependencies, network requests, local storage or API credentials. Optional HTTP launch instructions, design prompt and verification limits: [03_prototype_link.md](../03_prototype_link.md).

Four scripted tickets demonstrate safe workflow states, source inspection, review, editor insertion and escalation. All data is synthetic. The surface examples use DEMO IDs and are distinct from the evaluation rows. They do not execute the S4 pipeline in [spec.md](../spec.md).

“Use draft” only fills the local editor. “Escalate” only displays a local packet. No action sends messages, modifies transactions or contacts a real queue. Reset clears local state. For acceptance scenarios follow [03_user_research.md](../03_user_research.md).

Version v0.2 implements D01–D05 in the decision register: all displayed sources must be inspected, review must be explicit, edits invalidate review, manual mode disables insertion, and handover preserves snapshot times and names the appropriate specialist. Checks and limitations: [verification.md](verification.md).

Vercel hosting is configured at the repository root in [vercel.json](../vercel.json). Deploy from the repository root; the build copies `index.html` and `app.js` into `dist/`, serving the app at `/`. No dependency installation or environment variables are needed.
