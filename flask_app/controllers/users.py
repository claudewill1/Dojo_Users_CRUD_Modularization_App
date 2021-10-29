from flask_app import app
from flask import render_template,redirect,request,session
from flask_app.models.user import User
# ------------Main landing page
@app.route("/")
def index():
    return redirect('/users')

@app.route('/users/<int:id>')
def users(id):
    data = {
        "id": id
    }
    return render_template("show_user.html",user=User.getOne(data))
# -------------Add user landing page
@app.route('/users/new')
def new():
    return render_template("create.html")
# ------------Hidden create user route
@app.route("/create",methods=["POST"])
def create_user():
    print(request.form)
    data = request.form
    user = User.save(data)
    # Don't forget to redirect after saving to the database
    session['id'] = user
    return redirect(f"/users/{user}")

#-------Route to update user page
@app.route("/users/show/<int:id>")
def show_user(id):
    data = {
        "id": id
    }
    return render_template("show_user.html",user = User.getOne(data))

@app.route('/users/edit/<int:id>')
def edit(id):
    data = {
        "id": id
    }
    return render_template("update.html",user = User.getOne(data))

# ------ Hidden update user route
@app.route("/users/update/<int:id>",methods=["POST"])
def update(id):
    data = {
        "id": id,
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"]
    }
    user = User.update(data)
    
    return redirect(f"/users/{id}")

#---- Hidden delete route (only used to delete a record from table)
@app.route('/users/delete/<int:id>')
def delete(id):
    data = {
        "id": id
    }
    User.delete(data)
    return redirect("/")

@app.route('/users')
def display_users():
    users = User.get_all()
    return render_template("users.html",all_users = users)