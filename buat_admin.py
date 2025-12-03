from app import app
from models.user import db, User, bcrypt

# Jalankan dalam context Flask
with app.app_context():

    print("=== Create Admin Account ===")

    # Input email admin
    email = input("Masukkan email admin: ")

    # Input password admin
    password_input = input("Masukkan password admin: ")

    # Generate hash bcrypt
    password_hashed = bcrypt.generate_password_hash(password_input).decode()

    # Buat user baru dengan role admin
    admin = User(email=email, password=password_hashed, role="admin")

    # Simpan ke database
    db.session.add(admin)
    db.session.commit()

    print("\nAdmin berhasil dibuat!")
    print("Email :", email)
    print("Password (plain) :", password_input)
    print("Password (hash)  :", password_hashed)
