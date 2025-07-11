from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    vehicles = db.relationship('Vehicle', backref='owner', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    registration_number = db.Column(db.String(20), unique=True, nullable=False)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    vehicle_type = db.Column(db.String(20), nullable=False)  # MCWG, LMV, etc.
    fuel_type = db.Column(db.String(20), nullable=False)  # Petrol, Diesel, Electric
    purchase_date = db.Column(db.Date, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # RC Details
    engine_number = db.Column(db.String(50))
    chassis_number = db.Column(db.String(50))
    registration_date = db.Column(db.Date)
    rto_office = db.Column(db.String(50))
    rc_expiry_date = db.Column(db.Date)
    seating_capacity = db.Column(db.Integer)
    unladen_weight = db.Column(db.Integer)
    gross_vehicle_weight = db.Column(db.Integer)
    rc_document_photo = db.Column(db.String(200))
    
    # Insurance Details
    insurance_company = db.Column(db.String(100))
    policy_number = db.Column(db.String(50))
    policy_type = db.Column(db.String(30))  # Comprehensive, Third Party
    insurance_start_date = db.Column(db.Date)
    insurance_expiry_date = db.Column(db.Date)
    premium_amount = db.Column(db.Float)
    agent_name = db.Column(db.String(100))
    agent_contact = db.Column(db.String(20))
    idv_amount = db.Column(db.Float)  # Insured Declared Value
    insurance_document_photo = db.Column(db.String(200))
    
    # Owner Details
    owner_name = db.Column(db.String(100))
    owner_father_name = db.Column(db.String(100))
    owner_address = db.Column(db.Text)
    owner_phone = db.Column(db.String(20))
    owner_email = db.Column(db.String(100))
    owner_dob = db.Column(db.Date)
    driving_license_number = db.Column(db.String(50))
    dl_expiry_date = db.Column(db.Date)
    dl_document_photo = db.Column(db.String(200))
    
    expenses = db.relationship('Expense', backref='vehicle', lazy=True, cascade='all, delete-orphan')
    
    def has_expired_documents(self):
        """Check if any documents are expired or expiring soon (within 30 days)"""
        from datetime import date, timedelta
        today = date.today()
        alert_date = today + timedelta(days=30)
        
        expired_docs = []
        if self.rc_expiry_date and self.rc_expiry_date <= alert_date:
            expired_docs.append(('RC', self.rc_expiry_date))
        if self.insurance_expiry_date and self.insurance_expiry_date <= alert_date:
            expired_docs.append(('Insurance', self.insurance_expiry_date))
        if self.dl_expiry_date and self.dl_expiry_date <= alert_date:
            expired_docs.append(('Driving License', self.dl_expiry_date))
        
        return expired_docs
    
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