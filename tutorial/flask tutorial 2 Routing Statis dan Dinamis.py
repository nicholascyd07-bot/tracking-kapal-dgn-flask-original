from flask import Flask

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

app.run(debug=True)