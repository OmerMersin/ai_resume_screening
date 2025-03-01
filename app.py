# app.py

import logging
import os
from flask import Flask, request, render_template, redirect, url_for, abort
from config import (
    FLASK_ENV,
    SECRET_KEY,
    MAX_FILE_SIZE_MB,
    ALLOWED_EXT,
    HOST,
    PORT
)

# NLP modules
from nlp_utils.extractor import extract_text
from nlp_utils.ner_model import load_spacy_model, extract_named_entities
from nlp_utils.similarity_model import TextSimilarityModel, load_summarizer, summarize_text
from nlp_utils.skills_extractor import extract_skills

###############################################################################
# 1. APP CONFIG
###############################################################################
app = Flask(__name__)
app.config["ENV"] = FLASK_ENV
app.config["SECRET_KEY"] = SECRET_KEY
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE_MB * 1024 * 1024  # Convert MB to bytes

# File type security check
def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT

# Initialize Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

###############################################################################
# 2. IN-MEMORY STORE FOR CANDIDATES
###############################################################################
# We'll store processed resumes in a dictionary:
# { candidate_id: {... candidate data ...}, ... }
CANDIDATES_DB = {}
NEXT_ID = 1  # auto-incrementing ID

###############################################################################
# 3. LOAD MODELS ON STARTUP
###############################################################################
nlp = load_spacy_model()
similarity_model = TextSimilarityModel()
summarizer = load_summarizer()  # Optional summarization pipeline

###############################################################################
# 4. ROUTES
###############################################################################
@app.route("/", methods=["GET"])
def index():
    """
    Render the home page (index.html) which can:
    1. Upload a single resume (POST -> /process)
    2. Submit a folder path of multiple resumes (POST -> /process_folder)
    """
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    """
    Handle a single-file upload from index.html:
    1. Validate file
    2. Extract text (PDF or TXT)
    3. Perform NLP tasks (NER, skill extraction, similarity)
    4. Show results
    """
    if "resume" not in request.files:
        return redirect(url_for("index"))

    resume_file = request.files["resume"]
    if resume_file.filename == "":
        return redirect(url_for("index"))

    if not allowed_file(resume_file.filename):
        return "<p>Unsupported file type. Please upload a PDF or TXT file.</p>"

    job_description = request.form.get("job_description", "").strip()
    if not job_description:
        return "<p>Please enter a valid job description.</p>"

    try:
        # 1. Extract text
        resume_text = extract_text(resume_file)

        # 2. Named Entities
        entities = extract_named_entities(resume_text, nlp)

        # 3. Skill Extraction
        skills_found = extract_skills(resume_text)

        # 4. Compute similarity
        match_score = similarity_model.compute_similarity(resume_text, job_description)

        # 5. (Optional) Summaries
        job_desc_summary = summarize_text(summarizer, job_description)[:300]
        resume_summary = summarize_text(summarizer, resume_text)[:300]

        return render_template(
            "results.html",
            resume_preview=resume_text[:300],  # Show first 300 chars
            entities=entities,
            skills=skills_found,
            score=round(match_score, 4),
            job_summary=job_desc_summary,
            resume_summary=resume_summary
        )

    except Exception as e:
        logger.error(f"Error processing file: {e}")
        abort(500, description="An error occurred while processing your request.")

@app.route("/process_folder", methods=["POST"])
def process_folder():
    """
    Process all PDF/TXT resumes in a specified folder:
    1. Loop over each file in the folder
    2. Perform NLP tasks (NER, skill extraction, similarity)
    3. Store the results in an in-memory DB (CANDIDATES_DB)
    4. Redirect to /candidates to display a list of processed resumes
    """
    global NEXT_ID

    folder_path = request.form.get("folder_path", "").strip()
    job_description = request.form.get("job_description", "").strip()

    if not folder_path or not os.path.isdir(folder_path):
        return "<p>Please provide a valid folder path containing PDF or TXT files.</p>"

    if not job_description:
        return "<p>Please enter a valid job description.</p>"

    # Process each PDF/TXT in the folder
    for filename in os.listdir(folder_path):
        ext = filename.rsplit(".", 1)[-1].lower()
        if ext not in ALLOWED_EXT:
            # Skip files that are not in ALLOWED_EXT
            continue

        file_path = os.path.join(folder_path, filename)
        logger.info(f"Processing file: {file_path}")

        try:
            with open(file_path, "rb") as f:
                resume_text = extract_text(f)
            
            # Named Entities
            entities = extract_named_entities(resume_text, nlp)

            # Skills
            skills_found = extract_skills(resume_text)

            # Similarity
            match_score = similarity_model.compute_similarity(resume_text, job_description)

            # Store in memory
            candidate_id = NEXT_ID
            NEXT_ID += 1

            # You could parse the candidate's name from resume_text if you have a method.
            # For now, let's just label them "Candidate #"
            CANDIDATES_DB[candidate_id] = {
                "filename": filename,
                "resume_text": resume_text,
                "entities": entities,
                "skills": skills_found,
                "match_score": round(match_score, 4),
                "job_description": job_description
            }
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")

    return redirect(url_for("list_candidates"))

@app.route("/candidates", methods=["GET"])
def list_candidates():
    """
    Display a list of all processed candidates,
    sorted by match score (descending).
    """
    # Convert CANDIDATES_DB to a list
    candidates_list = []
    for cid, data in CANDIDATES_DB.items():
        candidates_list.append({
            "id": cid,
            "filename": data["filename"],
            "score": data["match_score"]
        })
    # Sort by score desc
    candidates_list.sort(key=lambda c: c["score"], reverse=True)

    return render_template("candidates.html", candidates=candidates_list)

@app.route("/candidate/<int:candidate_id>", methods=["GET"])
def candidate_detail(candidate_id):
    """
    Show the detailed results page for a single candidate from CANDIDATES_DB.
    Reuse 'results.html' but adapt it to show that candidate's info.
    """
    if candidate_id not in CANDIDATES_DB:
        abort(404, description="Candidate not found.")

    data = CANDIDATES_DB[candidate_id]

    # If you'd like to create a custom template just for this,
    # you could do that. Here we reuse the 'results.html'.
    # Summaries are optional; let's skip them or set them empty.
    return render_template(
        "results.html",
        resume_preview=data["resume_text"][:300],
        entities=data["entities"],
        skills=data["skills"],
        score=data["match_score"],
        job_summary="",
        resume_summary=""
    )

###############################################################################
# 5. ERROR HANDLERS
###############################################################################
@app.errorhandler(413)  # Payload Too Large
def request_entity_too_large(error):
    return render_template("error.html", message="File too large! Max is {} MB.".format(MAX_FILE_SIZE_MB)), 413

@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", message=str(error)), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template("error.html", message=str(error)), 500

###############################################################################
# 6. MAIN
###############################################################################
if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)