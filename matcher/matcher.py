import anthropic
import json
import os

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

PROMPT = """
You are a professional recruitment consultant. Based on the candidate's resume and job requirements, provide a detailed matching assessment.
Output only valid JSON, no other text or markdown:

{{
  "overall_score": 85,
  "dimensions": {{
    "skill_match": {{"score": 0, "reason": "detailed explanation"}},
    "experience_match": {{"score": 0, "reason": "detailed explanation"}},
    "education_match": {{"score": 0, "reason": "detailed explanation"}}
  }},
  "strengths": ["strength_1", "strength_2", "strength_3"],
  "gaps": ["gap_1", "gap_2"],
  "recommendation": "2-3 sentences of comprehensive recommendations",
  "verdict": "strongly recommended"
}}

Note: verdict can only be one of the following three: strongly recommended / consider / not a good fit

Candidate resume data:
{resume}

Job requirements data:
{jd}
"""


def match_and_report(resume: dict, jd: dict) -> dict:
    """Call Claude to perform resume-JD matching and scoring, return assessment report"""
    msg = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{
            "role": "user",
            "content": PROMPT.format(
                resume=json.dumps(resume, ensure_ascii=False, indent=2),
                jd=json.dumps(jd, ensure_ascii=False, indent=2)
            )
        }]
    )
    raw = msg.content[0].text.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)
