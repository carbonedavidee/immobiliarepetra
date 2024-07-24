from flask import send_from_directory , request , redirect , url_for
from flask_app import app , db , bcrypt 
from flask_app.flash_manager import generateFlashDic , setFlashDic
from flask_app.models import User
from flask_login import login_user , current_user , logout_user , login_required


@app.route("/admin")
@login_required
def admin():
        generateFlashDic()
        setFlashDic("currentUser", current_user.username)
        return send_from_directory(app.static_folder,"index.html")

@app.route("/login", methods=["POST" , "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin"))
    if request.method == "POST":
        username = request.form["nm"]
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, request.form["pw"]):
            login_user(user, remember=False)
            return redirect(url_for("admin"))
        else:
            generateFlashDic()
            setFlashDic("errorBannerMessage","Note utente e/o password errati. Riprova")
    return send_from_directory(app.static_folder,"index.html")

@login_required
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@login_required
@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form["nm"]
        if User.query.filter_by(username=username).first():
            generateFlashDic()
            setFlashDic("registerErrorBannerMessage","Questo nome utente è già registrato. Cambia  nome utente e riprova.")
        else:
            hashed_password = bcrypt.generate_password_hash(request.form["pw"]).decode("utf-8")
            user = User(username=username, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            #display success
            generateFlashDic()
            setFlashDic("registerSuccessBannerMessage","L'utente è stato registrato con successo.")
        return redirect(url_for("admin"))
        

@login_required
@app.route("/change-password", methods=["POST" , "GET"])
def change_password():
    user = User.query.filter_by(username=current_user.username).first()
    if user:
        user.password = bcrypt.generate_password_hash(request.form["pw"]).decode("utf-8")
        db.session.commit() 
        generateFlashDic()
        setFlashDic("changePasswordSuccessBannerMessage","Password modificata correttamente.")
    else:
        generateFlashDic()
        setFlashDic("changePasswordErrorBannerMessage","Si è verificato un errore. Riprova più tardi.")
    return redirect(url_for("admin"))

@login_required
@app.route("/delete-account", methods=["POST", "GET"])
def delete_account():
    user = User.query.filter_by(username=current_user.username).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("home"))


#dev routes
@app.route("/dev-login")
def devlogin():
    login_user(User.query.filter_by(username="carbonedavide").first())
    return redirect(url_for("admin"))

@app.route("/dev-logout")
def devlogout():
    logout_user()
    return redirect(url_for("login"))
