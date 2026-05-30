from groq_skills import generate_market_skills
from cache_utils import (
    load_skills_from_cache,
    save_skills_to_cache
)

# ==========================================
# GET MARKET SKILLS
# ==========================================

def get_market_skills(
    role,
    industry
):

    # =====================================
    # CACHE KEY
    # =====================================

    cache_key = (

        role.lower().strip()
        + "_"
        + industry.lower().strip()

    )

    # =====================================
    # CHECK CACHE
    # =====================================

    cached_skills = load_skills_from_cache(
        cache_key
    )

    if cached_skills:

        print(
            "Loaded from cache"
        )

        return cached_skills

    # =====================================
    # CALL GROQ
    # =====================================

    print(
        "Calling Groq..."
    )

    skills = generate_market_skills(

        role,
        industry

    )

    # =====================================
    # SAVE TO CACHE
    # =====================================

    if skills:

        save_skills_to_cache(

            cache_key,
            skills

        )

        return skills

    # =====================================
    # FALLBACK
    # =====================================

    return []