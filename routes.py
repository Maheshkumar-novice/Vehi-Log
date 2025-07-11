from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from models import db, Vehicle, Expense, ExpenseCategory
from forms import VehicleForm, ExpenseForm, CategoryForm
import os
from datetime import datetime

vehi_log_bp = Blueprint('vehi_log', __name__)

@vehi_log_bp.route('/')
def vehi_log_index():
    vehicles = Vehicle.query.all()
    recent_expenses = Expense.query.order_by(Expense.created_at.desc()).limit(5).all()
    return render_template('vehi_log_index.html', vehicles=vehicles, recent_expenses=recent_expenses)

@vehi_log_bp.route('/vehicles')
def vehi_log_vehicles():
    vehicles = Vehicle.query.all()
    return render_template('vehi_log_vehicles.html', vehicles=vehicles)

@vehi_log_bp.route('/vehicles/add', methods=['GET', 'POST'])
def vehi_log_add_vehicle():
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
        return redirect(url_for('vehi_log.vehi_log_vehicles'))
    return render_template('vehi_log_add_vehicle.html', form=form)

@vehi_log_bp.route('/vehicles/<int:id>')
def vehi_log_vehicle_detail(id):
    vehicle = Vehicle.query.get_or_404(id)
    expenses = Expense.query.filter_by(vehicle_id=id).order_by(Expense.expense_date.desc()).all()
    total_expenses = sum(expense.amount for expense in expenses)
    return render_template('vehi_log_vehicle_detail.html', vehicle=vehicle, expenses=expenses, total_expenses=total_expenses)

@vehi_log_bp.route('/expenses')
def vehi_log_expenses():
    expenses = Expense.query.order_by(Expense.expense_date.desc()).all()
    return render_template('vehi_log_expenses.html', expenses=expenses)

@vehi_log_bp.route('/expenses/add', methods=['GET', 'POST'])
def vehi_log_add_expense():
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
        return redirect(url_for('vehi_log.vehi_log_expenses'))
    
    return render_template('vehi_log_add_expense.html', form=form)

@vehi_log_bp.route('/categories')
def vehi_log_categories():
    categories = ExpenseCategory.query.all()
    return render_template('vehi_log_categories.html', categories=categories)

@vehi_log_bp.route('/categories/add', methods=['GET', 'POST'])
def vehi_log_add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = ExpenseCategory(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(category)
        db.session.commit()
        flash('Category added successfully!', 'success')
        return redirect(url_for('vehi_log.vehi_log_categories'))
    return render_template('vehi_log_add_category.html', form=form)

# Information Pages
@vehi_log_bp.route('/info')
def vehi_log_info_index():
    return render_template('vehi_log_info/index.html')

@vehi_log_bp.route('/info/maintenance-guide')
def vehi_log_maintenance_guide():
    return render_template('vehi_log_info/maintenance_guide.html')

@vehi_log_bp.route('/info/expense-categories')
def vehi_log_expense_categories_guide():
    return render_template('vehi_log_info/expense_categories.html')

@vehi_log_bp.route('/info/rto-information')
def vehi_log_rto_information():
    return render_template('vehi_log_info/rto_information.html')

@vehi_log_bp.route('/info/fuel-efficiency')
def vehi_log_fuel_efficiency():
    return render_template('vehi_log_info/fuel_efficiency.html')

@vehi_log_bp.route('/info/insurance-guide')
def vehi_log_insurance_guide():
    return render_template('vehi_log_info/insurance_guide.html')

@vehi_log_bp.route('/info/documents-checklist')
def vehi_log_documents_checklist():
    return render_template('vehi_log_info/documents_checklist.html')

@vehi_log_bp.route('/info/emergency-contacts')
def vehi_log_emergency_contacts():
    return render_template('vehi_log_info/emergency_contacts.html')

@vehi_log_bp.route('/info/tax-registration')
def vehi_log_tax_registration():
    return render_template('vehi_log_info/tax_registration.html')

@vehi_log_bp.route('/info/seasonal-maintenance')
def vehi_log_seasonal_maintenance():
    return render_template('vehi_log_info/seasonal_maintenance.html')

@vehi_log_bp.route('/info/cost-analysis')
def vehi_log_cost_analysis():
    return render_template('vehi_log_info/cost_analysis.html')

def save_bill_photo(photo):
    filename = secure_filename(photo.filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
    filename = timestamp + filename
    upload_folder = current_app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    photo.save(os.path.join(upload_folder, filename))
    return filename