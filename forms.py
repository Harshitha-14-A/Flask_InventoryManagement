from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange
from models import Product, Location


class ProductForm(FlaskForm):
    product_id = StringField('Product ID', validators=[DataRequired(), Length(min=1, max=50)])
    name = StringField('Product Name', validators=[DataRequired(), Length(min=1, max=100)])
    description = TextAreaField('Description')


class LocationForm(FlaskForm):
    location_id = StringField('Location ID', validators=[DataRequired(), Length(min=1, max=50)])
    name = StringField('Location Name', validators=[DataRequired(), Length(min=1, max=100)])
    description = TextAreaField('Description')


class ProductMovementForm(FlaskForm):
    movement_id = StringField('Movement ID', validators=[DataRequired(), Length(min=1, max=50)])
    product_id = SelectField('Product', choices=[], validators=[DataRequired()])
    from_location = SelectField('From Location', choices=[], coerce=str)
    to_location = SelectField('To Location', choices=[], coerce=str)
    qty = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    
    def __init__(self, *args, **kwargs):
        super(ProductMovementForm, self).__init__(*args, **kwargs)
        products = Product.query.all()
        self.product_id.choices = [(p.product_id, f"{p.product_id} - {p.name}") for p in products]
        
        locations = Location.query.all()
        location_choices = [('', 'Select Location')] + [(l.location_id, f"{l.location_id} - {l.name}") for l in locations]
        self.from_location.choices = location_choices
        self.to_location.choices = location_choices
