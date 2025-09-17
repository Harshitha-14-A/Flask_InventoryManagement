import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from database import db

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL") or "mysql+pymysql://root:Root12345%40@localhost/inventory_management"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
db.init_app(app)
csrf = CSRFProtect(app)

with app.app_context():
    import models  
    db.create_all()
    
    from models import ProductBalance, ProductMovement
    if ProductBalance.query.count() == 0 and ProductMovement.query.count() > 0:
        from utils import recalculate_all_balances
        recalculate_all_balances()

from routes import register_routes
register_routes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
