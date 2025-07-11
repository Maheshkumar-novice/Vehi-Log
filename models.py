from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registration_number = db.Column(db.String(20), unique=True, nullable=False)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    vehicle_type = db.Column(db.String(20), nullable=False)  # MCWG, LMV, etc.
    fuel_type = db.Column(db.String(20), nullable=False)  # Petrol, Diesel, Electric
    purchase_date = db.Column(db.Date, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    expenses = db.relationship('Expense', backref='vehicle', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Vehicle {self.registration_number}>'

class ExpenseCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    
    expenses = db.relationship('Expense', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<ExpenseCategory {self.name}>'

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('expense_category.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    expense_date = db.Column(db.Date, nullable=False)
    odometer_reading = db.Column(db.Integer)
    vendor_name = db.Column(db.String(100))
    bill_photo = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Expense {self.amount} for {self.vehicle.registration_number}>'