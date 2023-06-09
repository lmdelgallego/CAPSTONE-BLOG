from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap
from datetime import date
import requests
from Post import CreatePostForm
from Blog import Blog
from LoginForm import LoginForm


app = Flask(__name__)
ckeditor = CKEditor(app)
Bootstrap(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

app.secret_key = "secret"
blog = Blog()


# #CONFIGURE TABLE

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        """<Post {self.title}>"""


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)


@app.route("/post/<post_id>")
def get_post(post_id):
    # post_data = blog.getPost(BlogPost, id)
    post_data = BlogPost.query.get(post_id)
    return render_template("post.html", post_data=post_data)


@app.route("/edit-post/<post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        body=post.body,
        img_url=post.img_url,
        author=post.author,
    )

    if form.validate_on_submit():
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.body = form.body.data
        post.img_url = form.img_url.data
        post.author = form.author.data
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("make-post.html", form=form, is_edit=True)


@app.route("/new-post", methods=["GET", "POST"])
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            date=date.today().strftime("%B %d, %Y"),
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=form.author.data,
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("make-post.html", form=form)


@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


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
