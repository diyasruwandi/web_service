from models import db

class Bahan(db.Model):
    __tablename__ = "bahan"

    id = db.Column(db.Integer, primary_key=True)
    nama_bahan = db.Column(db.String(255), nullable=False)
    kategori = db.Column(db.String(255))
    dampak_negatif = db.Column(db.Text)
    batas_wajar = db.Column(db.String(255))
    informasi_kegunaan = db.Column(db.Text)
