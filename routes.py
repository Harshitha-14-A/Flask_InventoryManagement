from flask import render_template, request, redirect, url_for, flash, current_app
from database import db
from models import Product, Location, ProductMovement, ProductBalance
from forms import ProductForm, LocationForm, ProductMovementForm
from sqlalchemy import func


def register_routes(app):

    @app.route('/')
    def index():
        product_count = Product.query.count()
        location_count = Location.query.count()
        movement_count = ProductMovement.query.count()

        balance_count = ProductBalance.query.filter(ProductBalance.balance != 0).count()

        return render_template('index.html',
                             product_count=product_count,
                             location_count=location_count,
                             movement_count=movement_count,
                             balance_count=balance_count)

    @app.route('/products')
    def products():
        products = Product.query.all()
        return render_template('products.html', products=products)

    @app.route('/products/add', methods=['GET', 'POST'])
    def add_product():
        form = ProductForm()
        if form.validate_on_submit():
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

    @app.route('/products/delete/<product_id>', methods=['POST'])
    def delete_product(product_id):
        product = Product.query.get_or_404(product_id)
        
        movement_count = ProductMovement.query.filter_by(product_id=product_id).count()
        if movement_count > 0:
            flash(f'Cannot delete product "{product.name}" because it has {movement_count} movement(s) associated with it.', 'error')
            return redirect(url_for('view_product', product_id=product_id))
        
        db.session.delete(product)
        db.session.commit()
        flash(f'Product "{product.name}" has been deleted successfully!', 'success')
        return redirect(url_for('products'))

    @app.route('/locations')
    def locations():
        locations = Location.query.all()
        return render_template('locations.html', locations=locations)

    @app.route('/locations/add', methods=['GET', 'POST'])
    def add_location():
        form = LocationForm()
        if form.validate_on_submit():
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

    @app.route('/locations/delete/<location_id>', methods=['POST'])
    def delete_location(location_id):
        location = Location.query.get_or_404(location_id)
        
        movement_count_from = ProductMovement.query.filter_by(from_location=location_id).count()
        movement_count_to = ProductMovement.query.filter_by(to_location=location_id).count()
        total_movements = movement_count_from + movement_count_to
        
        if total_movements > 0:
            flash(f'Cannot delete location "{location.name}" because it has {total_movements} movement(s) associated with it.', 'error')
            return redirect(url_for('view_location', location_id=location_id))
        
        db.session.delete(location)
        db.session.commit()
        flash(f'Location "{location.name}" has been deleted successfully!', 'success')
        return redirect(url_for('locations'))

    @app.route('/movements')
    def movements():
        movements = ProductMovement.query.order_by(ProductMovement.timestamp.desc()).all()
        return render_template('movements.html', movements=movements)

    @app.route('/movements/add', methods=['GET', 'POST'])
    def add_movement():
        form = ProductMovementForm()
        if form.validate_on_submit():
            if not form.from_location.data and not form.to_location.data:
                flash('At least one location (From or To) must be specified!', 'error')
                return render_template('add_movement.html', form=form)
            
            existing_movement = ProductMovement.query.filter_by(movement_id=form.movement_id.data).first()
            if existing_movement:
                flash('Movement ID already exists!', 'error')
                return render_template('add_movement.html', form=form)
            
            if form.from_location.data:
                current_balance = ProductBalance.get_balance(form.product_id.data, form.from_location.data)
                if current_balance < form.qty.data:
                    flash(f'Insufficient stock! Current balance: {current_balance}, Requested: {form.qty.data}', 'error')
                    return render_template('add_movement.html', form=form)
            
            movement = ProductMovement(
                movement_id=form.movement_id.data,
                product_id=form.product_id.data,
                from_location=form.from_location.data if form.from_location.data else None,
                to_location=form.to_location.data if form.to_location.data else None,
                qty=form.qty.data
            )
            db.session.add(movement)
            
            if form.from_location.data:
                ProductBalance.update_balance(form.product_id.data, form.from_location.data, -form.qty.data)
            if form.to_location.data:
                ProductBalance.update_balance(form.product_id.data, form.to_location.data, form.qty.data)
            
            db.session.commit()
            flash('Movement added successfully!', 'success')
            return redirect(url_for('movements'))
        return render_template('add_movement.html', form=form)

    @app.route('/movements/edit/<movement_id>', methods=['GET', 'POST'])
    def edit_movement(movement_id):
        movement = ProductMovement.query.get_or_404(movement_id)
        form = ProductMovementForm(obj=movement)
        
        if form.validate_on_submit():
            if not form.from_location.data and not form.to_location.data:
                flash('At least one location (From or To) must be specified!', 'error')
                return render_template('edit_movement.html', form=form, movement=movement)
            
            if movement.from_location:
                ProductBalance.update_balance(movement.product_id, movement.from_location, movement.qty)
            if movement.to_location:
                ProductBalance.update_balance(movement.product_id, movement.to_location, -movement.qty)
            
            if form.from_location.data:
                current_balance = ProductBalance.get_balance(form.product_id.data, form.from_location.data)
                if current_balance < form.qty.data:
                    if movement.from_location:
                        ProductBalance.update_balance(movement.product_id, movement.from_location, -movement.qty)
                    if movement.to_location:
                        ProductBalance.update_balance(movement.product_id, movement.to_location, movement.qty)
                    flash(f'Insufficient stock! Current balance: {current_balance}, Requested: {form.qty.data}', 'error')
                    return render_template('edit_movement.html', form=form, movement=movement)
            
            movement.product_id = form.product_id.data
            movement.from_location = form.from_location.data if form.from_location.data else None
            movement.to_location = form.to_location.data if form.to_location.data else None
            movement.qty = form.qty.data
            
            if form.from_location.data:
                ProductBalance.update_balance(form.product_id.data, form.from_location.data, -form.qty.data)
            if form.to_location.data:
                ProductBalance.update_balance(form.product_id.data, form.to_location.data, form.qty.data)
            
            db.session.commit()
            flash('Movement updated successfully!', 'success')
            return redirect(url_for('movements'))
        
        return render_template('edit_movement.html', form=form, movement=movement)

    @app.route('/movements/view/<movement_id>')
    def view_movement(movement_id):
        movement = ProductMovement.query.get_or_404(movement_id)
        return render_template('view_movement.html', movement=movement)

    @app.route('/movements/delete/<movement_id>', methods=['POST'])
    def delete_movement(movement_id):
        movement = ProductMovement.query.get_or_404(movement_id)
        
        if movement.from_location:
            ProductBalance.update_balance(movement.product_id, movement.from_location, movement.qty)
        if movement.to_location:
            ProductBalance.update_balance(movement.product_id, movement.to_location, -movement.qty)
        
        db.session.delete(movement)
        db.session.commit()
        flash(f'Movement "{movement.movement_id}" has been deleted successfully!', 'success')
        return redirect(url_for('movements'))

    @app.route('/balance_report')
    def balance_report():
        balances = ProductBalance.get_all_balances()

        positive_balances = ProductBalance.query.filter(ProductBalance.balance > 0).count()
        negative_balances = ProductBalance.query.filter(ProductBalance.balance < 0).count()
        total_units = db.session.query(func.sum(ProductBalance.balance)).scalar() or 0
        
        balance_data = []
        for balance in balances:
            balance_data.append({
                'product_id': balance.product_id,
                'product_name': balance.product.name,
                'location_id': balance.location_id,
                'location_name': balance.location.name,
                'balance': balance.balance,
                'last_updated': balance.last_updated
            })
        
        balance_data.sort(key=lambda x: (x['product_id'], x['location_id']))
        
        return render_template('balance_report.html', balance_data=balance_data,
                               positive_balances=positive_balances,
                               negative_balances=negative_balances,
                               total_units=total_units)
    
    @app.route('/api/products', methods=['GET'])
    def api_products():
        """API endpoint to get all products"""
        products = Product.query.all()
        return {
            'products': [
                {
                    'product_id': p.product_id,
                    'name': p.name,
                    'description': p.description
                } for p in products
            ]
        }
    
    @app.route('/api/locations', methods=['GET'])
    def api_locations():
        """API endpoint to get all locations"""
        locations = Location.query.all()
        return {
            'locations': [
                {
                    'location_id': l.location_id,
                    'name': l.name,
                    'description': l.description
                } for l in locations
            ]
        }
    
    @app.route('/api/movements', methods=['GET'])
    def api_movements():
        """API endpoint to get all movements"""
        movements = ProductMovement.query.order_by(ProductMovement.timestamp.desc()).all()
        return {
            'movements': [
                {
                    'movement_id': m.movement_id,
                    'product_id': m.product_id,
                    'product_name': m.product.name,
                    'from_location': m.from_location,
                    'from_location_name': m.from_loc.name if m.from_loc else None,
                    'to_location': m.to_location,
                    'to_location_name': m.to_loc.name if m.to_loc else None,
                    'qty': m.qty,
                    'timestamp': m.timestamp.isoformat()
                } for m in movements
            ]
        }
    
    @app.route('/api/balance', methods=['GET'])
    def api_balance():
        """API endpoint to get current balance report"""
        balances = ProductBalance.get_all_balances()
        return {
            'balances': [
                {
                    'product_id': b.product_id,
                    'product_name': b.product.name,
                    'location_id': b.location_id,
                    'location_name': b.location.name,
                    'balance': b.balance,
                    'last_updated': b.last_updated.isoformat()
                } for b in balances
            ]
        }
    
    @app.route('/api/balance/<product_id>/<location_id>', methods=['GET'])
    def api_product_balance(product_id, location_id):
        """API endpoint to get balance for a specific product at a location"""
        balance = ProductBalance.get_balance(product_id, location_id)
        product = Product.query.get_or_404(product_id)
        location = Location.query.get_or_404(location_id)
        
        return {
            'product_id': product_id,
            'product_name': product.name,
            'location_id': location_id,
            'location_name': location.name,
            'balance': balance
        }

   
