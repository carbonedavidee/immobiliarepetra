from flask import session
from flask_app import app
def generateFlashDic():
    if not session.get("flash-dic"):
            session["flash-dic"] = {}

def setFlashDic(key, value):
    session["flash-dic"][key] = value


@app.route("/get-flash-dic")
def get_flash_dic():
    generateFlashDic()
    return session["flash-dic"]

@app.route("/delete-flash-dic")
def delete_flash_dic():
    generateFlashDic()
    session.pop("flash-dic", None)
    return ""