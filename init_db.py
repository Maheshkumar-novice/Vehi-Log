from app import create_app
from models import db, ExpenseCategory

def init_database():
    app = create_app()
    
    with app.app_context():
        db.create_all()
        
        # Add default categories
        default_categories = [
            ('Fuel', 'Petrol, Diesel, CNG refueling'),
            ('Service', 'Regular maintenance and service'),
            ('Repairs', 'Breakdown repairs and fixes'),
            ('Insurance', 'Vehicle insurance premiums'),
            ('Registration', 'RC renewal, license fees'),
            ('Accessories', 'Vehicle accessories and upgrades'),
            ('Toll', 'Highway tolls and parking fees'),
            ('Tyres', 'Tyre replacement and maintenance'),
            ('Parts', 'Spare parts and components'),
            ('Cleaning', 'Car wash and detailing')
        ]
        
        for name, description in default_categories:
            if not ExpenseCategory.query.filter_by(name=name).first():
                category = ExpenseCategory(name=name, description=description)
                db.session.add(category)
        
        db.session.commit()
        print("Database initialized with default categories!")

if __name__ == '__main__':
    init_database()