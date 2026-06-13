from sentence_transformers import (
    SentenceTransformer,
    util
)

# ==========================================
# LOAD MODEL
# ==========================================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# ==========================================
# SEMANTIC MATCH
# ==========================================

def semantic_match(

    skill,
    resume_text,
    threshold=0.25

):

    skill_embedding = model.encode(

        skill,

        convert_to_tensor=True

    )

    resume_embedding = model.encode(

        resume_text,

        convert_to_tensor=True

    )

    similarity = util.cos_sim(

        skill_embedding,
        resume_embedding

    )

    score = float(
        similarity
    )

   # print(
   #     f"{skill} -> {score:.3f}"
   # )

    return score >= threshold


# ==========================================
# EXTRACT RESUME SKILLS V2
# ==========================================

def extract_resume_skills_v2(

    resume_text,
    required_skills

):

    matched_skills = []

    for skill in required_skills:

        if semantic_match(

            skill,
            resume_text

        ):

            matched_skills.append(
                skill
            )

    return matched_skills