from flask_mail import Message
from flask_app import mail , app
from flask import request , redirect

@app.route("/send-email",methods=["GET","POST"])
def send_email():
    subject = request.form["subject"] if request.form["subject"] else ""
    name = request.form["nm"] if request.form["nm"] else ""
    email = request.form["email"] if request.form["email"] else ""
    body = request.form["body"] if request.form["body"] else ""
    msg = Message(
        subject=subject,
        sender="immobiliarepetraa@gmail.com",
        recipients=["filippocarroccia@gmail.com"]
        )
    msg.html = f"Il/La signor/a {name} con l'indirizzo email {email} scrive il seguente messaggio.<br>{body}"
    mail.send(msg)
    return redirect(request.referrer)

