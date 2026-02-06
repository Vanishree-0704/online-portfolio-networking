from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_cors import CORS
from database import get_db_connection
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
CORS(app)

# Session key
app.secret_key = "secret123"

# -----------------------------
# HOME – PORTFOLIO
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# --------------------------------
# CONTACT FORM – STORE MESSAGE + EMAIL
# --------------------------------
@app.route("/contact", methods=["POST"])
def contact():
    data = request.json

    name = data.get("name")
    email = data.get("email")
    subject = data.get("subject")
    message = data.get("message")

    # ---- DATABASE SAVE ----
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO contact_messages (name, email, subject, message) VALUES (?, ?, ?, ?)",
        (name, email, subject, message)
    )

    conn.commit()
    conn.close()

    # ---- SEND EMAIL ----
    print("send_email function called")
    send_email(name, email, subject, message)

    return jsonify({
        "status": "success",
        "message": "Message sent successfully"
    })


# --------------------------------
# 🔐 ADMIN LOGIN
# --------------------------------
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM admin_users WHERE username=? AND password=?",
            (username, password)
        )
        admin = cursor.fetchone()
        conn.close()

        if admin:
            session["admin"] = username
            return redirect(url_for("admin_dashboard"))
        else:
            return "Invalid login"

    return render_template("admin_login.html")


# --------------------------------
# 📊 ADMIN DASHBOARD – VIEW MESSAGES
# --------------------------------
@app.route("/admin/dashboard")
def admin_dashboard():
    if "admin" not in session:
        return redirect(url_for("admin_login"))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM contact_messages ORDER BY created_at DESC"
    )
    messages = cursor.fetchall()
    conn.close()

    return render_template("admin_dashboard.html", messages=messages)


# --------------------------------
# 🚪 ADMIN LOGOUT
# --------------------------------
@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("admin_login"))


# --------------------------------
# ✉️ EMAIL FUNCTION
# --------------------------------
def send_email(name, email, subject, message):
    EMAIL_ADDRESS = "vanishree0704@gmail.com"
    EMAIL_PASSWORD = "rchrdizmjnzvqpbj"   # app password (no spaces)

    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS
    msg["Subject"] = f"New Portfolio Message: {subject}"

    msg.set_content(
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Subject: {subject}\n\n"
        f"Message:\n{message}"
    )

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            print("Email sent successfully")
    except Exception as e:
        print("Email error:", e)


# -----------------------------
# START SERVER
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


