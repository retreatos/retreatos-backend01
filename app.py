
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import datetime
import os

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///retreatos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Retreat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    location = db.Column(db.String(100))
    date = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    retreat_id = db.Column(db.Integer, db.ForeignKey('retreat.id'))

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    currency = db.Column(db.String(10))
    retreat_id = db.Column(db.Integer, db.ForeignKey('retreat.id'))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

@app.route('/')
def home():
    return "RetreatOS API Live"

@app.route('/api/retreats', methods=['GET'])
def get_retreats():
    data = Retreat.query.all()
    return jsonify([{
        'id': r.id, 'title': r.title, 'location': r.location,
        'date': r.date, 'created_at': r.created_at.isoformat()
    } for r in data])

@app.route('/api/retreats', methods=['POST'])
def create_retreat():
    data = request.get_json()
    r = Retreat(title=data['title'], location=data['location'], date=data['date'])
    db.session.add(r)
    db.session.commit()
    return jsonify({'id': r.id, 'title': r.title}), 201

@app.route('/api/retreats/<int:retreat_id>/guests', methods=['GET'])
def get_guests(retreat_id):
    data = Guest.query.filter_by(retreat_id=retreat_id).all()
    return jsonify([{'id': g.id, 'name': g.name, 'email': g.email} for g in data])

@app.route('/api/guests', methods=['POST'])
def add_guest():
    data = request.get_json()
    g = Guest(name=data['name'], email=data['email'], retreat_id=data['retreat_id'])
    db.session.add(g)
    db.session.commit()
    return jsonify({'id': g.id, 'name': g.name}), 201

@app.route('/api/payments', methods=['GET'])
def get_payments():
    data = Payment.query.all()
    return jsonify([{
        'id': p.id, 'amount': p.amount, 'currency': p.currency,
        'retreat_id': p.retreat_id, 'timestamp': p.timestamp.isoformat()
    } for p in data])

@app.route('/api/payments', methods=['POST'])
def add_payment():
    data = request.get_json()
    p = Payment(amount=data['amount'], currency=data['currency'], retreat_id=data['retreat_id'])
    db.session.add(p)
    db.session.commit()
    return jsonify({'id': p.id, 'amount': p.amount}), 201

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=5000)
