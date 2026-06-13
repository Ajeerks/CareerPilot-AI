from groq import Groq
from dotenv import load_dotenv
import os
import ast
import re

# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

# ==========================================
# GROQ CLIENT
# ==========================================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ==========================================
# EXTRACT JD SKILLS
# ==========================================

def extract_jd_skills(job_description):

    prompt = f"""
Extract all important skills from the following Job Description.

Return ONLY a Python list.

Example:

["python", "sql", "machine learning"]

Job Description:

{job_description}
"""

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]

    )

    result = response.choices[0].message.content.strip()

    try:

        # Find the first [...] block
        match = re.search(
            r"\[.*\]",
            result,
            re.DOTALL
        )

        if not match:
            return []

        skills = ast.literal_eval(
            match.group()
        )

        return [

            str(skill).lower().strip()

            for skill in skills

        ]

    except Exception as e:

        print("JD Parsing Error:", e)

        return []