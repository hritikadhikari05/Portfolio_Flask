from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def about():
    name = "Hritik" 
    return render_template('about.html', name2 = name)

@app.route('/more')
def index():
    return render_template("index.html")
@app.route('/nav')
def nav():
    return render_template("navbar.html")
app.run(debug=True)
