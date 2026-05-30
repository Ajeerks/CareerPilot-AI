from groq import Groq
from dotenv import load_dotenv
import os
import json

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
# GENERATE MARKET SKILLS
# ==========================================

def generate_market_skills(
    role,
    industry
):

    prompt = f"""
You are an expert career intelligence system.

Identify the profession using BOTH:

ROLE: {role}

INDUSTRY: {industry}

Generate the most relevant:

- technical skills
- professional skills
- industry skills
- tools
- certifications
- domain knowledge

required for success in this role.

Rules:

1. Return ONLY a valid JSON array.
2. Return between 10 and 20 skills.
3. No explanations.
4. No markdown.
5. Consider the industry context.
6. Do not assume every role is related to software.
7. Generate skills genuinely required for the role.
8. Include practical job-specific skills whenever applicable.

Examples:

Role: Wiper Trainee
Industry: Marine

[
  "marine safety",
  "engine room cleaning",
  "equipment maintenance",
  "ship operations",
  "machinery lubrication",
  "tool handling",
  "safety procedures"
]

Role: Project Manager
Industry: Construction

[
  "project planning",
  "budget management",
  "construction scheduling",
  "risk management",
  "stakeholder communication"
]

Role: Data Scientist
Industry: Information Technology

[
  "python",
  "machine learning",
  "sql",
  "statistics",
  "data visualization"
]

Now generate skills for:

ROLE: {role}

INDUSTRY: {industry}
"""

    try:

        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2

        )

        content = response.choices[0].message.content.strip()

        print("\n==============================")
        print("RAW AI RESPONSE")
        print("==============================\n")
        print(content)

        # Remove markdown wrappers

        content = content.replace(
            "```json",
            ""
        )

        content = content.replace(
            "```",
            ""
        )

        content = content.strip()

        skills = json.loads(content)

        cleaned_skills = []

        for skill in skills:

            if isinstance(skill, str):

                cleaned_skills.append(
                    skill.lower().strip()
                )

        return list(
            set(cleaned_skills)
        )

    except Exception as e:

        print("\n==============================")
        print("ERROR")
        print("==============================\n")
        print(e)

        return []