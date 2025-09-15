from flask import render_template, request, redirect, url_for, flash, current_app
from database import db
from models import Product, Location, ProductMovement
from forms import ProductForm, LocationForm, ProductMovementForm
from sqlalchemy import func


def register_routes(app):

    @app.route('/')
    def index():
        return render_template('index.html')

    # Product routes
    @app.route('/products')
    def products():
        products = Product.query.all()
        return render_template('products.html', products=products)

    @app.route('/products/add', methods=['GET', 'POST'])
    def add_product():
        form = ProductForm()
        if form.validate_on_submit():
            # Check if product_id already exists
            existing_product = Product.query.filter_by(product_id=form.product_id.data).first()
            if existing_product:
                flash('Product ID already exists!', 'error')
                return render_template('add_product.html', form=form)
            
            product = Product(
                product_id=form.product_id.data,
                name=form.name.data,
                description=form.description.data
            )
            db.session.add(product)
            db.session.commit()
            flash('Product added successfully!', 'success')
            return redirect(url_for('products'))
        return render_template('add_product.html', form=form)

    @app.route('/products/edit/<product_id>', methods=['GET', 'POST'])
    def edit_product(product_id):
        product = Product.query.get_or_404(product_id)
        form = ProductForm(obj=product)
        
        if form.validate_on_submit():
            product.name = form.name.data
            product.description = form.description.data
            db.session.commit()
            flash('Product updated successfully!', 'success')
            return redirect(url_for('products'))
        
        return render_template('edit_product.html', form=form, product=product)

    @app.route('/products/view/<product_id>')
    def view_product(product_id):
        product = Product.query.get_or_404(product_id)
        movements = ProductMovement.query.filter_by(product_id=product_id).order_by(ProductMovement.timestamp.desc()).all()
        return render_template('view_product.html', product=product, movements=movements)

    # Location routes
    @app.route('/locations')
    def locations():
        locations = Location.query.all()
        return render_template('locations.html', locations=locations)

    @app.route('/locations/add', methods=['GET', 'POST'])
    def add_location():
        form = LocationForm()
        if form.validate_on_submit():
            # Check if location_id already exists
            existing_location = Location.query.filter_by(location_id=form.location_id.data).first()
            if existing_location:
                flash('Location ID already exists!', 'error')
                return render_template('add_location.html', form=form)
            
            location = Location(
                location_id=form.location_id.data,
                name=form.name.data,
                description=form.description.data
            )
            db.session.add(location)
            db.session.commit()
            flash('Location added successfully!', 'success')
            return redirect(url_for('locations'))
        return render_template('add_location.html', form=form)

    @app.route('/locations/edit/<location_id>', methods=['GET', 'POST'])
    def edit_location(location_id):
        location = Location.query.get_or_404(location_id)
        form = LocationForm(obj=location)
        
        if form.validate_on_submit():
            location.name = form.name.data
            location.description = form.description.data
            db.session.commit()
            flash('Location updated successfully!', 'success')
            return redirect(url_for('locations'))
        
        return render_template('edit_location.html', form=form, location=location)

    @app.route('/locations/view/<location_id>')
    def view_location(location_id):
        location = Location.query.get_or_404(location_id)
        movements_from = ProductMovement.query.filter_by(from_location=location_id).order_by(ProductMovement.timestamp.desc()).all()
        movements_to = ProductMovement.query.filter_by(to_location=location_id).order_by(ProductMovement.timestamp.desc()).all()
        return render_template('view_location.html', location=location, movements_from=movements_from, movements_to=movements_to)

    # Movement routes
    @app.route('/movements')
    def movements():
        movements = ProductMovement.query.order_by(ProductMovement.timestamp.desc()).all()
        return render_template('movements.html', movements=movements)

    @app.route('/movements/add', methods=['GET', 'POST'])
    def add_movement():
        form = ProductMovementForm()
        if form.validate_on_submit():
            # Validate that at least one location is specified
            if not form.from_location.data and not form.to_location.data:
                flash('At least one location (From or To) must be specified!', 'error')
                return render_template('add_movement.html', form=form)
            
            # Check if movement_id already exists
            existing_movement = ProductMovement.query.filter_by(movement_id=form.movement_id.data).first()
            if existing_movement:
                flash('Movement ID already exists!', 'error')
                return render_template('add_movement.html', form=form)
            
            movement = ProductMovement(
                movement_id=form.movement_id.data,
                product_id=form.product_id.data,
                from_location=form.from_location.data if form.from_location.data else None,
                to_location=form.to_location.data if form.to_location.data else None,
                qty=form.qty.data
            )
            db.session.add(movement)
            db.session.commit()
            flash('Movement added successfully!', 'success')
            return redirect(url_for('movements'))
        return render_template('add_movement.html', form=form)

    @app.route('/movements/edit/<movement_id>', methods=['GET', 'POST'])
    def edit_movement(movement_id):
        movement = ProductMovement.query.get_or_404(movement_id)
        form = ProductMovementForm(obj=movement)
        
        if form.validate_on_submit():
            # Validate that at least one location is specified
            if not form.from_location.data and not form.to_location.data:
                flash('At least one location (From or To) must be specified!', 'error')
                return render_template('edit_movement.html', form=form, movement=movement)
            
            movement.product_id = form.product_id.data
            movement.from_location = form.from_location.data if form.from_location.data else None
            movement.to_location = form.to_location.data if form.to_location.data else None
            movement.qty = form.qty.data
            db.session.commit()
            flash('Movement updated successfully!', 'success')
            return redirect(url_for('movements'))
        
        return render_template('edit_movement.html', form=form, movement=movement)

    @app.route('/movements/view/<movement_id>')
    def view_movement(movement_id):
        movement = ProductMovement.query.get_or_404(movement_id)
        return render_template('view_movement.html', movement=movement)

    # Balance Report route
    @app.route('/balance_report')
    def balance_report():
        # Calculate balance for each product in each location
        # This is a complex query that calculates net balance per product per location
        
        # Get all movements that bring items INTO locations (to_location is not null)
        incoming = db.session.query(
            ProductMovement.product_id,
            ProductMovement.to_location.label('location_id'),
            func.sum(ProductMovement.qty).label('incoming_qty')
        ).filter(
            ProductMovement.to_location.isnot(None)
        ).group_by(
            ProductMovement.product_id,
            ProductMovement.to_location
        ).subquery()
        
        # Get all movements that take items OUT of locations (from_location is not null)
        outgoing = db.session.query(
            ProductMovement.product_id,
            ProductMovement.from_location.label('location_id'),
            func.sum(ProductMovement.qty).label('outgoing_qty')
        ).filter(
            ProductMovement.from_location.isnot(None)
        ).group_by(
            ProductMovement.product_id,
            ProductMovement.from_location
        ).subquery()
        
        # Calculate net balance by combining incoming and outgoing
        balance_query = db.session.query(
            Product.product_id,
            Product.name.label('product_name'),
            Location.location_id,
            Location.name.label('location_name'),
            (func.coalesce(incoming.c.incoming_qty, 0) - func.coalesce(outgoing.c.outgoing_qty, 0)).label('balance')
        ).select_from(Product).join(
            Location, True  # Cross join to get all product-location combinations
        ).outerjoin(
            incoming, (incoming.c.product_id == Product.product_id) & (incoming.c.location_id == Location.location_id)
        ).outerjoin(
            outgoing, (outgoing.c.product_id == Product.product_id) & (outgoing.c.location_id == Location.location_id)
        ).filter(
            func.coalesce(incoming.c.incoming_qty, 0) - func.coalesce(outgoing.c.outgoing_qty, 0) != 0
        ).order_by(
            Product.product_id, Location.location_id
        ).all()
        
        return render_template('balance_report.html', balance_data=balance_query)