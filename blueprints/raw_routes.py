from flask import Blueprint, render_template
from psycopg2.extras import RealDictCursor
from database import get_db_connection

raw_bp = Blueprint('raw_bp', __name__)

@raw_bp.route('/nr_playground_table1_raw/')
def show_table_raw():
    data = []
    columns = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM nr_playground_table1 ORDER BY time DESC;")
        data = cursor.fetchall()
        if cursor.description:
            columns = [desc[0] for desc in cursor.description]
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error database: {e}")

    return render_template('flask-dari-postgre.html', columns=columns, rows=data)