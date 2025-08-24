from flask import Flask, render_template, request,send_from_directory
import json
from pathlib import Path
import os
import pandas as pd

app = Flask(__name__)

# We'll really use this in Step 2 (projects page). For now it's safe to keep.
PROJECTS_FILE = Path("projects.json")
if PROJECTS_FILE.exists():
    with open(PROJECTS_FILE, "r", encoding="utf-8") as f:
        PROJECTS = json.load(f)
else:
    PROJECTS = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/projects")
def projects_page():
    # optionally support page query param
    page = int(request.args.get("page", 1))
    per_page = 2
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(PROJECTS) + per_page - 1) // per_page
    return render_template(
        "projects.html",
        projects=PROJECTS[start:end],
        page=page,
        total_pages=total_pages
    )

@app.route('/download_diploma')
def download_diploma():
    diploma_folder = os.path.join(app.root_path, 'static', 'diplomas')
    return send_from_directory(diploma_folder, 'mahat_diploma.pdf', as_attachment=True)


@app.route("/academics")
def academics_page():
    df = pd.read_excel("Academics.xlsx")  # headers: Course, Grade, Credits
    grades = df.to_dict(orient="records")
    return render_template("academics.html", grades=grades)


@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


