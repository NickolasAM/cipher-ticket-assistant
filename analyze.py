import os
from dotenv import load_dotenv
from anthropic import Anthropic

# 1. Load your API key from the .env file
load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# 2. The instructions we give Claude (the "prompt")
PROMPT = """You are an IT support assistant that analyzes help-desk tickets.

You will be given the raw text of one IT ticket. Read it and work out what the user actually needs.

Sort it into exactly ONE of these categories:
- Access/SSO — can't log into apps (Teams, Outlook, Zoom) or single sign-on issues
- Network/Connectivity — can't reach apps/services due to firewall, VPN, or being out of the country
- Account/Password — password resets or locked accounts
- Software/Applications — SharePoint, Outlook, or other app usage questions
- Hardware — hardware requests or device problems

Judge urgency as Low, Medium, or High. Base it on impact, not just topic: someone fully blocked or facing a deadline is High, even for a normally routine issue.

Respond with ONLY a JSON object, no other text, in exactly this shape:
{
  "summary": "one plain sentence of what the user actually needs",
  "category": "one of the five categories above",
  "urgency": "Low, Medium, or High",
  "likely_cause": "the most likely underlying cause",
  "draft_response": "a short, professional reply the tech can edit and send"
}"""

# 3. Read one ticket to test with
with open("tickets/raw/ticket_01.txt") as f:
    ticket_text = f.read()

# 4. Send the ticket to Claude
message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1000,
    system=PROMPT,
    messages=[{"role": "user", "content": ticket_text}],
)

# 5. Print Claude's answer
print(message.content[0].text)