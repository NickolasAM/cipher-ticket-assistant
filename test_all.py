import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic
from prompt import PROMPT

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Load your answer key
with open("tickets/answer_key.json") as f:
    answer_key = json.load(f)

# Ask Claude to analyze one ticket, return the parsed answer
def analyze(ticket_text):
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system=PROMPT,
        messages=[{"role": "user", "content": ticket_text}],
    )
    reply = message.content[0].text
    start = reply.find("{")        # grab from the first {
    end = reply.rfind("}")         # to the last }
    return json.loads(reply[start:end + 1])

cat_matches = 0
urg_matches = 0

for entry in answer_key:
    with open(f"tickets/raw/{entry['file']}") as f:
        ticket_text = f.read()

    result = analyze(ticket_text)
    cat_ok = result["category"] == entry["expected_category"]
    urg_ok = result["urgency"] == entry["expected_urgency"]
    cat_matches += cat_ok
    urg_matches += urg_ok

    print(f"{entry['id']}: "
          f"category {'OK  ' if cat_ok else 'MISS'} "
          f"(AI {result['category']} / key {entry['expected_category']})  |  "
          f"urgency {'OK  ' if urg_ok else 'MISS'} "
          f"(AI {result['urgency']} / key {entry['expected_urgency']})")

total = len(answer_key)
print(f"\nCategory accuracy: {cat_matches}/{total}")
print(f"Urgency accuracy:  {urg_matches}/{total}")