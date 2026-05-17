# Resume AI Assessment & Job Matching System

An intelligent resume parsing and job matching tool based on Claude API, achieving automated Pipeline from unstructured resume/job description text to quantified assessment reports.

## Project Structure

```
resume-ai/
├── main.py                 # FastAPI main entry point with three API interfaces
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template (copy to .env and add API Key)
├── resume-ai.html          # Pure frontend demo page (backend not required)
├── utils/
│   └── file_reader.py      # Read PDF / DOCX resume text
├── parser/
│   ├── resume_parser.py    # Parse resume → structured JSON
│   └── jd_parser.py        # Parse JD → structured JSON
└── matcher/
    └── matcher.py          # Perform matching, scoring + generate assessment report
```

## Quick Start (Backend)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
```bash
cp .env.example .env
# Open .env with your text editor/VSCode and add your Anthropic API Key
```
Get your API Key from https://console.anthropic.com (starts with sk-ant-)

### 3. Start the Service
```bash
uvicorn main:app --reload
```

### 4. Open Test Interface
Open in browser: http://127.0.0.1:8000/docs

## Quick Experience (Frontend, No Python Required)

Open `resume-ai.html` directly in your browser, add your API Key and start using it.

## API Interfaces

| Interface | Method | Description |
|-----------|--------|-------------|
| `/` | GET | Health check |
| `/analyze` | POST | Complete assessment: Upload resume + JD → scoring report |
| `/parse-resume` | POST | Parse resume only → structured JSON |
| `/parse-jd` | POST | Parse JD only → structured JSON |

## Assessment Report Data Structure

```json
{
  "overall_score": 87,
  "dimensions": {
    "skill_match": {"score": 92, "reason": "Python/Go/Redis fully covers job requirements"},
    "experience_match": {"score": 85, "reason": "4 years experience, 1 year below requirement but high project quality"},
    "education_match": {"score": 88, "reason": "Bachelor's degree from SJTU in Computer Science, meets requirements"}
  },
  "strengths": ["Strong hands-on experience with high-concurrency systems", "Technology stack highly aligns", "Top-tier university background"],
  "gaps": ["1 year short on work experience", "No AI project experience"],
  "recommendation": "Candidate has outstanding technical skills, recommend scheduling interview to focus on system design assessment.",
  "verdict": "strongly recommended"
}
```

## Technical Architecture

```
User Layer (Job Seekers/Recruiters)
    ↓
Frontend Application (resume-ai.html)
    ↓
Backend API (FastAPI / main.py)
    ↓
AI Engine (Three modules in parallel)
  ├── Resume Parsing (resume_parser.py)
  ├── Job Understanding (jd_parser.py)
  └── Matching Scoring (matcher.py)
    ↓
Large Language Model Layer (Claude claude-sonnet-4-20250514)
```

## Technology Stack

- **Backend**: Python 3.9+ + FastAPI + Uvicorn
- **Large Language Model**: Claude claude-sonnet-4-20250514 (Anthropic API)
- **Document Parsing**: pdfplumber (PDF), python-docx (DOCX)
- **Frontend**: Pure HTML + Vanilla JS + Chart.js (radar chart) + mammoth.js (DOCX)

## Prompt Design Notes

The system uses two types of Prompts:

1. **Parsing-type Prompts** (resume_parser.py / jd_parser.py)
   - System layer enforces JSON-only output
   - User layer provides complete JSON template for the model to fill in
   - After returning, remove markdown code blocks before json.loads

2. **Assessment-type Prompts** (matcher.py)
   - Insert two structured JSONs into the Prompt
   - Limit verdict to only three fixed values
   - Use LLM-as-Judge mode to implement multi-dimensional semantic scoring
