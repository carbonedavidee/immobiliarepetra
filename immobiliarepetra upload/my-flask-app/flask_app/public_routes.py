from flask import send_from_directory
from flask_app import app


@app.route("/",defaults={"id":""})
@app.route("/<id>")
def home(id):
    return send_from_directory(app.static_folder,"index.html")
