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


# =============================================================================
# Custom Validation Functions
# =============================================================================

def validate_date_format(form, field):
    """Validate date format for required date fields (dd/mm/yyyy)."""
    if not field.data:
        raise ValidationError('This field is required.')
    try:
        datetime.strptime(field.data, '%d/%m/%Y')
    except (ValueError, TypeError):
        raise ValidationError('Invalid date format. Use dd/mm/yyyy')


def validate_optional_date_format(form, field):
    """Validate date format for optional date fields (dd/mm/yyyy)."""
    if field.data and field.data.strip():
        try:
            datetime.strptime(field.data, '%d/%m/%Y')
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
# Choice Lists
# =============================================================================

VEHICLE_TYPE_CHOICES = [
    ('MCWG', 'Motorcycle with Gear'),
    ('MCWOG', 'Motorcycle without Gear'),
    ('LMV', 'Light Motor Vehicle'),
    ('HMV', 'Heavy Motor Vehicle')
]

FUEL_TYPE_CHOICES = [
    ('Petrol', 'Petrol'),
    ('Diesel', 'Diesel'),
    ('Electric', 'Electric'),
    ('CNG', 'CNG')
]

POLICY_TYPE_CHOICES = [
    ('', 'Select Policy Type'),
    ('Comprehensive', 'Comprehensive'),
    ('Third Party', 'Third Party'),
    ('Standalone OD', 'Standalone Own Damage')
]

TN_RTO_OFFICE_CHOICES = [
    ('', 'Select RTO Office'),
    ('TN01', 'TN01 - Chennai Central'),
    ('TN02', 'TN02 - Chennai North'),
    ('TN03', 'TN03 - Chennai South'),
    ('TN04', 'TN04 - Chennai West'),
    ('TN05', 'TN05 - Maduravoyal'),
    ('TN06', 'TN06 - Ambattur'),
    ('TN07', 'TN07 - Poonamallee'),
    ('TN09', 'TN09 - Coimbatore'),
    ('TN10', 'TN10 - Erode'),
    ('TN11', 'TN11 - Salem'),
    ('TN12', 'TN12 - Vellore'),
    ('TN13', 'TN13 - Krishnagiri'),
    ('TN14', 'TN14 - Dharmapuri'),
    ('TN15', 'TN15 - Madurai'),
    ('TN16', 'TN16 - Dindigul'),
    ('TN17', 'TN17 - Theni'),
    ('TN18', 'TN18 - Sivaganga'),
    ('TN19', 'TN19 - Ramanathapuram'),
    ('TN20', 'TN20 - Virudhunagar'),
    ('TN21', 'TN21 - Tirunelveli'),
    ('TN22', 'TN22 - Tuticorin'),
    ('TN23', 'TN23 - Kanyakumari'),
    ('TN24', 'TN24 - Tiruchirapalli'),
    ('TN25', 'TN25 - Thanjavur'),
    ('TN26', 'TN26 - Pudukkottai'),
    ('TN27', 'TN27 - Karur'),
    ('TN28', 'TN28 - Ariyalur'),
    ('TN29', 'TN29 - Cuddalore'),
    ('TN30', 'TN30 - Villupuram'),
    ('TN31', 'TN31 - Tiruvannamalai'),
    ('TN32', 'TN32 - Kanchipuram'),
    ('TN33', 'TN33 - Tiruvallur'),
    ('TN34', 'TN34 - Nagapattinam'),
    ('TN35', 'TN35 - Tiruvarur'),
    ('TN36', 'TN36 - Nilgiris'),
    ('TN37', 'TN37 - Namakkal'),
    ('TN38', 'TN38 - Perambalur'),
    ('TN39', 'TN39 - Tenkasi')
]


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
        validators=[DataRequired(), NumberRange(min=1990, max=date.today().year)],
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
        choices=TN_RTO_OFFICE_CHOICES
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
        validators=[DataRequired(), Length(min=3, max=80)],
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
        validators=[DataRequired(), Length(min=3, max=80)],
        render_kw={"placeholder": "Choose a username"}
    )
    
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6)],
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