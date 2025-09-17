from database import db
from datetime import datetime


class Product(db.Model):
    __tablename__ = 'products'
    
    product_id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    movements = db.relationship('ProductMovement', backref='product', lazy=True)
    
    def __repr__(self):
        return f'<Product {self.product_id}: {self.name}>'


class Location(db.Model):
    __tablename__ = 'locations'
    
    location_id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    movements_from = db.relationship('ProductMovement', foreign_keys='ProductMovement.from_location', backref='from_loc', lazy=True)
    movements_to = db.relationship('ProductMovement', foreign_keys='ProductMovement.to_location', backref='to_loc', lazy=True)
    
    def __repr__(self):
        return f'<Location {self.location_id}: {self.name}>'


class ProductMovement(db.Model):
    __tablename__ = 'product_movements'
    
    movement_id = db.Column(db.String(50), primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    from_location = db.Column(db.String(50), db.ForeignKey('locations.location_id'), nullable=True)
    to_location = db.Column(db.String(50), db.ForeignKey('locations.location_id'), nullable=True)
    product_id = db.Column(db.String(50), db.ForeignKey('products.product_id'), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f'<ProductMovement {self.movement_id}: {self.qty} units of {self.product_id}>'
class ProductBalance(db.Model):
    __tablename__ = 'product_balances'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(50), db.ForeignKey('products.product_id'), nullable=False)
    location_id = db.Column(db.String(50), db.ForeignKey('locations.location_id'), nullable=False)
    balance = db.Column(db.Integer, nullable=False, default=0)
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    product = db.relationship('Product', backref='balances')
    location = db.relationship('Location', backref='balances')
    
    __table_args__ = (db.UniqueConstraint('product_id', 'location_id', name='unique_product_location'),)
    
    def __repr__(self):
        return f'<ProductBalance {self.product_id} at {self.location_id}: {self.balance}>'
    
    @staticmethod
    def update_balance(product_id, location_id, quantity_change):
        """Update or create balance for a product at a location"""
        balance = ProductBalance.query.filter_by(
            product_id=product_id, 
            location_id=location_id
        ).first()
        
        if balance:
            balance.balance += quantity_change
            balance.last_updated = datetime.utcnow()
        else:
            balance = ProductBalance(
                product_id=product_id,
                location_id=location_id,
                balance=quantity_change,
                last_updated=datetime.utcnow()
            )
            db.session.add(balance)
        
        return balance
    
    @staticmethod
    def get_balance(product_id, location_id):
        """Get current balance for a product at a location"""
        balance = ProductBalance.query.filter_by(
            product_id=product_id, 
            location_id=location_id
        ).first()
        return balance.balance if balance else 0
    
    @staticmethod
    def get_all_balances():
        """Get all non-zero balances"""
        return ProductBalance.query.filter(ProductBalance.balance != 0).all()
