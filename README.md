# AI Resume Screening

A production-like Flask application that uses NLP to analyze resumes:
- **SpaCy** for Named Entity Recognition
- **Hugging Face Transformers** for semantic similarity
- **Docker** & **GitHub Actions** for easy deployment & CI
- **Skill Extraction** & **Summarization** as advanced features

## Quick Start

```bash
git clone https://github.com/OmerMersin/ai_resume_screening.git
cd ai_resume_screening
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
