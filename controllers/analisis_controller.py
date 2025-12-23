from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import pytesseract
import re
from PIL import Image
from models.bahan import Bahan
from models import db

# Load trained model & vectorizer
from services.model_loader import model, vectorizer

analysis = Blueprint("analysis", __name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "..", "uploads")

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

STOPWORDS = [
    "komposisi","komposisi:","Komposisi", "ingredients","untuk","pabrik","alamat","mengandung",
    "berat", "bersih", "netto", "diproduksi","disimpan","gunakan","kedaluwarsa","makanan","fasa",
    "oleh", "expired", "exp", "bpom","lihat","daftar","alergen","dapat","proses"
]

def clean_ingredients(text):
    text = text.lower()

    # ambil teks setelah kata "komposisi" (kalau ada)
    if "komposisi" in text:
        text = text.split("komposisi", 1)[1]

    # hapus angka & simbol
    text = re.sub(r'[^a-zA-Z,\n ]', '', text)

    # split jadi list
    raw_items = re.split(r'[,\n]', text)

    cleaned = []
    for item in raw_items:
        item = item.strip()
        if len(item) < 3:
            continue
        if any(stop in item for stop in STOPWORDS):
            continue
        cleaned.append(item)

    return list(set(cleaned))

def normalize_ingredient(text):
    text = text.lower()
    text = re.sub(r'\b(pasir|halus|cair|bubuk)\b', '', text)
    return text.strip()


# 1. Upload gambar → OCR → ambil teks komposisi
@analysis.route("/analysis/ocr", methods=["POST"])
def extract_text():
    if "image" not in request.files:
        return jsonify({"status": False, "message": "Image not found"}), 400

    file = request.files["image"]
    filename = secure_filename(file.filename)

    # upload_dir = "uploads"
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    save_path = os.path.join(UPLOAD_DIR, filename)
    file.save(save_path)

    # OCR ambil teks komposisi
    try:
        text = pytesseract.image_to_string(Image.open(save_path))

        ingredients = clean_ingredients(text)

    except Exception as e:

        return jsonify({"status": False, "message": str(e)}), 500

    results = []

    for item in ingredients:

        clean_item = normalize_ingredient(item)

        vector = vectorizer.transform([normalize_ingredient(item)])
        category = model.predict(vector)[0]

        bahan = Bahan.query.filter(Bahan.nama_bahan.like(f"%{clean_item}%")).first()

        results.append({
            "ingredient": item,
            "category": category, # "alami" / "sintetis"
            "informasi_kegunaan": bahan.informasi_kegunaan if bahan else "Informasi tidak ditemukan",
            "batas_wajar": bahan.batas_wajar if bahan else "Informasi tidak ditemukan",
            "dampak_negatif": bahan.dampak_negatif if bahan else "Informasi tidak ditemukan"
        })

    return jsonify({
        "status": True,
        "results": results,
        # "extracted_text": text,
        # "ingredients": ingredients
    }), 200


# 2. Klasifikasi bahan 
# @analysis.route("/analysis/classify", methods=["POST"])
# def classify_ingredients():
#     data = request.get_json()

#     if not data or "ingredients" not in data:
#         return jsonify({"status": False, "message": "Ingredients missing"}), 400

#     ingredients = data["ingredients"]  # array/list
#     results = []

#     for item in ingredients:
#         clean_text = normalize_ingredient(item)

#         # Vectorize
#         vector = vectorizer.transform([clean_text])

#         # Predict
#         prediction = model.predict(vector)[0]

#         #cari di db bahan
#         bahan = Bahan.query.filter(Bahan.nama_bahan.like(f"%{clean_text}%")).first()
        

#         results.append({
#             "ingredient": item,
#             "category": prediction, # "alami" / "sintetis"
#             "informasi_kegunaan": bahan.informasi_kegunaan if bahan else "Informasi tidak ditemukan",
#             "batas_wajar": bahan.batas_wajar if bahan else "Informasi tidak ditemukan",
#             "dampak_negatif": bahan.dampak_negatif if bahan else "Informasi tidak ditemukan"
            
#         })

#     return jsonify({
#         "status": True,
#         "results": results
#     }), 200
