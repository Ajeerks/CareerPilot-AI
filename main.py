from interview_generator import (
    generate_interview_questions
)

from fastapi import FastAPI, UploadFile, File, Form
from jd_parser import extract_jd_skills
from jd_matcher import analyze_resume_against_jd

import fitz
import re

app = FastAPI()

# ==========================================
# CLEAN TEXT
# ==========================================

def clean_text(text):

    text = text.lower()

    text = re.sub(
        r'[^a-zA-Z0-9\s\+\#\.-]',
        ' ',
        text
    )

    text = re.sub(
        r'\s+',
        ' ',
        text
    )

    return text

# ==========================================
# RECOMMENDATIONS
# ==========================================

def generate_recommendations(
    missing_skills
):

    recommendations = []

    for skill in missing_skills[:5]:

        recommendations.append(

            f"Consider improving skills related to {skill}"

        )

    return recommendations

# ==========================================
# HOME
# ==========================================

@app.get("/")
def home():

    return {

        "message":
        "CareerPilot AI Running Successfully"

    }

# ==========================================
# UPLOAD RESUME
# ==========================================

@app.post("/upload")
async def upload_resume(

    job_description: str = Form(...),
    experience_type: str = Form(...),
    years_of_experience: int = Form(0),
    file: UploadFile = File(...)

):

    try:

        # ----------------------------------
        # EXPERIENCE VALIDATION
        # ----------------------------------
        experience_type = experience_type.title()

        if experience_type not in ["Fresher", "Experienced"]:

            return {
                "error":
                "experience_type must be Fresher or Experienced"
             }

        if experience_type == "Fresher":

            years_of_experience = 0

        # ----------------------------------
        # EXTRACT JD SKILLS USING GROQ
        # ----------------------------------

        required_skills = extract_jd_skills(

            job_description

        )

        if not required_skills:

            return {

                "error":
                "Unable to extract skills from Job Description"

            }

        # ----------------------------------
        # READ RESUME PDF
        # ----------------------------------

        contents = await file.read()

        pdf = fitz.open(

            stream=contents,
            filetype="pdf"

        )

        resume_text = ""

        for page in pdf:

            resume_text += page.get_text()

        pdf.close()

        # ----------------------------------
        # ATS ANALYSIS
        # ----------------------------------

        result = analyze_resume_against_jd(

            resume_text,
            required_skills

        )

        ats_score = result["ats_score"]

        matched_skills = result["matched_skills"]

        missing_skills = result["missing_skills"]

        # ----------------------------------
        # RECOMMENDATIONS
        # ----------------------------------

        recommendations = generate_recommendations(

            missing_skills

        )

        # ----------------------------------
        # INTERVIEW QUESTIONS
        # ----------------------------------

        interview_questions = generate_interview_questions(

            job_description,

            experience_type,

            years_of_experience

        )

        # ----------------------------------
        # RESPONSE
        # ----------------------------------

        return {

            "filename":
            file.filename,

            "experience_type":
            experience_type,

            "years_of_experience":
            years_of_experience,

            "required_skills":
            required_skills,

            "ats_score":
            ats_score,

            "total_required_skills":
            len(required_skills),

            "matched_skills":
            matched_skills,

            "missing_skills":
            missing_skills,

            "recommendations":
            recommendations,

            "interview_questions":
            interview_questions

        }

    except Exception as e:

        return {

            "error":
            str(e)

        }