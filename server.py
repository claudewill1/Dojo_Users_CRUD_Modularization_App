from flask import Flask, render_template, request, redirect, session
from models.user import User
from env import KEY

app = Flask(__name__)
app.secret_key = KEY

# ------------Main landing page
@app.route("/")
def index():
    return redirect('/users')
# -------------Add user landing page
@app.route('/users/new')
def new():
    return render_template("create.html")
# ------------Hidden create user route
@app.route("/create",methods=["POST"])
def create_user():
    print(request.form)
    data = request.form
    User.save(data)
    # Don't forget to redirect after saving to the database
    return redirect("/users")

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
    User.update(data)
    return redirect('/users')

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

if __name__ == "__main__":
    app.run(debug=True)