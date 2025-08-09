from flask import Flask, jsonify, redirect, url_for, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth
import os

# -------------------- App & Config --------------------
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")

# DB (uses SQLite by default; set DATABASE_URL for Postgres on Render)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///local.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Cookies/Sessions for cross-site (frontend <-> backend) if needed
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = True

db = SQLAlchemy(app)

# CORS: set FRONTEND_ORIGIN env to your frontend URL (e.g. https://retreatos-frontend.onrender.com)
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "")
_cors_origins = [FRONTEND_ORIGIN] if FRONTEND_ORIGIN else ["*"]  # change to specific origin in production
CORS(app, supports_credentials=True, resources={r"/*": {"origins": _cors_origins}})

# -------------------- OAuth (Google) --------------------
from authlib.integrations.flask_client import OAuth
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'},
    authorize_params={'access_type': 'offline', 'prompt': 'consent'},
)

# -------------------- Cloudinary (Image storage) --------------------
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# -------------------- Models --------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)

    images = db.relationship("GalleryImage", backref="user", lazy=True)

class GalleryImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)

# -------------------- Routes --------------------
@app.route("/")
def home():
    return jsonify(message="RetreatOS Backend OK", logged_in=("email" in session))

@app.route("/healthz")
def health():
    return jsonify(status="ok")

@app.route("/login")
def login():
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route("/authorize")
def authorize():
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    email = user_info.get('email')
    if not email:
        return jsonify(error="Google OAuth failed (no email)"), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email)
        db.session.add(user)
        db.session.commit()

    session['email'] = email
    return redirect(os.getenv("POST_LOGIN_REDIRECT", "/ok"))

@app.route("/ok")
def ok_page():
    return jsonify(message="Logged in", email=session.get("email"))

@app.route("/logout", methods=["POST", "GET"])
def logout():
    session.clear()
    return jsonify(message="Logged out")

@app.route("/upload-image", methods=["POST"])
def upload_image():
    if 'email' not in session:
        return jsonify(error="Not logged in"), 401

    if 'file' not in request.files:
        return jsonify(error="No file uploaded"), 400

    file = request.files['file']
    if not file:
        return jsonify(error="Empty file"), 400

    # Upload to Cloudinary
    try:
        res = cloudinary.uploader.upload(file, folder=os.getenv("CLOUDINARY_FOLDER", "retreatos"))
        image_url = res.get('secure_url')
    except Exception as e:
        return jsonify(error=f"Upload failed: {e}"), 500

    user = User.query.filter_by(email=session['email']).first()
    img = GalleryImage(user_id=user.id, image_url=image_url)
    db.session.add(img)
    db.session.commit()

    return jsonify(message="Uploaded", url=image_url)

@app.route("/my-gallery", methods=["GET"])
def my_gallery():
    if 'email' not in session:
        return jsonify(error="Not logged in"), 401

    user = User.query.filter_by(email=session['email']).first()
    images = GalleryImage.query.filter_by(user_id=user.id).all()
    return jsonify(images=[{"id": i.id, "url": i.image_url} for i in images])

# Create tables at import-time (works with gunicorn)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
