from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json
from datetime import datetime

with open('config.json', 'r') as c:
    params = json.load(c)["params"]
with open('config.json', 'r') as d:
    info = json.load(d)["info"]
local_server = "True"

app = Flask(__name__)
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['user'],
    MAIL_PASSWORD = params['pass']
)
mail = Mail(app)
if (local_server):
     app.config['SQLALCHEMY_DATABASE_URI'] = params['local_url']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_url']
db = SQLAlchemy(app)

class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    Phone = db.Column(db.String(13), nullable=False)
    Message = db.Column(db.String(12), nullable=False)
    Date = db.Column(db.String(120), nullable=True)

class Form(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)

class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(25), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    img_file = db.Column(db.String(120), nullable=False)
    




@app.route('/')
def home():
    
    posts = Posts.query.filter_by().all()[0:2]
    return render_template('index.html' ,params = params ,info = info , posts=posts)

@app.route("/post/<string:post_slug>", methods=['GET'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', params=params, post=post, info=info)


@app.route('/about')
def about():
    return render_template("about.html" ,params = params ,info = info)
@app.route('/login')
def login():
    return render_template("login.html" ,params = params ,info = info)

@app.route('/contact' ,methods = ['GET' , 'POST'])
def contact():
    if (request.method== 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(Name = name , Email = email , Phone = phone , Message = message , Date = datetime.now())
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from Blog' , sender= name  , body = message , recipients = [params['user']]  )
    return render_template("contact.html" ,params = params, info = info)



@app.route('/form' ,methods = ['GET' , 'POST'])
def form():
    if (request.method== 'POST'):
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        year = request.form.get('year')
        month = request.form.get('mth')
        day = request.form.get('day')
        entry = Form(first_name = fname , last_name = lname , year = year , month = month , day = day)
        db.session.add(entry)
        db.session.commit()
        return render_template("navbar.html" ,params = params , info = info )
app.run(debug=True)