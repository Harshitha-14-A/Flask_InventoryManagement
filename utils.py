from models import ProductMovement, ProductBalance
from database import db
from datetime import datetime


def recalculate_all_balances():
    
    ProductBalance.query.delete()
    
    movements = ProductMovement.query.all()
    
    for movement in movements:
        if movement.from_location:
            ProductBalance.update_balance(
                movement.product_id, 
                movement.from_location, 
                -movement.qty
            )
        
        if movement.to_location:
            ProductBalance.update_balance(
                movement.product_id, 
                movement.to_location, 
                movement.qty
            )
    
    db.session.commit()
    return True


def validate_movement_data(product_id, from_location, to_location, qty):
   
    errors = []
    
    if not from_location and not to_location:
        errors.append("At least one location (From or To) must be specified")
    
    if qty <= 0:
        errors.append("Quantity must be positive")
    
    if from_location:
        current_balance = ProductBalance.get_balance(product_id, from_location)
        if current_balance < qty:
            errors.append(f"Insufficient stock at {from_location}. Available: {current_balance}, Requested: {qty}")
    
    return errors


def get_product_summary(product_id):
    from models import Product
    
    product = Product.query.get(product_id)
    if not product:
        return None
    
    balances = ProductBalance.query.filter_by(product_id=product_id).all()
    
    total_stock = sum(balance.balance for balance in balances)
    locations_with_stock = [
        {
            'location_id': balance.location_id,
            'location_name': balance.location.name,
            'balance': balance.balance,
            'last_updated': balance.last_updated
        }
        for balance in balances if balance.balance > 0
    ]
    
    return {
        'product_id': product_id,
        'product_name': product.name,
        'product_description': product.description,
        'total_stock': total_stock,
        'locations_with_stock': locations_with_stock,
        'total_locations': len(locations_with_stock)
    }


def get_location_summary(location_id):
    from models import Location
    
    location = Location.query.get(location_id)
    if not location:
        return None
    
    balances = ProductBalance.query.filter_by(location_id=location_id).all()
    
    products_in_location = [
        {
            'product_id': balance.product_id,
            'product_name': balance.product.name,
            'balance': balance.balance,
            'last_updated': balance.last_updated
        }
        for balance in balances if balance.balance > 0
    ]
    
    total_items = sum(balance.balance for balance in balances if balance.balance > 0)
    
    return {
        'location_id': location_id,
        'location_name': location.name,
        'location_description': location.description,
        'total_items': total_items,
        'products_in_location': products_in_location,
        'total_product_types': len(products_in_location)
    }


def generate_movement_id():
    import uuid
    return f"MOV-{uuid.uuid4().hex[:8].upper()}"


def generate_product_id():
    import uuid
    return f"PRD-{uuid.uuid4().hex[:8].upper()}"


def generate_location_id():
    import uuid
    return f"LOC-{uuid.uuid4().hex[:8].upper()}"