from flask import render_template, url_for, flash,session
from blog import app
from blog.models import User, Post, Product, Checkout
from blog import db
from flask import request, redirect
from blog.forms import RegistrationForm
from blog.forms import LoginForm
from flask_login import login_user
from flask_login import logout_user
from blog.models import Comment
from blog.forms import CommentForm
from blog.forms import CheckoutForm, SearchForm
from flask_login import login_required, current_user
from sqlalchemy import desc
from datetime import datetime


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
@app.route("/home/<string:sort_by>", methods=['GET', 'POST'])
def home(sort_by=None):
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1  # reading and updating session data
    else:
        session['visits'] = 1 # setting session data
        cart_item = {'Labrador Retriever': 0, 'German Shepherd': 0, 'Golden Retriever': 0,'Beagle': 0,'Poodle': 0, 'Pug': 0}
        session['cart_item'] = cart_item
    form = SearchForm()
    if form.validate_on_submit():
        search = form.search.data
        if Product.query.filter_by(title=search).all():
            flash(f'{search} Found')
            products =  Product.query.filter_by(title=search.lower()).all()
            return render_template('home.html',products=products,sort_by=sort_by,form=form)
        else:
            flash(f'Dog Name: {search} Not Found')
            redirect(url_for('home'))


    products=Product.query.order_by('title').all()
    if not(sort_by == None):
        if sort_by[0] == 'n':
            if sort_by[2] == 'd':
                products=Product.query.order_by(desc('title')).all()
        else:
            if sort_by[2] == 'd':
                products=Product.query.order_by(desc('price'))
            else:
                products=Product.query.order_by('price')
    return render_template('home.html',products=products,sort_by=sort_by,form=form)




@app.route("/cart")
def cart():
    if not(current_user.is_authenticated):
        flash('You must login to do this.')
        return redirect(url_for('login'))
    products=Product.query.all()
    return render_template('cart.html',products=products)


@app.route("/wishlist")
def wishlist():
    if not(current_user.is_authenticated):
        flash('You must login to do this.')
        return redirect(url_for('login'))
    if not('wishlist' in session):
        session['wishlist'] = {'Labrador Retriever': 0, 'German Shepherd': 0, 'Golden Retriever': 0,'Beagle': 0,'Poodle': 0, 'Pug': 0}  #BASKET😎

    products=Product.query.all()
    return render_template('wishlist.html',products=products)


@app.route('/add/<string:loc>/<string:item_name>/<product_id>/<skey>')
def add(loc,item_name,product_id=None,skey=None):
    if not(current_user.is_authenticated):
        flash('You must login to do this.')
        return redirect(url_for('login'))
    if skey in session:
        session[skey][item_name] = int(session[skey][item_name]) + 1
        session.modified = True

        if skey == 'wishlist':
            flash(f'Item Added! You added {item_name} to your {skey}!')
        else:
            flash(f'Item Added! You added {item_name} to your cart!')
    else:
        cart_item = {'Labrador Retriever': 0, 'German Shepherd': 0, 'Golden Retriever': 0,'Beagle': 0,'Poodle': 0, 'Pug': 0}   #BASKET😎
        session[skey] = cart_item
    return redirect(url_for(loc,product_id=product_id))

@app.route('/subtract/<string:loc>/<string:item_name>/<product_id>/<skey>')
def subtract(loc,item_name,product_id=None,skey=None):
    if not(current_user.is_authenticated):
        flash('You must login to do this.')
        return redirect(url_for('login'))
    if not(session[skey][item_name] == 0):
        if skey in session:
            session[skey][item_name] = int(session[skey][item_name]) - 1
            session.modified = True
        else:
            cart_item = {'Labrador Retriever': 0, 'German Shepherd': 0, 'Golden Retriever': 0,'Beagle': 0,'Poodle': 0, 'Pug': 0}    #BASKET😎
            session[skey] = cart_item

    return redirect(url_for(loc,product_id=product_id))

@app.route('/clear/<string:loc>/<string:item_name>/<product_id>/<skey>')
def clear(loc,item_name,product_id=None,skey=None):
    if not(current_user.is_authenticated):
        flash('You must login to do this.')
        return redirect(url_for('login'))
    if not(session[skey][item_name] == 0):
        if skey in session:
            session[skey][item_name] = 0
            session.modified = True
        else:
            cart_item = {'Labrador Retriever': 0, 'German Shepherd': 0, 'Golden Retriever': 0,'Beagle': 0,'Poodle': 0, 'Pug': 0}
            session[skey] = cart_item

    return redirect(url_for(loc,product_id=product_id))

@app.route("/about")
def about():
  return render_template('about.html', title='About')


@app.route("/product/<int:product_id>")
def product(product_id):
    product = Product.query.get_or_404(product_id)
    comments = Comment.query.filter(Comment.product_id == product.id)
    form = CommentForm()
    return render_template('product.html', product=product, comments=comments, form=form)

@app.route('/product/<int:product_id>/comment', methods=['GET', 'POST'])
@login_required
def product_comment(product_id):
    if not(current_user.is_authenticated):
        flash('You must login to do this.')
        return redirect(url_for('login'))
    product = Product.query.get_or_404(product_id)
    form = CommentForm()
    if form.validate_on_submit():
        db.session.add(Comment(content=form.comment.data, product_id=product.id, author_id=current_user.id))
        db.session.commit()
        flash("Your comment has been added to the product page", "success")
        return redirect(f'/product/{product.id}')
    comments = Comment.query.filter(Comment.product_id == product.id)
    return render_template('product.html', product=product, comments=comments, form=form)

@app.template_filter()
def currencyformat(value):
    value = float(value)
    return "${:,.2f}".format(value)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,first_name=form.first_name.data,last_name=form.last_name.data,email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!')
        login_user(user)
        return redirect(url_for('home')) #Redirects to thank you for registering page

    return render_template('register.html', title='Register',form=form)

@app.route("/login/<int:flag_comment>", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login(flag_comment=None):
    if flag_comment == 1:
        flash('You must login to comment.')
        flag_comment=0

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash('Login successful!')
            return redirect(url_for('home'))
        else:
            flash('That account does not exist!')





    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash('Logout successful!')
    return redirect(url_for('home'))




@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
    if not(current_user.is_authenticated):
        flash('You must login to do this.')
        return redirect(url_for('login'))
    counter = 0
    products = products=Product.query.all()
    for product in products:
        if session['cart_item'][product.title] > 0:
            counter = counter + 1
    if counter == 0:
        flash('Cart is empty! Add items to check out.')
        return redirect(url_for('invoice'))

    form = CheckoutForm()
    if form.validate_on_submit():
        checkout = Checkout(full_name=form.full_name.data,email=form.email.data,address=form.address.data,city=form.city.data, card_number=form.card_number.data, cvv=form.cvv.data, expiry_month=form.expiry_month.data,expiry_year=form.expiry_year.data)
        db.session.add(checkout)
        db.session.commit()
        flash('Payment Successful!')
        return redirect(url_for('invoice')) #Redirects to home

    return render_template('checkout.html',form=form)

@app.route("/invoice")
def invoice():
    if not(current_user.is_authenticated):
        flash('You must login to do this.')
        return redirect(url_for('login'))

    user = User.query.filter_by(email=current_user.email).first()
    checkout = Checkout.query.filter_by(email=current_user.email).first()
    if checkout == None:
        flash('You must checkout to receive an invoice.')
        return redirect(url_for('checkout'))
    products=Product.query.all()

    return render_template('invoice.html',checkout=checkout,products=products,user=user)

@app.route("/ship")
def ship():
    if not(current_user.is_authenticated):
        flash('You must login to do this.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=current_user.email).first()
    checkout = Checkout.query.filter_by(email=current_user.email).first()
    if checkout == None:
        flash('You must checkout to receive a shipping label')
        return redirect(url_for('checkout'))
    products=Product.query.all()
    date = datetime.now()
    return render_template('ship.html',checkout=checkout,products=products,user=user, date=date.strftime("%d/%m/%y"))
