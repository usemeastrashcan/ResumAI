from dotenv import load_dotenv
import os
import json
import openai

load_dotenv()

openai.api_key = os.getenv("OPENIAI_API_KEY")

system_prompt = """
    You are a helpful career consultant and resume improvement assistant.
    You take structured data from a person's CV in JSON format (fields like skills, technologies, experience, hobbies, etc.)
    and provide suggestions for improving the content.

    Your suggestions should focus on enhancing clarity, specificity, impact, and professionalism.
    For each section, point out if items could be more detailed, reworded, or grouped better.
    Only suggest things that would help the candidate stand out in a job market.

    Respond with structured JSON like:
    {
    "skills_suggestions": "...",
    "technologies_suggestions": "...",
    "experience_suggestions": "...",
    "hobbies_suggestions": "...",
    "general_tips": "..."
    }
"""


def get_resume_improvements(resume_data):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            { "role": "system", "content": system_prompt },
            { "role": "user", "content": f"Here is the resume data:\n{json.dumps(resume_data, indent=2)}" }
        ],
        temperature=0.7,
    )
    return response['choices'][0]['message']['content']