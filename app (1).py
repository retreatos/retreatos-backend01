from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# הגדרת חיבור לבסיס הנתונים
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# דוגמה למודל משתמש
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)

# יצירת הטבלאות בקונטקסט האפליקציה
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return "🎉 RetreatOS backend is running!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
