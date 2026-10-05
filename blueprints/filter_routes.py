import os
from flask import Blueprint, render_template, request
from psycopg2.extras import RealDictCursor
from database import get_db_connection

filter_bp = Blueprint('filter_bp', __name__)

# Fungsi penolong untuk membaca file SQL
def load_sql_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

@filter_bp.route('/nr_playground_table_filter/', methods=['GET'])
def filter_table():
    # 1. Tangkap input dari URL query
    start_date = request.args.get('start_date') or None
    end_date = request.args.get('end_date') or None
    min_depth = request.args.get('min_depth') or None
    max_depth = request.args.get('max_depth') or None
    selected_magtype = request.args.get('magtype') or None
    selected_type = request.args.get('type') or None

    end_date_full = f"{end_date} 23:59:59" if end_date else None
    min_depth_num = float(min_depth) if min_depth else None
    max_depth_num = float(max_depth) if max_depth else None

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    # 2. Ambil pilihan unik untuk dropdown
    cursor.execute("SELECT DISTINCT magtype FROM nr_playground_table1 WHERE magtype IS NOT NULL ORDER BY magtype;")
    magtype_options = [row['magtype'] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT type FROM nr_playground_table1 WHERE type IS NOT NULL ORDER BY type;")
    type_options = [row['type'] for row in cursor.fetchall()]

    # 3. Baca dan jalankan file SQL eksternal
    sql_path = os.path.join('queries', 'filter_query.sql')
    query = load_sql_file(sql_path)

    params = (
        start_date, start_date,
        end_date_full, end_date_full,
        min_depth_num, min_depth_num,
        max_depth_num, max_depth_num,
        selected_magtype, selected_magtype,
        selected_type, selected_type
    )

    cursor.execute(query, params)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description] if cursor.description else []

    cursor.close()
    conn.close()

    return render_template(
        'flask-dari-postgre-filter.html',
        rows=rows,
        columns=columns,
        magtype_options=magtype_options,
        type_options=type_options,
        filters={
            'start_date': start_date or '',
            'end_date': end_date or '',
            'min_depth': min_depth or '',
            'max_depth': max_depth or '',
            'magtype': selected_magtype or '',
            'type': selected_type or ''
        }
    )