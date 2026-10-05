from flask import Flask, render_template, request
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 5432,
    'database': 'nodered_db',
    'user': 'postgres',
    'password': '6969'
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# 1. Route Raw Data (Tetap Dikehaltan)
@app.route('/')
@app.route('/nr_playground_table1_raw/')
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


# 2. Route Filter Data (Gunakan trailing slash di akhir)
@app.route('/nr_playground_table1_filter/', methods=['GET'])
def filter_table():
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    min_depth = request.args.get('min_depth', '')
    max_depth = request.args.get('max_depth', '')
    selected_magtype = request.args.get('magtype', '')
    selected_type = request.args.get('type', '')

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    # Ambil opsi unik untuk dropdown magtype & type
    cursor.execute("SELECT DISTINCT magtype FROM nr_playground_table1 WHERE magtype IS NOT NULL ORDER BY magtype;")
    magtype_options = [row['magtype'] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT type FROM nr_playground_table1 WHERE type IS NOT NULL ORDER BY type;")
    type_options = [row['type'] for row in cursor.fetchall()]

    # Query Dinamis
    query = "SELECT * FROM nr_playground_table1 WHERE 1=1"
    params = []

    if start_date:
        query += " AND time >= %s"
        params.append(start_date)
    if end_date:
        query += " AND time <= %s"
        params.append(f"{end_date} 23:59:59")

    if min_depth:
        query += " AND depth >= %s"
        params.append(float(min_depth))
    if max_depth:
        query += " AND depth <= %s"
        params.append(float(max_depth))

    if selected_magtype:
        query += " AND magtype = %s"
        params.append(selected_magtype)
    if selected_type:
        query += " AND type = %s"
        params.append(selected_type)

    query += " ORDER BY time DESC;"

    cursor.execute(query, params)
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description] if cursor.description else []

    cursor.close()
    conn.close()

    return render_template(
        'flask-dari-postgre-filter.html',
        rows=data,
        columns=columns,
        magtype_options=magtype_options,
        type_options=type_options,
        filters={
            'start_date': start_date,
            'end_date': end_date,
            'min_depth': min_depth,
            'max_depth': max_depth,
            'magtype': selected_magtype,
            'type': selected_type
        }
    )

if __name__ == '__main__':
    app.run(port=5002, debug=True)