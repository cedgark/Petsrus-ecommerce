from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_qrcode import QRcode



app = Flask(__name__)


QRcode(app)
app.config['SECRET_KEY'] = '76655bf80f7900ae3929c8696951a90c6378b658b9258c2d'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Lelouch123@localhost:3306/dog'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dog-ecommerce_owner:o5WMmfxgIsP6@ep-muddy-shadow-a5hlx9b7.us-east-2.aws.neon.tech/dog-ecommerce?sslmode=require'
#mysql+pymysql://chiwuikea-o:Lelouch123@localhost:3306/dog
#mysql+pymysql://d21012668:Belle12345@csmysql.cs.cf.ac.uk:3306/c21012668_cm1102
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

# store these flask objects

from store import store

#store_app(app)

store.store_app(app)

store.store_db(db)

store.store_login_manager(login_manager)

#store_app(login_manager)

# from blog import routes
from routes import routes

app.register_blueprint(routes, url_prefix="") # a blueprint of the routes is created

@app.template_filter() ## importing the template filter for currency format
def currencyformat(value):
    value = float(value)
    return "${:,.2f}".format(value)

from flask_admin import Admin
from views import AdminView
from models import User, Post, Comment, Checkout, Product
admin = Admin(app, name='Admin panel', template_mode='bootstrap3')
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Post, db.session))
admin.add_view(AdminView(Comment, db.session))
admin.add_view(AdminView(Product, db.session))
admin.add_view(AdminView(Checkout, db.session))

from waitress import serve
    
if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=8080)
