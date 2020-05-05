from flask import Flask, render_template, request, session,redirect
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
app.secret_key = 'super-secret key'
# app.config.update(
#     MAIL_SERVER = 'smtp.gmail.com',
#     MAIL_PORT = '465',
#     MAIL_USE_SSL = True,
#     MAIL_USERNAME = params['user'],
#     MAIL_PASSWORD = params['pass']
# )
# mail = Mail(app)
ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_url']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_url']
    

db = SQLAlchemy(app)

class Contacts(db.Model):
    __tablename__ = 'contacts'
    sno = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    Phone = db.Column(db.String(15), nullable=False)
    Message = db.Column(db.String(1200), nullable=False)
    Date = db.Column(db.String(120), nullable=True)

    def __init__(self, Name, Email, Phone, Message, Date):
        self.Name = Name
        self.Email = Email
        self.Phone = Phone  
        self.Message = Message 
        self.Date = Date


class Form(db.Model):
    __tablename__ = 'form'
    sno = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)

    def __init__(self, first_name, last_name, year, month, day):
        self.first_name =first_name
        self.last_name = last_name
        self.year =year  
        self.month = month 
        self.day = day

class Posts(db.Model):
    __tablename__ = 'posts'
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(800), nullable=False)
    slug = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(1500), nullable=False)
    date = db.Column(db.String(30), nullable=True)
    img_file = db.Column(db.String(120), nullable=False)

    def __init__(self, title, slug, content, date, img_file):
        self.title = title
        self.slug =slug
        self.content =content  
        self.date =date 
        self.img_file =img_file
    




@app.route('/')
def home():
    
    posts = Posts.query.filter_by().all()
    return render_template('index.html' ,params = params ,info = info , posts=posts)

@app.route("/post/<string:post_slug>", methods=['GET'])
def post_route(post_slug):
    
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', params=params, post=post, info=info)


@app.route('/about')
def about():
    return render_template("about.html" ,params = params ,info = info)

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')


@app.route('/login' ,methods = ['GET', 'POST'])
def login():
    if ('user' in session and session['user'] == info['user_name']):
        posts = Posts.query.all()
        return render_template('dashboard.html', info = info, params =params, posts = posts)




    if (request.method == 'POST'):
        username = request.form.get('uname')
        password = request.form.get('Pass')
        if (username == info['user_name'] and password == info['password']):
            
            session['user'] = username
            posts = Posts.query.all()


            return render_template('dashboard.html', info = info, params =params, posts = posts)
    return render_template("login.html" ,params = params ,info = info)

@app.route("/edit/<string:sno>", methods = ['GET' , 'POST'])
def edit(sno):
    if ('user' in session and session['user'] == info['user_name']):
        if (request.method == 'POST'):
            box_title = request.form.get('title')
            box_slug = request.form.get('slug')
            box_content = request.form.get('content')
            box_image = request.form.get('image')
            date = datetime.now()
            
            if (sno == '0' ):
                enter = Posts(title = box_title , slug = box_slug , content = box_content , img_file = box_image , date = date)
                db.session.add(enter)
                db.session.commit()

            else:
                post = Posts.query.filter_by(sno=sno).first()
                post.title = box_title
                post.slug = box_slug
                post.content = box_content
                post.img_file = box_image
                post.date = date
                db.session.commit()
                return redirect('/edit/'+sno)

        post = Posts.query.filter_by(sno=sno).first()

        return render_template("edit.html" ,params = params ,info = info, post =post)


@app.route("/delete/<string:sno>", methods = ['GET' , 'POST'])
def delete(sno):
    if ('user' in session and session['user'] == info['user_name']):
        post = Posts.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
    return redirect('/login')


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
        # mail.send_message('New message from Blog' , sender= name  , body = message , recipients = [params['user']]  )
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
if __name__ == '__main__':

    app.debug = True
    app.run()