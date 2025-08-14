from flask import Flask, render_template, request
import json
from pathlib import Path
import os

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
    per_page = 6
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(PROJECTS) + per_page - 1) // per_page
    return render_template(
        "projects.html",
        projects=PROJECTS[start:end],
        page=page,
        total_pages=total_pages
    )


@app.route("/academics")
def academics():
    return render_template("academics.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run()


