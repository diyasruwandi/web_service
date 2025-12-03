# web_service

Sebuah aplikasi web sederhana berbasis Flask untuk menampilkan dan mengelola artikel, dengan autentikasi user dan admin serta chatbot sederhana berbasis aturan.

**Ringkasan**
- **Framework:** `Flask`
- **Database:** MySQL (dikoneksikan via `PyMySQL` + `Flask-SQLAlchemy`)
- **Auth / Password hashing:** `Flask-Bcrypt` / `werkzeug.security`

**File penting**
- `app.py`: entrypoint aplikasi
- `config.py`: konfigurasi aplikasi (secret key & database URI)
- `requirements.txt`: daftar dependency pip
- `buat_admin.py`: util untuk membuat akun admin dari CLI
- `mesin_chatbot.py`: mesin chatbot berbasis `rules.json`
- `templates/` dan `static/`: view dan styling

Instalasi
---------
1. (Opsional) buat virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Pasang dependency

```bash
python -m pip install -r requirements.txt
```

Konfigurasi database
---------------------
- `config.py` saat ini menunjuk ke:
  `mysql+pymysql://webuser:Password123!@localhost/web_db`
- Pastikan database MySQL `web_db` sudah dibuat dan user `webuser` memiliki akses yang sesuai, atau ganti `SQLALCHEMY_DATABASE_URI` sesuai lingkungan Anda.

Menjalankan aplikasi
--------------------

```bash
python app.py
```

Ini akan membuat tabel (jika belum ada) pada folder kerja karena `db.create_all()` dipanggil saat `__main__`.

Membuat akun admin
-------------------
Jalankan util untuk membuat admin dari CLI:

```bash
python buat_admin.py
```

Ikuti prompt untuk memasukkan email dan password admin.

API / Routes utama
------------------
- `GET /` atau `GET /login` — halaman login
- `GET /register`, `POST /register` — registrasi user
- `GET /user/dashboard` — dashboard user (lihat artikel)
- `GET /admin/dashboard` — dashboard admin
- CRUD artikel tersedia di route `/admin/article` (API) dan halaman admin di `/admin/articles`.
- Chatbot endpoint: `POST /chatbot` (kirim JSON `{ "message": "..." }`)

Catatan tambahan
----------------
- `requirements.txt` dibuat berdasarkan import di kode; versi paket tidak dipaku. Jika Anda ingin pin versi yang pasti, jalankan `pip freeze > requirements.txt` dari environment yang sudah terpasang paket lalu beri tahu saya untuk menggabungkannya.
- Jika ada file eksternal/extension yang hilang (mis. `extensions.py` referensi di `models/admin_model.py`), sesuaikan atau perbaiki import agar konsisten.

Butuh bantuan lebih lanjut?
- Mau saya pin versi paket dari environment Anda sekarang?
- Atau jalankan `python -m pip install -r requirements.txt` di sini untuk verifikasi? Tuliskan pilihan Anda.
