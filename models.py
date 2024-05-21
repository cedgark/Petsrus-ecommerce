from datetime import datetime
from flask import current_app as app
# from app import app
#from app import db
# from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
# from app import login_manager
from store import store
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# db.metadata.clear()
app = store.app
db = store.db
login_manager = store.login_manager

class Post(db.Model):
  __table_args__ = {'keep_existing': True}
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  title = db.Column(db.Text, nullable=False)
  content = db.Column(db.Text, nullable=False)
  image_file = db.Column(db.String(40), nullable=False, default='default.jpg')
  author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

  def __repr__(self):
    return f"Post('{self.date}', '{self.title}', '{self.content}')"

###
class Product(db.Model):
  __table_args__ = {'keep_existing': True}
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(64))
  scontent = db.Column(db.Text,nullable=True) #short and long descriptions
  lcontent = db.Column(db.Text,nullable=True)
  price = db.Column(db.Float,nullable=False)
  image_file = db.Column(db.String(64),unique=True)


class User(UserMixin, db.Model):
    __table_args__ = {'keep_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    first_name = db.Column(db.String(15), unique=True, nullable=False, default='Joe')
    last_name = db.Column(db.String(15), unique=True, nullable=False, default='Blow') #Continue adding first and last name
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    password_hash = db.Column(db.String(128))
    password = db.Column(db.String(60), nullable=False)
    comment=db.relationship('Comment',backref='user',lazy=True)
    post = db.relationship('Post', backref='user', lazy=True)
    #checkout = db.relationship('Checkout', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Comment(db.Model):
  __table_args__ = {'keep_existing': True}
  id = db.Column(db.Integer,primary_key=True)
  date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
  content = db.Column(db.Text,nullable=False)
  parent_id = db.Column(db.Integer,db.ForeignKey('comment.id'),nullable=True)
  product_id = db.Column(db.Integer,db.ForeignKey('product.id'),nullable=False)
  author_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
  parent = db.relationship('Comment',backref='comment_parent',remote_side=id,lazy=True)

  def __repr__(self):
    return f"Post('{self.date}','{self.content}')"


class Checkout(db.Model):
  __table_args__ = {'keep_existing': True}
  id = db.Column(db.Integer, primary_key=True)
  full_name = db.Column(db.Text)
  email = db.Column(db.String(120)) #email = db.Column(db.String(120),db.ForeignKey('user.id'))
  address = db.Column(db.Text) #checkout.cvv checkout.expiry_month checkout.expiry_year
  city =  db.Column(db.Text)
  card_number = db.Column(db.Text)
  cvv = db.Column(db.Text)
  expiry_month = db.Column(db.Integer)
  expiry_year = db.Column(db.Text)
