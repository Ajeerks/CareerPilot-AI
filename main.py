from market_skills import get_market_skills
from fastapi import FastAPI, UploadFile, File, Form
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
# EXTRACT RESUME SKILLS
# ==========================================

def extract_resume_skills(
    resume_text,
    required_skills
):

    resume_text = clean_text(
        resume_text
    )

    found_skills = []

    for skill in required_skills:

        if skill.lower() in resume_text:

            found_skills.append(
                skill
            )

    return list(
        set(found_skills)
    )

# ==========================================
# ATS SCORE
# ==========================================

def calculate_ats_score(
    found_skills,
    required_skills
):

    if len(required_skills) == 0:

        return 0

    score = (

        len(found_skills)
        /
        len(required_skills)

    ) * 100

    return round(score)

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

    field: str = Form(...),
    industry: str = Form(...),
    file: UploadFile = File(...)

):

    try:

        # ----------------------------------
        # USER INPUT
        # ----------------------------------

        field = field.lower().strip()

        industry = industry.lower().strip()

        # ----------------------------------
        # GET MARKET SKILLS
        # ----------------------------------

        required_skills = get_market_skills(

            field,
            industry

        )

        if not required_skills:

            return {

                "error":
                f"Unable to generate skills for '{field}'"

            }

        # ----------------------------------
        # READ PDF
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
        # MATCHED SKILLS
        # ----------------------------------

        found_skills = extract_resume_skills(

            resume_text,
            required_skills

        )

        # ----------------------------------
        # MISSING SKILLS
        # ----------------------------------

        missing_skills = []

        for skill in required_skills:

            if skill not in found_skills:

                missing_skills.append(
                    skill
                )

        # ----------------------------------
        # ATS SCORE
        # ----------------------------------

        ats_score = calculate_ats_score(

            found_skills,
            required_skills

        )

        # ----------------------------------
        # RECOMMENDATIONS
        # ----------------------------------

        recommendations = generate_recommendations(

            missing_skills

        )

        # ----------------------------------
        # RESPONSE
        # ----------------------------------

        return {

            "filename":
            file.filename,

            "target_field":
            field,

            "industry":
            industry,

            "ats_score":
            ats_score,

            "total_required_skills":
            len(required_skills),

            "matched_skills":
            found_skills,

            "missing_skills":
            missing_skills,

            "recommendations":
            recommendations

        }

    except Exception as e:

        return {

            "error":
            str(e)

        }