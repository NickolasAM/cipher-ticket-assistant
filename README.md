# Cipher — AI IT Ticket Assistant

Cipher decodes messy, free-text IT help-desk tickets into clear, structured, actionable information. A technician pastes a raw ticket; Cipher returns a summary, category, urgency, likely cause, and a draft response the technician reviews, edits, and sends.

Built as an internal-tools prototype for a fictional defense contractor, **Meridian Defense Solutions**. Uses **synthetic data only** — no real tickets, users, or systems.

## The problem
IT techs receive tickets written in messy human language. For each one they must read it, work out what the user actually needs, classify it, judge urgency, and write a professional reply — slow and inconsistent, especially for newer techs.

## What Cipher does
Paste a raw ticket and Cipher returns:
- **Summary** — one plain-language line of the real need
- **Category** — Access/SSO, Network/Connectivity, Account/Password, Software/Applications, or Hardware
- **Urgency** — Low / Medium / High (judged by impact, not just topic)
- **Likely cause** — the probable underlying issue
- **Draft response** — a professional reply the tech edits and sends

A human always reviews before anything is sent.

## Why AI, not a script
Tickets are unstructured human language, and the real problem is often only implied ("I'm overseas and can't reach the base apps" → firewall/VPN block). Fixed keyword rules break as people rephrase. An LLM reads meaning, and both *understands* the ticket and *generates* the reply — which scripting can't do reliably.

## How it works
- **Backend:** a FastAPI (Python) endpoint `/analyze` that sends the ticket to the Claude API with a structured prompt and returns JSON.
- **Model:** Claude Sonnet — capable enough for the task without overpaying.
- **Frontend:** a single served HTML/CSS/JS page with the input, result cards, and an editable draft.
- **Prompt:** category definitions plus an impact-based urgency rubric, kept in one file and refined against a test set.

## Accuracy
A labeled test set of 15 synthetic tickets (`tickets/answer_key.json`) measures the model against human-assigned correct answers.
- First pass: 13/15 category, 8/15 urgency.
- After sharpening the category and urgency rules: **15/15 category, 15/15 urgency.**

Labels are human-assigned, not AI-generated, so the score measures the model — not the model grading itself.

## Security
App-level measures built in:
- **Synthetic data only** — no real tickets or users.
- **API key in `.env`**, never hardcoded; `.env` is git-ignored so it can't reach GitHub.
- **Input validation** — ticket length is capped.
- **Human-in-the-loop** — the tool drafts; a person reviews before sending.

In production this would run against an internally hosted or government-approved model so ticket data never leaves the boundary, with access controlled by the organization's identity and network security.

## Run it locally
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# create a .env file with: ANTHROPIC_API_KEY=sk-ant-...
uvicorn main:app --reload
```
Then open http://localhost:8000.

## Next steps
- Confidence score + "needs human review" for vague tickets.
- Validate on held-out tickets the model hasn't seen.