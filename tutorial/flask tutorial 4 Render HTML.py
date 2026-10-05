from flask import Flask
from markupsafe import escape
# from flask import escape
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello Dunia!</h1>'

@app.route('/about')
def about():
    return '<h1>About Us</h1>'

@app.route('/contact')
def contact():
    return '<h1>Contact Us</h1>'

@app.route('/profile', defaults={'_route': "home", 'nilai': 0})
@app.route('/profile/<int:nilai>', defaults={'_route': "profile"})
def profile_name(nilai, _route):
    if _route == "home":
        return '<h1>ProfileHome</h1>'
    elif _route == "profile":
        nilai = nilai + 100
        return '<h1>Hello %s!</h1>' % nilai

@app.route("/htmlescape/<code>")
def htmlescape(code):
    mystring = "~!@@@#$$%^&$%&$^^&(&)*_&*^&*%%$%^#@#@^$^YI+_(*+"
    return escape(mystring)
@app.route('/routetanpaslah')
def routetanpaslah():
    return '<h1>Route Tanpa Slah</h1>'

@app.route("/routedenganslah/")
def routedenganslah():
    return '<h1>Route Dengan Slah</h1>'

@app.route("/cobarequest", methods=['GET', 'POST'])
def cobarequest():
    if request.method == "GET":
        return '<h1>Coba GET</h1>'
    elif request.method == "POST":
        return '<h1>Coba POST</h1>'

@app.route('/render_template/')
def halaman_template():
    return render_template('index.html')


app.run(debug=True)