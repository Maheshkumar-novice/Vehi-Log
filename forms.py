"""
Forms for VehiLog application.

This module contains all form classes and validation functions for the vehicle
expense tracking application.
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, IntegerField, FloatField, SelectField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length, NumberRange, Regexp, ValidationError, EqualTo
from datetime import date, datetime
from constants import (
    VEHICLE_TYPE_CHOICES, FUEL_TYPE_CHOICES, POLICY_TYPE_CHOICES, 
    RTO_OFFICE_CHOICES, DATE_FORMAT, MIN_YEAR, MIN_USERNAME_LENGTH, 
    MAX_USERNAME_LENGTH, MIN_PASSWORD_LENGTH
)


# =============================================================================
# Custom Validation Functions
# =============================================================================

def validate_date_format(form, field):
    """Validate date format for required date fields (dd/mm/yyyy)."""
    if not field.data:
        raise ValidationError('This field is required.')
    try:
        datetime.strptime(field.data, DATE_FORMAT)
    except (ValueError, TypeError):
        raise ValidationError('Invalid date format. Use dd/mm/yyyy')


def validate_optional_date_format(form, field):
    """Validate date format for optional date fields (dd/mm/yyyy)."""
    if field.data and field.data.strip():
        try:
            datetime.strptime(field.data, DATE_FORMAT)
        except (ValueError, TypeError):
            raise ValidationError('Invalid date format. Use dd/mm/yyyy')


def validate_optional_integer(form, field):
    """Validate integer for optional integer fields."""
    if field.data and str(field.data).strip():
        try:
            int(field.data)
        except (ValueError, TypeError):
            raise ValidationError('Please enter a valid number')


def validate_optional_float(form, field):
    """Validate float for optional float fields."""
    if field.data and str(field.data).strip():
        try:
            float(field.data)
        except (ValueError, TypeError):
            raise ValidationError('Please enter a valid number')




# =============================================================================
# Form Classes
# =============================================================================

class VehicleForm(FlaskForm):
    """Form for adding/editing vehicle information."""
    
    # -------------------------------------------------------------------------
    # Basic Vehicle Details (Required)
    # -------------------------------------------------------------------------
    
    registration_number = StringField(
        'Registration Number',
        validators=[
            DataRequired(),
            Length(min=10, max=20),
            Regexp(r'^TN\d{2}[A-Z]{2}\d{4}$', 
                   message='Format: TN##XX#### (e.g., TN01AA1234)')
        ],
        render_kw={"placeholder": "TN01AA1234"}
    )
    
    make = StringField(
        'Make',
        validators=[DataRequired(), Length(max=50)],
        render_kw={"placeholder": "Honda, TVS, Maruti, Hyundai"}
    )
    
    model = StringField(
        'Model',
        validators=[DataRequired(), Length(max=50)],
        render_kw={"placeholder": "Activa, Swift, i20, Splendor"}
    )
    
    year = IntegerField(
        'Year',
        validators=[DataRequired(), NumberRange(min=MIN_YEAR, max=date.today().year)],
        render_kw={"placeholder": "2020"}
    )
    
    vehicle_type = SelectField(
        'Vehicle Type',
        choices=VEHICLE_TYPE_CHOICES,
        validators=[DataRequired()]
    )
    
    fuel_type = SelectField(
        'Fuel Type',
        choices=FUEL_TYPE_CHOICES,
        validators=[DataRequired()]
    )
    
    purchase_date = StringField(
        'Purchase Date',
        validators=[DataRequired(), validate_date_format],
        render_kw={"placeholder": "dd/mm/yyyy"}
    )
    
    purchase_price = FloatField(
        'Purchase Price (₹)',
        validators=[DataRequired(), NumberRange(min=0)],
        render_kw={"placeholder": "150000"}
    )
    
    # -------------------------------------------------------------------------
    # RC Details (Optional)
    # -------------------------------------------------------------------------
    
    engine_number = StringField(
        'Engine Number',
        validators=[Length(max=50)],
        render_kw={"placeholder": "AB12CD3456789"}
    )
    
    chassis_number = StringField(
        'Chassis Number',
        validators=[Length(max=50)],
        render_kw={"placeholder": "MA1234567890123456"}
    )
    
    registration_date = StringField(
        'Registration Date',
        validators=[validate_optional_date_format],
        render_kw={"placeholder": "dd/mm/yyyy"}
    )
    
    rto_office = SelectField(
        'RTO Office',
        choices=RTO_OFFICE_CHOICES
    )
    
    rc_expiry_date = StringField(
        'RC Expiry Date',
        validators=[validate_optional_date_format],
        render_kw={"placeholder": "dd/mm/yyyy"}
    )
    
    seating_capacity = StringField(
        'Seating Capacity',
        validators=[validate_optional_integer],
        render_kw={"placeholder": "5"}
    )
    
    unladen_weight = StringField(
        'Unladen Weight (kg)',
        validators=[validate_optional_integer],
        render_kw={"placeholder": "1200"}
    )
    
    gross_vehicle_weight = StringField(
        'Gross Vehicle Weight (kg)',
        validators=[validate_optional_integer],
        render_kw={"placeholder": "1800"}
    )
    
    # -------------------------------------------------------------------------
    # Insurance Details (Optional)
    # -------------------------------------------------------------------------
    
    insurance_company = StringField(
        'Insurance Company',
        validators=[Length(max=100)],
        render_kw={"placeholder": "New India Assurance, ICICI Lombard, Bajaj Allianz"}
    )
    
    policy_number = StringField(
        'Policy Number',
        validators=[Length(max=50)],
        render_kw={"placeholder": "1234567890"}
    )
    
    policy_type = SelectField(
        'Policy Type',
        choices=POLICY_TYPE_CHOICES
    )
    
    insurance_start_date = StringField(
        'Insurance Start Date',
        validators=[validate_optional_date_format],
        render_kw={"placeholder": "dd/mm/yyyy"}
    )
    
    insurance_expiry_date = StringField(
        'Insurance Expiry Date',
        validators=[validate_optional_date_format],
        render_kw={"placeholder": "dd/mm/yyyy"}
    )
    
    premium_amount = StringField(
        'Premium Amount (₹)',
        validators=[validate_optional_float],
        render_kw={"placeholder": "15000"}
    )
    
    agent_name = StringField(
        'Agent Name',
        validators=[Length(max=100)],
        render_kw={"placeholder": "Agent Name"}
    )
    
    agent_contact = StringField(
        'Agent Contact',
        validators=[Length(max=20)],
        render_kw={"placeholder": "9876543210"}
    )
    
    idv_amount = StringField(
        'IDV Amount (₹)',
        validators=[validate_optional_float],
        render_kw={"placeholder": "500000"}
    )
    
    # -------------------------------------------------------------------------
    # Owner Details (Optional)
    # -------------------------------------------------------------------------
    
    owner_name = StringField(
        'Owner Name',
        validators=[Length(max=100)],
        render_kw={"placeholder": "Full Name as per RC"}
    )
    
    owner_father_name = StringField(
        'Father/Husband Name',
        validators=[Length(max=100)],
        render_kw={"placeholder": "Father's/Husband's Name"}
    )
    
    owner_address = TextAreaField(
        'Address',
        validators=[Length(max=500)],
        render_kw={"placeholder": "Address as per RC", "rows": "3"}
    )
    
    owner_phone = StringField(
        'Phone Number',
        validators=[Length(max=20)],
        render_kw={"placeholder": "9876543210"}
    )
    
    owner_email = StringField(
        'Email',
        validators=[Length(max=100)],
        render_kw={"placeholder": "owner@email.com"}
    )
    
    owner_dob = StringField(
        'Date of Birth',
        validators=[validate_optional_date_format],
        render_kw={"placeholder": "dd/mm/yyyy"}
    )
    
    driving_license_number = StringField(
        'Driving License Number',
        validators=[Length(max=50)],
        render_kw={"placeholder": "TN1234567890"}
    )
    
    dl_expiry_date = StringField(
        'DL Expiry Date',
        validators=[validate_optional_date_format],
        render_kw={"placeholder": "dd/mm/yyyy"}
    )


class ExpenseForm(FlaskForm):
    """Form for adding/editing expense information."""
    
    vehicle_id = SelectField(
        'Vehicle',
        coerce=int,
        validators=[DataRequired()]
    )
    
    category_id = SelectField(
        'Category',
        coerce=int,
        validators=[DataRequired()]
    )
    
    amount = FloatField(
        'Amount (₹)',
        validators=[DataRequired(), NumberRange(min=0)],
        render_kw={"placeholder": "1500"}
    )
    
    description = TextAreaField(
        'Description',
        validators=[DataRequired(), Length(max=200)],
        render_kw={"placeholder": "Engine oil change, brake pad replacement, etc."}
    )
    
    expense_date = StringField(
        'Date',
        validators=[DataRequired(), validate_date_format],
        render_kw={"placeholder": "dd/mm/yyyy"}
    )
    
    odometer_reading = IntegerField(
        'Odometer Reading (km)',
        validators=[NumberRange(min=0)],
        render_kw={"placeholder": "25000"}
    )
    
    vendor_name = StringField(
        'Vendor/Shop Name',
        validators=[Length(max=100)],
        render_kw={"placeholder": "Ramesh Auto Service, City Honda"}
    )
    
    bill_photo = FileField(
        'Bill Photo',
        validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')]
    )


class CategoryForm(FlaskForm):
    """Form for adding/editing expense categories."""
    
    name = StringField(
        'Category Name',
        validators=[DataRequired(), Length(max=50)],
        render_kw={"placeholder": "Brake Service, Oil Change, Tyre Rotation"}
    )
    
    description = TextAreaField(
        'Description',
        validators=[Length(max=200)],
        render_kw={"placeholder": "Description of this expense category"}
    )


class LoginForm(FlaskForm):
    """Form for user login."""
    
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=MIN_USERNAME_LENGTH, max=MAX_USERNAME_LENGTH)],
        render_kw={"placeholder": "Enter your username"}
    )
    
    password = PasswordField(
        'Password',
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your password"}
    )


class RegistrationForm(FlaskForm):
    """Form for user registration."""
    
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=MIN_USERNAME_LENGTH, max=MAX_USERNAME_LENGTH)],
        render_kw={"placeholder": "Choose a username"}
    )
    
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=MIN_PASSWORD_LENGTH)],
        render_kw={"placeholder": "Choose a strong password"}
    )
    
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match')
        ],
        render_kw={"placeholder": "Confirm your password"}
    )