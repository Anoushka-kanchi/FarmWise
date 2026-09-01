from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)

from werkzeug.utils import secure_filename

import os

import pandas as pd

from database.db import (
    Base,
    engine,
    SessionLocal,
    CropListing,
    FarmingProduct
)


app = Flask(__name__)


# ==========================================
# CONFIGURATION
# ==========================================

app.config['UPLOAD_FOLDER'] = os.path.join(
    app.root_path,
    'static',
    'uploads'
)

# Create upload folder if it doesn't exist
os.makedirs(
    app.config['UPLOAD_FOLDER'],
    exist_ok=True
)


# ==========================================
# CREATE DATABASE
# ==========================================

Base.metadata.create_all(
    bind=engine
)


# ==========================================
# LOAD CSV
# ==========================================

CSV_FILE = "dataset.csv"


def load_csv():

    try:

        df = pd.read_csv(CSV_FILE)

        return df

    except Exception:

        return pd.DataFrame()


# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ==========================================
# FARMER DASHBOARD
# ==========================================

@app.route("/farmer")
def farmer():

    db = SessionLocal()

    listings = db.query(
        CropListing
    ).all()

    products = db.query(
        FarmingProduct
    ).all()

    db.close()

    return render_template(
        "farmer.html",
        listings=listings,
        products=products
    )


# ==========================================
# FARMER SELL PAGE
# ==========================================

@app.route("/farmer/sell")
def farmer_sell():

    return render_template(
        "farmer_sell.html"
    )


# ==========================================
# ADD CROP
# ==========================================

@app.route(
    "/farmer/add-crop",
    methods=["POST"]
)
def add_crop():

    farmer_name = request.form.get("farmer_name")
    crop = request.form.get("crop")
    category = request.form.get("category")
    quantity = request.form.get("quantity")
    price = request.form.get("price")
    location = request.form.get("location")
    description = request.form.get("description")

    # Validate required fields
    if not all([farmer_name, crop, quantity, price]):
        return "Missing required fields", 400

    try:
        quantity = float(quantity)
        price = float(price)
    except ValueError:
        return "Quantity and Price must be valid numbers", 400


    # ==========================================
    # IMAGE UPLOAD
    # ==========================================

    image = request.files.get("image")

    image_filename = None


    if image and image.filename:

        image_filename = secure_filename(
            image.filename
        )


        upload_folder = os.path.join(
            app.root_path,
            "static",
            "uploads"
        )


        os.makedirs(
            upload_folder,
            exist_ok=True
        )


        image.save(
            os.path.join(
                upload_folder,
                image_filename
            )
        )


    # ==========================================
    # DATABASE
    # ==========================================

    db = SessionLocal()


    new_crop = CropListing(

        farmer_name=farmer_name,

        crop=crop,

        category=category,

        quantity=quantity,

        price=price,

        location=location,

        description=description,

        image_filename=image_filename

    )


    db.add(
        new_crop
    )

    db.commit()

    db.close()


    return redirect(
        url_for("farmer")
    )
# ==========================================
# FARMER BUY PAGE
# ==========================================

@app.route("/farmer/buy")
def farmer_buy():

    db = SessionLocal()

    products = db.query(
        FarmingProduct
    ).all()

    db.close()


    return render_template(
        "farmer_buy.html",
        products=products
    )


# ==========================================
# CONSUMER
# ==========================================

@app.route("/consumer")
def consumer():

    db = SessionLocal()

    crops = db.query(
        CropListing
    ).all()

    db.close()


    return render_template(
        "consumer.html",
        crops=crops
    )


# ==========================================
# BUY CROP
# ==========================================

@app.route(
    "/consumer/buy/<int:crop_id>",
    methods=["POST"]
)
def buy_crop(crop_id):

    db = SessionLocal()

    crop = db.query(
        CropListing
    ).filter(
        CropListing.id == crop_id
    ).first()


    if crop:

        print(
            f"Consumer purchased "
            f"{crop.crop} from "
            f"{crop.farmer_name}"
        )


    db.close()


    return redirect(
        url_for("consumer")
    )


# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )