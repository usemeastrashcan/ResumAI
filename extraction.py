import re

def extract_skills_section(text):
    keywords = ['skills', 'technical skills', 'technologies']
    for keyword in keywords:
        pattern = re.compile(rf'{keyword}.*?(?=\n\n|\n[A-Z])', re.IGNORECASE | re.DOTALL)
        match = pattern.search(text)
        if match:
            return match.group(0)
    return None

def extract_skills_list(skills_section):
    if not skills_section:
        return []

    # Remove the keyword header like "Skills", "Technical Skills", etc.
    skills_section = re.sub(r'(?i)(skills|technical skills|technologies)', '', skills_section).strip()

    # Handle bullets, commas, and newlines
    raw_skills = re.split(r'[\n•,\-\u2022]+', skills_section)

    # Clean individual skills
    skills = [skill.strip().title() for skill in raw_skills if skill.strip()]
    return skills
