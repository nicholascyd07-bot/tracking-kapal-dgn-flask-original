#File Python Utama
from flask import Flask
from blueprints.raw_routes import raw_bp
from blueprints.filter_routes import filter_bp
from blueprints.filter_routes_2 import filter_bp_2
from blueprints.insert_data import insert_bp
from blueprints.disaster_type_pie import disaster_type_pie_bp

app = Flask(__name__)

# Daftarkan masing-masing blueprint ke aplikasi Flask utama
app.register_blueprint(raw_bp)
app.register_blueprint(filter_bp)
app.register_blueprint(filter_bp_2)
app.register_blueprint(insert_bp)
app.register_blueprint(disaster_type_pie_bp)

if __name__ == '__main__':
    app.run(port=5002, debug=True)