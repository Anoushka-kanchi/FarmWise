from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify
)

from werkzeug.utils import secure_filename

from flask_cors import CORS

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

# Enable CORS for Streamlit integration
CORS(app)


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
# API ENDPOINTS FOR STREAMLIT
# ==========================================

@app.route("/api/crops", methods=["GET"])
def api_get_crops():
    """Get all crop listings"""
    db = SessionLocal()
    crops = db.query(CropListing).all()
    db.close()
    
    crops_data = []
    for crop in crops:
        crops_data.append({
            "id": crop.id,
            "farmer_name": crop.farmer_name,
            "crop": crop.crop,
            "category": crop.category,
            "price": crop.price,
            "quantity": crop.quantity,
            "location": crop.location,
            "description": crop.description,
            "image_filename": crop.image_filename,
            "date_listed": crop.date_listed.isoformat() if crop.date_listed else None
        })
    
    return jsonify(crops_data)


@app.route("/api/crops/<int:crop_id>", methods=["GET"])
def api_get_crop(crop_id):
    """Get single crop listing"""
    db = SessionLocal()
    crop = db.query(CropListing).filter(CropListing.id == crop_id).first()
    db.close()
    
    if not crop:
        return jsonify({"error": "Crop not found"}), 404
    
    return jsonify({
        "id": crop.id,
        "farmer_name": crop.farmer_name,
        "crop": crop.crop,
        "category": crop.category,
        "price": crop.price,
        "quantity": crop.quantity,
        "location": crop.location,
        "description": crop.description,
        "image_filename": crop.image_filename,
        "date_listed": crop.date_listed.isoformat() if crop.date_listed else None
    })


@app.route("/api/crops", methods=["POST"])
def api_add_crop():
    """Add new crop listing via API"""
    data = request.get_json()
    
    farmer_name = data.get("farmer_name")
    crop = data.get("crop")
    category = data.get("category")
    quantity = data.get("quantity")
    price = data.get("price")
    location = data.get("location")
    description = data.get("description")
    
    # Validate required fields
    if not all([farmer_name, crop, quantity, price]):
        return jsonify({"error": "Missing required fields"}), 400
    
    try:
        quantity = float(quantity)
        price = float(price)
    except ValueError:
        return jsonify({"error": "Quantity and Price must be valid numbers"}), 400
    
    db = SessionLocal()
    
    new_crop = CropListing(
        farmer_name=farmer_name,
        crop=crop,
        category=category,
        quantity=quantity,
        price=price,
        location=location,
        description=description,
        image_filename=data.get("image_filename")
    )
    
    db.add(new_crop)
    db.commit()
    crop_id = new_crop.id
    db.close()
    
    return jsonify({
        "message": "Crop added successfully",
        "crop_id": crop_id
    }), 201


@app.route("/api/products", methods=["GET"])
def api_get_products():
    """Get all farming products"""
    db = SessionLocal()
    products = db.query(FarmingProduct).all()
    db.close()
    
    products_data = []
    for product in products:
        products_data.append({
            "id": product.id,
            "title": product.title,
            "category": product.category,
            "price": product.price,
            "quantity": product.quantity,
            "seller": product.seller,
            "description": product.description,
            "image_filename": product.image_filename
        })
    
    return jsonify(products_data)


@app.route("/api/buy", methods=["POST"])
def api_buy_product():
    """Record a purchase"""
    data = request.get_json()
    
    crop_id = data.get("crop_id")
    quantity = data.get("quantity", 1)
    
    db = SessionLocal()
    crop = db.query(CropListing).filter(CropListing.id == crop_id).first()
    
    if not crop:
        db.close()
        return jsonify({"error": "Crop not found"}), 404
    
    # Update quantity
    crop.quantity -= quantity
    db.commit()
    db.close()
    
    return jsonify({
        "message": "Purchase successful",
        "crop": crop.crop,
        "seller": crop.farmer_name,
        "quantity": quantity
    }), 200


# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )