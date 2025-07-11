from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from models import db, Vehicle, Expense, ExpenseCategory, User
from forms import VehicleForm, ExpenseForm, CategoryForm, LoginForm, RegistrationForm
import os
from datetime import datetime

vehi_log_bp = Blueprint('vehi_log', __name__)

# Authentication routes
@vehi_log_bp.route('/login', methods=['GET', 'POST'])
def vehi_log_login():
    if current_user.is_authenticated:
        return redirect(url_for('vehi_log.vehi_log_index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('vehi_log.vehi_log_index'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('vehi_log_login.html', form=form)

@vehi_log_bp.route('/register', methods=['GET', 'POST'])
def vehi_log_register():
    if current_user.is_authenticated:
        return redirect(url_for('vehi_log.vehi_log_index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if username already exists
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
        else:
            user = User(username=form.username.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('vehi_log.vehi_log_login'))
    
    return render_template('vehi_log_register.html', form=form)

@vehi_log_bp.route('/logout')
@login_required
def vehi_log_logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('vehi_log.vehi_log_login'))

@vehi_log_bp.route('/')
@login_required
def vehi_log_index():
    vehicles = Vehicle.query.filter_by(user_id=current_user.id).all()
    recent_expenses = Expense.query.join(Vehicle).filter(Vehicle.user_id == current_user.id).order_by(Expense.created_at.desc()).limit(5).all()
    return render_template('vehi_log_index.html', vehicles=vehicles, recent_expenses=recent_expenses)

@vehi_log_bp.route('/vehicles')
@login_required
def vehi_log_vehicles():
    vehicles = Vehicle.query.filter_by(user_id=current_user.id).all()
    return render_template('vehi_log_vehicles.html', vehicles=vehicles)

@vehi_log_bp.route('/vehicles/add', methods=['GET', 'POST'])
@login_required
def vehi_log_add_vehicle():
    form = VehicleForm()
    if form.validate_on_submit():
        # Convert string dates to datetime objects
        purchase_date = datetime.strptime(form.purchase_date.data, '%d/%m/%Y').date()
        
        # Handle optional date fields
        registration_date = None
        if form.registration_date.data:
            registration_date = datetime.strptime(form.registration_date.data, '%d/%m/%Y').date()
        
        rc_expiry_date = None
        if form.rc_expiry_date.data:
            rc_expiry_date = datetime.strptime(form.rc_expiry_date.data, '%d/%m/%Y').date()
        
        insurance_start_date = None
        if form.insurance_start_date.data:
            insurance_start_date = datetime.strptime(form.insurance_start_date.data, '%d/%m/%Y').date()
        
        insurance_expiry_date = None
        if form.insurance_expiry_date.data:
            insurance_expiry_date = datetime.strptime(form.insurance_expiry_date.data, '%d/%m/%Y').date()
        
        owner_dob = None
        if form.owner_dob.data:
            owner_dob = datetime.strptime(form.owner_dob.data, '%d/%m/%Y').date()
        
        dl_expiry_date = None
        if form.dl_expiry_date.data:
            dl_expiry_date = datetime.strptime(form.dl_expiry_date.data, '%d/%m/%Y').date()
        
        vehicle = Vehicle(
            user_id=current_user.id,
            registration_number=form.registration_number.data,
            make=form.make.data,
            model=form.model.data,
            year=form.year.data,
            vehicle_type=form.vehicle_type.data,
            fuel_type=form.fuel_type.data,
            purchase_date=purchase_date,
            purchase_price=form.purchase_price.data,
            # RC Details
            engine_number=form.engine_number.data,
            chassis_number=form.chassis_number.data,
            registration_date=registration_date,
            rto_office=form.rto_office.data,
            rc_expiry_date=rc_expiry_date,
            seating_capacity=form.seating_capacity.data,
            unladen_weight=form.unladen_weight.data,
            gross_vehicle_weight=form.gross_vehicle_weight.data,
            # Insurance Details
            insurance_company=form.insurance_company.data,
            policy_number=form.policy_number.data,
            policy_type=form.policy_type.data,
            insurance_start_date=insurance_start_date,
            insurance_expiry_date=insurance_expiry_date,
            premium_amount=form.premium_amount.data,
            agent_name=form.agent_name.data,
            agent_contact=form.agent_contact.data,
            idv_amount=form.idv_amount.data,
            # Owner Details
            owner_name=form.owner_name.data,
            owner_father_name=form.owner_father_name.data,
            owner_address=form.owner_address.data,
            owner_phone=form.owner_phone.data,
            owner_email=form.owner_email.data,
            owner_dob=owner_dob,
            driving_license_number=form.driving_license_number.data,
            dl_expiry_date=dl_expiry_date
        )
        db.session.add(vehicle)
        db.session.commit()
        flash('Vehicle added successfully!', 'success')
        return redirect(url_for('vehi_log.vehi_log_vehicles'))
    return render_template('vehi_log_add_vehicle.html', form=form)

@vehi_log_bp.route('/vehicles/<int:id>')
@login_required
def vehi_log_vehicle_detail(id):
    vehicle = Vehicle.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    expenses = Expense.query.filter_by(vehicle_id=id).order_by(Expense.expense_date.desc()).all()
    total_expenses = sum(expense.amount for expense in expenses)
    return render_template('vehi_log_vehicle_detail.html', vehicle=vehicle, expenses=expenses, total_expenses=total_expenses)

@vehi_log_bp.route('/vehicles/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def vehi_log_edit_vehicle(id):
    vehicle = Vehicle.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = VehicleForm(obj=vehicle)
    
    if request.method == 'GET':
        # Pre-populate form with existing data
        form.purchase_date.data = vehicle.purchase_date.strftime('%d/%m/%Y')
        if vehicle.registration_date:
            form.registration_date.data = vehicle.registration_date.strftime('%d/%m/%Y')
        if vehicle.rc_expiry_date:
            form.rc_expiry_date.data = vehicle.rc_expiry_date.strftime('%d/%m/%Y')
        if vehicle.insurance_start_date:
            form.insurance_start_date.data = vehicle.insurance_start_date.strftime('%d/%m/%Y')
        if vehicle.insurance_expiry_date:
            form.insurance_expiry_date.data = vehicle.insurance_expiry_date.strftime('%d/%m/%Y')
        if vehicle.owner_dob:
            form.owner_dob.data = vehicle.owner_dob.strftime('%d/%m/%Y')
        if vehicle.dl_expiry_date:
            form.dl_expiry_date.data = vehicle.dl_expiry_date.strftime('%d/%m/%Y')
    
    if form.validate_on_submit():
        # Convert string dates to datetime objects
        purchase_date = datetime.strptime(form.purchase_date.data, '%d/%m/%Y').date()
        
        # Handle optional date fields
        registration_date = None
        if form.registration_date.data:
            registration_date = datetime.strptime(form.registration_date.data, '%d/%m/%Y').date()
        
        rc_expiry_date = None
        if form.rc_expiry_date.data:
            rc_expiry_date = datetime.strptime(form.rc_expiry_date.data, '%d/%m/%Y').date()
        
        insurance_start_date = None
        if form.insurance_start_date.data:
            insurance_start_date = datetime.strptime(form.insurance_start_date.data, '%d/%m/%Y').date()
        
        insurance_expiry_date = None
        if form.insurance_expiry_date.data:
            insurance_expiry_date = datetime.strptime(form.insurance_expiry_date.data, '%d/%m/%Y').date()
        
        owner_dob = None
        if form.owner_dob.data:
            owner_dob = datetime.strptime(form.owner_dob.data, '%d/%m/%Y').date()
        
        dl_expiry_date = None
        if form.dl_expiry_date.data:
            dl_expiry_date = datetime.strptime(form.dl_expiry_date.data, '%d/%m/%Y').date()
        
        # Update basic vehicle details
        vehicle.registration_number = form.registration_number.data
        vehicle.make = form.make.data
        vehicle.model = form.model.data
        vehicle.year = form.year.data
        vehicle.vehicle_type = form.vehicle_type.data
        vehicle.fuel_type = form.fuel_type.data
        vehicle.purchase_date = purchase_date
        vehicle.purchase_price = form.purchase_price.data
        
        # Update RC details
        vehicle.engine_number = form.engine_number.data
        vehicle.chassis_number = form.chassis_number.data
        vehicle.registration_date = registration_date
        vehicle.rto_office = form.rto_office.data
        vehicle.rc_expiry_date = rc_expiry_date
        vehicle.seating_capacity = form.seating_capacity.data
        vehicle.unladen_weight = form.unladen_weight.data
        vehicle.gross_vehicle_weight = form.gross_vehicle_weight.data
        
        # Update insurance details
        vehicle.insurance_company = form.insurance_company.data
        vehicle.policy_number = form.policy_number.data
        vehicle.policy_type = form.policy_type.data
        vehicle.insurance_start_date = insurance_start_date
        vehicle.insurance_expiry_date = insurance_expiry_date
        vehicle.premium_amount = form.premium_amount.data
        vehicle.agent_name = form.agent_name.data
        vehicle.agent_contact = form.agent_contact.data
        vehicle.idv_amount = form.idv_amount.data
        
        # Update owner details
        vehicle.owner_name = form.owner_name.data
        vehicle.owner_father_name = form.owner_father_name.data
        vehicle.owner_address = form.owner_address.data
        vehicle.owner_phone = form.owner_phone.data
        vehicle.owner_email = form.owner_email.data
        vehicle.owner_dob = owner_dob
        vehicle.driving_license_number = form.driving_license_number.data
        vehicle.dl_expiry_date = dl_expiry_date
        
        db.session.commit()
        flash('Vehicle updated successfully!', 'success')
        return redirect(url_for('vehi_log.vehi_log_vehicle_detail', id=id))
    
    return render_template('vehi_log_edit_vehicle.html', form=form, vehicle=vehicle)

@vehi_log_bp.route('/vehicles/<int:id>/delete', methods=['POST'])
@login_required
def vehi_log_delete_vehicle(id):
    vehicle = Vehicle.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    # Delete the vehicle (expenses will be deleted automatically due to cascade)
    db.session.delete(vehicle)
    db.session.commit()
    
    flash(f'Vehicle {vehicle.registration_number} deleted successfully!', 'success')
    return redirect(url_for('vehi_log.vehi_log_vehicles'))

@vehi_log_bp.route('/expenses')
@login_required
def vehi_log_expenses():
    expenses = Expense.query.join(Vehicle).filter(Vehicle.user_id == current_user.id).order_by(Expense.expense_date.desc()).all()
    return render_template('vehi_log_expenses.html', expenses=expenses)

@vehi_log_bp.route('/expenses/add', methods=['GET', 'POST'])
@login_required
def vehi_log_add_expense():
    form = ExpenseForm()
    form.vehicle_id.choices = [(v.id, f"{v.registration_number} - {v.make} {v.model}") for v in Vehicle.query.filter_by(user_id=current_user.id).all()]
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

@vehi_log_bp.route('/expenses/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def vehi_log_edit_expense(id):
    expense = Expense.query.join(Vehicle).filter(Expense.id == id, Vehicle.user_id == current_user.id).first_or_404()
    form = ExpenseForm(obj=expense)
    form.vehicle_id.choices = [(v.id, f"{v.registration_number} - {v.make} {v.model}") for v in Vehicle.query.filter_by(user_id=current_user.id).all()]
    form.category_id.choices = [(c.id, c.name) for c in ExpenseCategory.query.all()]
    
    if request.method == 'GET':
        # Pre-populate form with existing data
        form.expense_date.data = expense.expense_date.strftime('%d/%m/%Y')
        form.vehicle_id.data = expense.vehicle_id
        form.category_id.data = expense.category_id
    
    if form.validate_on_submit():
        filename = expense.bill_photo  # Keep existing photo by default
        if form.bill_photo.data:
            filename = save_bill_photo(form.bill_photo.data)
        
        # Convert string date to datetime object
        expense_date = datetime.strptime(form.expense_date.data, '%d/%m/%Y').date()
        
        expense.vehicle_id = form.vehicle_id.data
        expense.category_id = form.category_id.data
        expense.amount = form.amount.data
        expense.description = form.description.data
        expense.expense_date = expense_date
        expense.odometer_reading = form.odometer_reading.data
        expense.vendor_name = form.vendor_name.data
        expense.bill_photo = filename
        
        db.session.commit()
        flash('Expense updated successfully!', 'success')
        return redirect(url_for('vehi_log.vehi_log_expenses'))
    
    return render_template('vehi_log_edit_expense.html', form=form, expense=expense)

@vehi_log_bp.route('/expenses/<int:id>/delete', methods=['POST'])
@login_required
def vehi_log_delete_expense(id):
    expense = Expense.query.join(Vehicle).filter(Expense.id == id, Vehicle.user_id == current_user.id).first_or_404()
    
    # Delete the expense
    db.session.delete(expense)
    db.session.commit()
    
    flash(f'Expense deleted successfully!', 'success')
    return redirect(url_for('vehi_log.vehi_log_expenses'))

@vehi_log_bp.route('/categories')
@login_required
def vehi_log_categories():
    categories = ExpenseCategory.query.all()
    return render_template('vehi_log_categories.html', categories=categories)

@vehi_log_bp.route('/categories/add', methods=['GET', 'POST'])
@login_required
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
@login_required
def vehi_log_info_index():
    return render_template('vehi_log_info/index.html')

@vehi_log_bp.route('/info/maintenance-guide')
@login_required
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