from flask import Flask, render_template, request,send_from_directory ,redirect, flash, url_for
import smtplib
import json
from pathlib import Path
import os
import pandas as pd
from forms import ContactForm



app = Flask(__name__)


EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")
app.config["RECAPTCHA_PUBLIC_KEY"] = os.getenv("RECAPTCHA_PUBLIC_KEY")
app.config["RECAPTCHA_PRIVATE_KEY"] = os.getenv("RECAPTCHA_PRIVATE_KEY")




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
    per_page = 3
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
    return send_from_directory(diploma_folder, 'Rivka Sorscher mahat diploma.pdf', as_attachment=True)


@app.route("/academics")
def academics_page():
    df = pd.read_excel("Academics.xlsx")  # headers: Course, Grade, Credits
    grades = df.to_dict(orient="records")
    return render_template("academics.html", grades=grades)



from flask import render_template, request, redirect, url_for, flash
import smtplib

import smtplib
import socket

@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data

        try:
            # חיבור עם timeout כדי למנוע תקיעה
            with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.sendmail(
                    EMAIL_ADDRESS,
                    EMAIL_ADDRESS,
                    f"Subject: Portfolio Contact Form\n\n"
                    f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
                )
            flash("Your message has been sent successfully!", "success")

        except (smtplib.SMTPException, socket.timeout) as e:
            flash(f"Error sending message: {e}", "danger")

        return redirect(url_for("contact"))

    return render_template("contact.html", form=form)




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


