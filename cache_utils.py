import os
import json

CACHE_FOLDER = "cache"

# ==========================================
# SAVE SKILLS
# ==========================================

def save_skills_to_cache(

    role,
    skills

):

    filename = (

        role.lower()
        .replace(" ", "_")
        + ".json"

    )

    path = os.path.join(

        CACHE_FOLDER,
        filename

    )

    with open(

        path,
        "w",
        encoding="utf-8"

    ) as f:

        json.dump(

            skills,
            f,
            indent=4

        )

# ==========================================
# LOAD SKILLS
# ==========================================

def load_skills_from_cache(role):

    filename = (

        role.lower()
        .replace(" ", "_")
        + ".json"

    )

    path = os.path.join(

        CACHE_FOLDER,
        filename

    )

    if not os.path.exists(path):

        return None

    with open(

        path,
        "r",
        encoding="utf-8"

    ) as f:

        return json.load(f)