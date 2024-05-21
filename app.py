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

@app.route("/", methods=['GET', 'POST'])
def home():
    return "<p>Hello</p>"
    
if __name__ == "__main__":
    app.run(debug=True)
