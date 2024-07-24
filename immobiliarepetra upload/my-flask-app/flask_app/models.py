from flask_app import db , login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)
    def __repr__(self):
        return f"User('{self.username}' , '{self.password}')"
    

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String ,unique=True, nullable=False)
    description = db.Column(db.String , nullable=False) 
    price = db.Column(db.Float , nullable=False)
    category = db.Column(db.String , nullable=False)
    tipology = db.Column(db.String , nullable=False)
    address = db.Column(db.String , nullable=False)
    city = db.Column(db.String , nullable=False)
    zone = db.Column(db.String , nullable=False)
    on_home = db.Column(db.Boolean , nullable=False)
    maps = db.Column(db.String , nullable=False)
    street_view = db.Column(db.String , nullable=False)
    pdf = db.Column(db.String ,nullable=False)
    video = db.Column(db.String ,nullable=False)
    bed_rooms = db.Column(db.Integer,  nullable=True)
    size = db.Column(db.Integer, nullable=True)
    bath_rooms = db.Column(db.Integer, nullable=True)
    floor = db.Column(db.Integer, nullable=True)
    rooms = db.Column(db.Integer, nullable=True)
    green_houses = db.Column(db.Integer, nullable=True)
    others = db.Column(db.PickleType,  nullable=False) 
    images = db.Column(db.PickleType,  nullable=False)
    fixed_image = db.Column(db.String,  nullable=False) 

    def __repr__(self):
        return f"Item('{self.id}', '{self.title}' , '{self.price}')"

class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, unique=True, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)

class Pdf(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pdf = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, unique=True, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)

