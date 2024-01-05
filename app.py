"""Blogly application."""

from flask import Flask, request, redirect, render_template, abort, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from flask_migrate import Migrate

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_ENABLED'] = True 

connect_db(app)

migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

@app.route('/')
def root():
    return redirect("/users")

@app.route('/users')
def users_index():

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users.html', users=users)

@app.route('/users/new', methods=["GET"])
def create_form():
    return render_template('create_user.html')


@app.route('/users/new', methods=["POST"])
def create_user():
    first_name = request.form['fname']
    last_name = request.form['lname']
    image_url = request.form.get('img') or 'https://i.pinimg.com/564x/b9/b7/8f/b9b78feef136d29fc6ac7cffc12bc991.jpg'

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        image_url=image_url
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:id>')
def user_detail(id):
    user = User.query.get(id)
    if not user:
        abort(404)
    return render_template('user_detail.html', user=user)


@app.route('/users/<int:id>/edit', methods=["GET", "POST"])
def users_edit(id):
    user = User.query.get_or_404(id)
    
    if request.method == "POST":
        user.first_name = request.form['edit-fname']
        user.last_name = request.form['edit-lname']
        user.image_url = request.form['edit-img']

        db.session.commit()

        return redirect("/users")

    return render_template('edit_user.html', user=user)

@app.route('/users/<int:id>/delete', methods = ["POST"])
def delete_user(id):
    user = User.query.get_or_404(id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

if __name__ == '__main__':
    app.run(debug=True)
