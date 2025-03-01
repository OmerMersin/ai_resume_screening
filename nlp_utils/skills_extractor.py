# nlp_utils/skills_extractor.py

import re

SKILLS = {
    "Python",
    "Java",
    "NLP",
    "Machine Learning",
    "Data Analysis",
    "C++",
    "AWS",
    "Docker",
    "Kubernetes",
    # Add as many as you like...
}

def extract_skills(text: str) -> list:
    """
    A naive approach to find known skill keywords in the text.
    It's case-insensitive, and looks for exact word matches.
    """
    found_skills = []
    text_lower = text.lower()
    for skill in SKILLS:
        # Use a simple regex boundary match
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, text_lower):
            found_skills.append(skill)
    return found_skills