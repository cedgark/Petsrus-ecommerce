from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_qrcode import QRcode

app = Flask(__name__)
QRcode(app)
app.config['SECRET_KEY'] = '76655bf80f7900ae3929c8696951a90c6378b658b9258c2d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c21012668:Belle12345@csmysql.cs.cf.ac.uk:3306/c21012668_cm1102'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

from blog import routes

from flask_admin import Admin
from blog.views import AdminView
from blog.models import User, Post, Comment, Checkout, Product
admin = Admin(app, name='Admin panel', template_mode='bootstrap3')
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Post, db.session))
admin.add_view(AdminView(Comment, db.session))
admin.add_view(AdminView(Product, db.session))
admin.add_view(AdminView(Checkout, db.session))
