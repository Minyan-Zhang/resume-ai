import anthropic
import json
import os

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

PROMPT = """
Please parse the following resume text into JSON, output only JSON, no other text or markdown:
{{
  "name": "name",
  "contact": {{"email": "", "phone": ""}},
  "education": [{{"school": "", "degree": "", "major": "", "year": ""}}],
  "experience": [{{"company": "", "title": "", "duration": "", "highlights": []}}],
  "skills": [],
  "summary": "one-sentence background summary"
}}

Resume content:
{text}
"""


def parse_resume(text: str) -> dict:
    """Call Claude to parse resume text into structured JSON"""
    msg = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{
            "role": "user",
            "content": PROMPT.format(text=text)
        }]
    )
    raw = msg.content[0].text.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)
