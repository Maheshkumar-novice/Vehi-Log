from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, IntegerField, FloatField, SelectField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Regexp, ValidationError
from datetime import date, datetime

def validate_date_format(form, field):
    try:
        datetime.strptime(field.data, '%d/%m/%Y')
    except ValueError:
        raise ValidationError('Invalid date format. Use dd/mm/yyyy')

class VehicleForm(FlaskForm):
    registration_number = StringField('Registration Number', 
                                    validators=[DataRequired(), Length(min=10, max=20),
                                              Regexp(r'^TN\d{2}[A-Z]{2}\d{4}$', 
                                                   message='Format: TN##XX#### (e.g., TN01AA1234)')],
                                    render_kw={"placeholder": "TN01AA1234"})
    make = StringField('Make', validators=[DataRequired(), Length(max=50)],
                      render_kw={"placeholder": "Honda, TVS, Maruti, Hyundai"})
    model = StringField('Model', validators=[DataRequired(), Length(max=50)],
                       render_kw={"placeholder": "Activa, Swift, i20, Splendor"})
    year = IntegerField('Year', validators=[DataRequired(), NumberRange(min=1990, max=date.today().year)],
                       render_kw={"placeholder": "2020"})
    vehicle_type = SelectField('Vehicle Type', 
                              choices=[('MCWG', 'Motorcycle with Gear'),
                                     ('MCWOG', 'Motorcycle without Gear'),
                                     ('LMV', 'Light Motor Vehicle'),
                                     ('HMV', 'Heavy Motor Vehicle')],
                              validators=[DataRequired()])
    fuel_type = SelectField('Fuel Type',
                           choices=[('Petrol', 'Petrol'),
                                  ('Diesel', 'Diesel'),
                                  ('Electric', 'Electric'),
                                  ('CNG', 'CNG')],
                           validators=[DataRequired()])
    purchase_date = StringField('Purchase Date', validators=[DataRequired(), validate_date_format], 
                               render_kw={"placeholder": "dd/mm/yyyy"})
    purchase_price = FloatField('Purchase Price (₹)', validators=[DataRequired(), NumberRange(min=0)],
                               render_kw={"placeholder": "150000"})

class ExpenseForm(FlaskForm):
    vehicle_id = SelectField('Vehicle', coerce=int, validators=[DataRequired()])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    amount = FloatField('Amount (₹)', validators=[DataRequired(), NumberRange(min=0)],
                       render_kw={"placeholder": "1500"})
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=200)],
                               render_kw={"placeholder": "Engine oil change, brake pad replacement, etc."})
    expense_date = StringField('Date', validators=[DataRequired(), validate_date_format],
                              render_kw={"placeholder": "dd/mm/yyyy"})
    odometer_reading = IntegerField('Odometer Reading (km)', validators=[NumberRange(min=0)],
                                   render_kw={"placeholder": "25000"})
    vendor_name = StringField('Vendor/Shop Name', validators=[Length(max=100)],
                             render_kw={"placeholder": "Ramesh Auto Service, City Honda"})
    bill_photo = FileField('Bill Photo', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])

class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(max=50)],
                      render_kw={"placeholder": "Brake Service, Oil Change, Tyre Rotation"})
    description = TextAreaField('Description', validators=[Length(max=200)],
                               render_kw={"placeholder": "Description of this expense category"})