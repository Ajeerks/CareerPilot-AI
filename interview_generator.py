from groq import Groq
from dotenv import load_dotenv
import os

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
# INTERVIEW QUESTION GENERATOR
# ==========================================

def generate_interview_questions(

    role,
    industry,
    experience="Fresher"

):

    prompt = f"""

Generate exactly 10 interview questions for a {experience}
applying for the role of {role} in the {industry} industry.

Focus on the actual job responsibilities,
industry practices,
safety procedures,
technical knowledge,
and workplace scenarios related to the role.

Do not interpret the role name literally.

Requirements:

-5 Technical Questions
-3 HR Questions
-2 Project-Based Questions

Return only the questions.

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

    return response.choices[0].message.content