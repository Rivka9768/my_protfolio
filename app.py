from flask import Flask, render_template, request, send_from_directory, redirect, flash, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
from pathlib import Path
import os
import pandas as pd
from forms import ContactForm
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")
app.config["RECAPTCHA_PUBLIC_KEY"] = os.getenv("RECAPTCHA_PUBLIC_KEY")
app.config["RECAPTCHA_PRIVATE_KEY"] = os.getenv("RECAPTCHA_PRIVATE_KEY")


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
    df = pd.read_excel("Academics.xlsx")
    grades = df.to_dict(orient="records")
    return render_template("academics.html", grades=grades)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        try:
            # Build a proper MIME message to support Hebrew and UTF-8
            msg = MIMEMultipart()
            msg["Subject"] = "Portfolio Contact Form"
            msg["From"] = EMAIL_ADDRESS
            msg["To"] = EMAIL_ADDRESS
            body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            msg.attach(MIMEText(body, "plain", "utf-8"))
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as server:
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)

            flash("Your message was sent! I appreciate you contacting me.", "success")
        except smtplib.SMTPAuthenticationError:
            flash("Authentication error — please check your App Password.", "danger")
        except smtplib.SMTPException as e:
            flash(f"SMTP error: {e}", "danger")
        except Exception as e:
            flash(f"Error sending message: {e}", "danger")

        return redirect(url_for("contact"))

    # Show validation errors after a failed POST
    if request.method == "POST" and form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in field {field}: {error}", "warning")

    return render_template("contact.html", form=form)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))