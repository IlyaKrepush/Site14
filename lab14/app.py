from flask import render_template, request, redirect, flash
from forms import ProductForm, LoginForm, AuthozizateForm
from table import Users, Products, db, app
from flask_login import login_required, logout_user, LoginManager, login_user
from werkzeug.security import check_password_hash, generate_password_hash


from sqlalchemy import create_engine, Table, MetaData, select



login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


@app.route('/', methods=['GET', 'POST'])
def home():
    products=Products.query.order_by(Products.id).all()
    return render_template("home.html", products=products)


@app.route('/edit', methods=['GET', 'POST'])
def edit():

    if request.method == 'POST':
        type=request.form['type']
        name=request.form['name']
        description=request.form['description']
        manufacturer=request.form['manufacturer']
        price=request.form['price']
        photo=request.files['photo']

        price=int(price)

        products=Products(type=type, name=name, description=description, manufacturer=manufacturer, price=price, photo=photo.filename)
        db.session.add(products)
        db.session.commit()
        return redirect('/')
    else: 
        return render_template('edit.html', form=ProductForm())


@app.route('/login', methods=['GET', 'POST'])
def login():

    form=LoginForm()

    if form.validate_on_submit():

        login=form.login.data
        password=form.password.data

        user = Users.query.filter_by(login=login).first()
        
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect('/')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():

    form=AuthozizateForm()

    if form.validate_on_submit():

        login=form.login.data
        password=form.password.data

        hash_password=generate_password_hash(password)
        new_user=Users(login=login, password=hash_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')

    else: 
        return render_template('register.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/')

# Редактирование карточек
@app.route('/edit/<int:idr>/ed', methods=["GET","POST"])
def edite(idr):
    form=ProductForm()

    if request.method == "POST":

        type = request.form['type']
        name = request.form['name']
        description = request.form['description']
        manufacturer = request.form['manufacturer']
        price = request.form['price']
        photo = request.files['photo']
        print(type)

        engine = create_engine("sqlite:///instance/base.db", echo=True)
        meta = MetaData(engine)
        products = Table("Products", meta, autoload=True)
        conn = engine.connect()

        mass_db=[]
        column=0

        s = select(products).where(products.c.id == idr)
        result=conn.execute(s)

        for raw in result:
            pass

        for i in (type, name, description, manufacturer, price, photo):
            column += 1
            if i:
                mass_db.append(i)
            else:
                mass_db.append(raw[column])
        s = products.update().where(products.c.id == idr).values(type=mass_db[0],name=mass_db[1],description=mass_db[2],manufacturer=mass_db[3],price=mass_db[4],photo=mass_db[5])
        conn.execute(s)
        return redirect('/')

    return render_template('edit_admin.html',form=form)
# def delete - УДАЛЕНИЕ КАРТОЧЕК !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@app.route('/delete/<int:id>/del')
def delete(id):
    print('happy')
    u = db.session.get(Products, id)
    db.session.delete(u)
    db.session.commit()
    return redirect('/')

@app.route('/db/base')
def base():
    engine = create_engine("sqlite:///instance/base.db", echo=True)
    meta = MetaData(engine)
    products = Table("Products", meta, autoload=True)
    conn = engine.connect()

    s = products.select()
    result = conn.execute(s)
    for raw in result:
        print(raw)
    return("base.html")








if __name__ == '__main__':
    app.run(debug=True)





