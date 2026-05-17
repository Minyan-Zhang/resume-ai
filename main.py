from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import tempfile
import os

load_dotenv()  # Load API Key from .env file

from utils.file_reader import read_resume
from parser.resume_parser import parse_resume
from parser.jd_parser import parse_jd
from matcher.matcher import match_and_report

app = FastAPI(
    title="Resume AI Assessment & Job Matching System",
    description="Intelligent resume parsing, job description understanding, and multi-dimensional matching scoring system based on Claude API",
    version="1.0.0"
)

# Enable CORS (required for direct frontend calls)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Resume AI Assessment System Running ✓", "version": "1.0.0"}


@app.post("/analyze", summary="Complete Assessment: Upload Resume + JD → Return Matching Report")
async def analyze(
    resume_file: UploadFile = File(..., description="Resume file, supports PDF or DOCX"),
    jd_text: str = Form(..., description="Job Description (JD) text")
):
    """
    Complete Assessment Pipeline:
    1. Read resume file (PDF / DOCX)
    2. Claude parses resume → structured JSON
    3. Claude parses JD → structured JSON
    4. Claude performs matching & scoring → assessment report
    """
    filename = resume_file.filename or ""
    if not (filename.endswith(".pdf") or filename.endswith(".docx")):
        raise HTTPException(status_code=400, detail="Only PDF or DOCX resume files are supported")

    suffix = os.path.splitext(filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await resume_file.read())
        tmp_path = tmp.name

    try:
        raw_text = read_resume(tmp_path)
        resume_data = parse_resume(raw_text)
        jd_data = parse_jd(jd_text)
        result = match_and_report(resume_data, jd_data)

        return {
            "status": "ok",
            "resume": resume_data,
            "jd": jd_data,
            "result": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Assessment failed: {str(e)}")

    finally:
        os.unlink(tmp_path)


@app.post("/parse-resume", summary="Parse Resume Only, Return Structured JSON")
async def parse_resume_only(
    resume_file: UploadFile = File(..., description="Resume file, supports PDF or DOCX")
):
    filename = resume_file.filename or ""
    suffix = os.path.splitext(filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await resume_file.read())
        tmp_path = tmp.name
    try:
        raw_text = read_resume(tmp_path)
        return {"status": "ok", "resume": parse_resume(raw_text)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        os.unlink(tmp_path)


@app.post("/parse-jd", summary="Parse JD Only, Return Structured JSON")
async def parse_jd_only(
    jd_text: str = Form(..., description="Job description text")
):
    try:
        return {"status": "ok", "jd": parse_jd(jd_text)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
