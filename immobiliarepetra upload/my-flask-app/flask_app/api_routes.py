from flask_app import app , db
from flask_login import login_required , current_user
from flask_app.models import Item, Img , Pdf
from flask import request , Response
from flask_app.flash_manager import generateFlashDic , setFlashDic
from werkzeug.utils import secure_filename



@app.route("/api-preview")
def api_preview():
    data = []
    items = Item.query.all()
    for item in items:
        dic = {}
        dic["id"] = item.id
        dic["category"] = item.category
        dic["tipology"] = item.tipology
        dic["title"] = item.title
        dic["price"] = item.price
        dic["city"] = item.city
        dic["bed_rooms"] = item.bed_rooms
        dic["size"] = item.size
        dic["bath_rooms"] = item.bath_rooms
        dic["floor"] = item.floor
        dic["green_houses"] = item.green_houses
        dic["rooms"] = item.rooms
        dic["fixed_image"] = item.fixed_image
        data.append(dic)
    return data

@app.route("/",defaults={"id":1})
@app.route("/api-details/<id>")
def api_details(id):
    item = Item.query.filter_by(id=id).first()
    dic = {}
    dic["id"] = item.id
    dic["title"] = item.title
    dic["description"] = item.description
    dic["price"] = item.price
    dic["category"] = item.category
    dic["tipology"] = item.tipology
    dic["address"] = item.address
    dic["city"] = item.city
    dic["zone"] = item.zone
    dic["on_home"] = item.on_home
    dic["maps"] = item.maps
    dic["street_view"] = item.street_view
    dic["pdf"] = item.pdf
    dic["video"] = item.video
    dic["bed_rooms"] = item.bed_rooms
    dic["size"] = item.size
    dic["bath_rooms"] = item.bath_rooms
    dic["others"] = item.others
    dic["images"] = item.images
    dic["fixed_image"] = item.fixed_image
    dic["floor"] = item.floor
    dic["green_houses"] = item.green_houses
    dic["rooms"] = item.rooms
    return dic

@app.route("/api-admin-fetch")
@login_required
def api_admin_fetch():
    data = []
    items = Item.query.all()
    for item in items:
        dic = {}
        dic["id"] = item.id
        dic["title"] = item.title
        dic["description"] = item.description
        dic["price"] = item.price
        dic["category"] = item.category
        dic["tipology"] = item.tipology
        dic["address"] = item.address
        dic["city"] = item.city
        dic["zone"] = item.zone
        dic["on_home"] = item.on_home
        dic["maps"] = item.maps
        dic["street_view"] = item.street_view
        dic["pdf"] = item.pdf
        dic["video"] = item.video
        dic["bed_rooms"] = item.bed_rooms
        dic["size"] = item.size
        dic["bath_rooms"] = item.bath_rooms
        dic["others"] = item.others
        dic["images"] = item.images
        dic["fixed_image"] = item.fixed_image
        dic["floor"] = item.floor
        dic["green_houses"] = item.green_houses
        dic["rooms"] = item.rooms
        data.append(dic)
    return data

@app.route("/api-admin-push", methods=["GET","POST"])
@login_required
def api_admin_push():
    data = request.json
    #clear item db
    items = Item.query.all()
    for item in items:
        db.session.delete(item)
    #add items from data=[{"example":"example"}, {"example":"example"}]
    for json_data in data:
        maps = json_data["maps"]
        maps = maps.replace('<iframe src="','')
        maps = maps.replace('" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>','')
        street_view = json_data["street_view"]
        street_view = street_view.replace('<iframe src="','')
        street_view = street_view.replace('" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>','')
        print(street_view)
        video = json_data["video"]
        video = video.replace('<iframe width="560" height="315" src="','')
        video = video.replace('" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>','')
        print(video)

        others = json_data["others"]
        def othersFilter(other):
            if other[0] == "" or other[1] == "":
                return False
            else:
                return True
        othersFiltered = filter(othersFilter,others)
        others = []
        for other in othersFiltered:
            others.append(other)

        item = Item(id=json_data["id"],title=json_data["title"],description=json_data["description"],price=json_data["price"],category=json_data["category"],tipology=json_data["tipology"],address=json_data["address"],city=json_data["city"],zone=json_data["zone"],on_home=json_data["on_home"],maps=maps,street_view=street_view,pdf=json_data["pdf"],video=video,bed_rooms=json_data["bed_rooms"],size=json_data["size"],bath_rooms=json_data["bath_rooms"],floor=json_data["floor"],rooms=json_data["rooms"],green_houses=json_data["green_houses"] ,others=others,images=json_data["images"],fixed_image=json_data["fixed_image"],)
        db.session.add(item)

    items = Item.query.all()
    images = Img.query.all()
    pdfs = Pdf.query.all()
    for image in images:
        delete = True
        for item in items:
            if image.name in item.images:
                delete = False
        if delete == True:
            db.session.delete(image)
    
    for pdf in pdfs:
        delete = True
        for item in items:
            if pdf.name == item.pdf:
                delete = False
        if delete == True:
            db.session.delete(pdf)



    
    db.session.commit()
    generateFlashDic()
    setFlashDic("pushDataSuccessBannerMessage","Modifiche salvate correttamente.")
    setFlashDic("currentUser", current_user.username)
    return "Success"

@login_required
@app.route("/upload-image", methods=["POST"])
def upload_image():
    pics = request.files.getlist("file")
    for pic in pics:
        if not pic:
            return 'No pic uploaded!', 400

        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        if not filename or not mimetype:
            return 'Bad upload!', 400

        img = Img(img=pic.read(), name=filename, mimetype=mimetype)
        db.session.add(img)
    db.session.commit()

    return 'Img Uploaded!', 200

@app.route("/images/<image>")
def get_image(image):
    img = Img.query.filter_by(name=image).first()
    if not img:
            return 'Img Not Found!', 404

    return Response(img.img, mimetype=img.mimetype)

@app.route("/get-server-images")
def get_server_images():
    data = []
    images = Img.query.all()
    for image in images:
        data.append(image.name)
    return data

@login_required
@app.route("/upload-pdf", methods=["POST"])
def upload_pdf():
    pdfs = request.files.getlist("file")
    for pdf in pdfs:
        if not pdf:
            return 'No pdf uploaded!', 400

        filename = secure_filename(pdf.filename)
        mimetype = pdf.mimetype
        if not filename or not mimetype:
            return 'Bad upload!', 400

        pdf1 = Pdf(pdf=pdf.read(), name=filename, mimetype=mimetype)
        db.session.add(pdf1)
    db.session.commit()

    return 'Pdf Uploaded!', 200

@app.route("/pdf/<pdf>")
def get_pdf(pdf):
    pdf = Pdf.query.filter_by(name=pdf).first()
    if not pdf:
            return 'Img Not Found!', 404

    return Response(pdf.pdf, mimetype=pdf.mimetype)

@app.route("/get-server-pdf")
def get_server_pdf():
    data = []
    pdfs = Pdf.query.all()
    for pdf in pdfs:
        data.append(pdf.name)
    return data