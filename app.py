from flask import Flask, render_template, request,send_from_directory ,redirect, flash, url_for
import smtplib
import json
from pathlib import Path
import os
import pandas as pd


app = Flask(__name__)
app.secret_key = "your_secret_key_here"



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

@app.route("/submit_contact", methods=["POST"])
def submit_contact():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    # Example: send email using SMTP (configure with your email provider)
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("your_email@gmail.com", "your_email_app_password")
            server.sendmail(
                "your_email@gmail.com",
                "your_email@gmail.com",  # send to yourself
                f"Subject: Portfolio Contact Form\n\nName: {name}\nEmail: {email}\n\nMessage:\n{message}"
            )
        flash("Your message has been sent successfully!", "success")
    except Exception as e:
        flash(f"Error sending message: {e}", "danger")

    return redirect(url_for("contact"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


