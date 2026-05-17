import anthropic
import json
import os

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

PROMPT = """
Please parse the following JD (job description) into JSON, output only JSON, no other text or markdown:
{{
  "title": "job_title",
  "must_have": ["required skills or experience"],
  "nice_to_have": ["nice-to-have skills"],
  "responsibilities": ["main responsibilities"],
  "experience_years": "required years of experience",
  "education": "education requirements"
}}

JD content:
{text}
"""


def parse_jd(text: str) -> dict:
    """Call Claude to parse JD text into structured JSON"""
    msg = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": PROMPT.format(text=text)
        }]
    )
    raw = msg.content[0].text.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)
