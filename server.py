from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
import requests
from Blog import Blog
from LoginForm import LoginForm

app = Flask(__name__)
app.secret_key = "secret"
blog = Blog()


@app.route("/")
def home():
    return render_template("index.html", all_posts=blog.all_post)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/guess/<name>")
def guess(name):
    gender_url = f"https://api.genderize.io?name={name}"
    genderResponse = requests.get(gender_url)
    gender_data = genderResponse.json()
    gender = gender_data.get("gender")
    age_url = f"https://api.agify.io?name={name}"
    ageResponse = requests.get(age_url)
    age_data = ageResponse.json()
    age = age_data.get("age")
    return render_template(
        "guess.html", person_name=name, person_gender=gender, person_age=age
    )


@app.route("/post/<id>")
def get_post(id):
    post_data = blog.getPost(id)
    return render_template("post.html", post_data=post_data)


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if (
            login_form.email.data == "admin@gmail.com"
            and login_form.password.data == "password"
        ):
            return redirect("/")
        else:
            return render_template("denied.html")
    return render_template("login.html", form=login_form)


@app.route("/form-entry", methods=["POST"])
def receive_data():
    data = request.form
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    message = data.get("message")
    print(name, email, phone, message)
    return "<h1>Successfully sent your message</h1>"


if __name__ == "__main__":
    app.run(debug=True)
