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

    job_description,
    experience_type,
    years_of_experience

):

    prompt = f"""

Generate exactly 10 interview questions based on this Job Description.

Job Description:

{job_description}

Candidate Type:
{experience_type}

Years of Experience:
{years_of_experience}

Requirements:

- 5 Technical Questions
- 3 HR Questions
- 2 Project/Scenario Questions

Focus on:

- Actual job responsibilities
- Required skills
- Industry practices
- Workplace scenarios

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