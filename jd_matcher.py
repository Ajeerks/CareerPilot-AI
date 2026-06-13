from semantic_matcher import extract_resume_skills_v2

# ==========================================
# JD ATS ANALYSIS
# ==========================================

def analyze_resume_against_jd(

    resume_text,
    jd_skills

):

    matched_skills = extract_resume_skills_v2(

        resume_text,
        jd_skills

    )

    missing_skills = []

    for skill in jd_skills:

        if skill not in matched_skills:

            missing_skills.append(
                skill
            )

    if len(jd_skills) == 0:

        ats_score = 0

    else:

        ats_score = round(

            (
                len(matched_skills)
                /
                len(jd_skills)
            ) * 100

        )

    return {

        "ats_score":
        ats_score,

        "matched_skills":
        matched_skills,

        "missing_skills":
        missing_skills

    }