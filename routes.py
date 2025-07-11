from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from models import db, Vehicle, Expense, ExpenseCategory
from forms import VehicleForm, ExpenseForm, CategoryForm
import os
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    vehicles = Vehicle.query.all()
    recent_expenses = Expense.query.order_by(Expense.created_at.desc()).limit(5).all()
    return render_template('index.html', vehicles=vehicles, recent_expenses=recent_expenses)

@main_bp.route('/vehicles')
def vehicles():
    vehicles = Vehicle.query.all()
    return render_template('vehicles.html', vehicles=vehicles)

@main_bp.route('/vehicles/add', methods=['GET', 'POST'])
def add_vehicle():
    form = VehicleForm()
    if form.validate_on_submit():
        # Convert string date to datetime object
        purchase_date = datetime.strptime(form.purchase_date.data, '%d/%m/%Y').date()
        
        vehicle = Vehicle(
            registration_number=form.registration_number.data,
            make=form.make.data,
            model=form.model.data,
            year=form.year.data,
            vehicle_type=form.vehicle_type.data,
            fuel_type=form.fuel_type.data,
            purchase_date=purchase_date,
            purchase_price=form.purchase_price.data
        )
        db.session.add(vehicle)
        db.session.commit()
        flash('Vehicle added successfully!', 'success')
        return redirect(url_for('main.vehicles'))
    return render_template('add_vehicle.html', form=form)

@main_bp.route('/vehicles/<int:id>')
def vehicle_detail(id):
    vehicle = Vehicle.query.get_or_404(id)
    expenses = Expense.query.filter_by(vehicle_id=id).order_by(Expense.expense_date.desc()).all()
    total_expenses = sum(expense.amount for expense in expenses)
    return render_template('vehicle_detail.html', vehicle=vehicle, expenses=expenses, total_expenses=total_expenses)

@main_bp.route('/expenses')
def expenses():
    expenses = Expense.query.order_by(Expense.expense_date.desc()).all()
    return render_template('expenses.html', expenses=expenses)

@main_bp.route('/expenses/add', methods=['GET', 'POST'])
def add_expense():
    form = ExpenseForm()
    form.vehicle_id.choices = [(v.id, f"{v.registration_number} - {v.make} {v.model}") for v in Vehicle.query.all()]
    form.category_id.choices = [(c.id, c.name) for c in ExpenseCategory.query.all()]
    
    if form.validate_on_submit():
        filename = None
        if form.bill_photo.data:
            filename = save_bill_photo(form.bill_photo.data)
        
        # Convert string date to datetime object
        expense_date = datetime.strptime(form.expense_date.data, '%d/%m/%Y').date()
        
        expense = Expense(
            vehicle_id=form.vehicle_id.data,
            category_id=form.category_id.data,
            amount=form.amount.data,
            description=form.description.data,
            expense_date=expense_date,
            odometer_reading=form.odometer_reading.data,
            vendor_name=form.vendor_name.data,
            bill_photo=filename
        )
        db.session.add(expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('main.expenses'))
    
    return render_template('add_expense.html', form=form)

@main_bp.route('/categories')
def categories():
    categories = ExpenseCategory.query.all()
    return render_template('categories.html', categories=categories)

@main_bp.route('/categories/add', methods=['GET', 'POST'])
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = ExpenseCategory(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(category)
        db.session.commit()
        flash('Category added successfully!', 'success')
        return redirect(url_for('main.categories'))
    return render_template('add_category.html', form=form)

def save_bill_photo(photo):
    filename = secure_filename(photo.filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
    filename = timestamp + filename
    upload_folder = current_app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    photo.save(os.path.join(upload_folder, filename))
    return filename