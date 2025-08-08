
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///retreatos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models (Retreat, Guest, Payment)
# Add Organizer (User) and Authentication here

@app.route('/')
def home():
    return "RetreatOS API Live with Full Stack Structure"

# ROUTES:
# - /api/auth (OAuth placeholder)
# - /api/retreats (Create/View retreats)
# - /api/dashboard (Organizer dashboard summary)
# - /api/payments (Stripe)
# - /api/messaging (WhatsApp/email placeholder)

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=5000)
