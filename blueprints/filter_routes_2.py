import io
import os
import pandas as pd
from flask import Blueprint, render_template, request, send_file
from psycopg2.extras import RealDictCursor
from database import get_db_connection

filter_bp_2 = Blueprint('filter_bp_2', __name__)

@filter_bp_2.route('/nr_playground_table_filter_2/', methods=['GET'])
def filter_table_2():
    # 1. Tangkap parameter action ('filter' atau 'export')
    action = request.args.get('action')
    
    # Tangkap input dari URL query
    start_date = request.args.get('start_date') or None
    end_date = request.args.get('end_date') or None
    min_depth = request.args.get('min_depth') or None
    max_depth = request.args.get('max_depth') or None
    selected_type = request.args.get('type') or None
    
    # Tangkap checklist magtype sebagai list
    selected_magtype = request.args.getlist('magtype')
    selected_magtype = [m for m in selected_magtype if m]

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # 2. Ambil pilihan opsi untuk dropdown / checklist
        cursor.execute("SELECT DISTINCT magtype FROM nr_playground_table1 WHERE magtype IS NOT NULL ORDER BY magtype;")
        magtype_options = [row['magtype'] for row in cursor.fetchall()]

        cursor.execute("SELECT DISTINCT type FROM nr_playground_table1 WHERE type IS NOT NULL ORDER BY type;")
        type_options = [row['type'] for row in cursor.fetchall()]

        # 3. Susun Query Dinamis
        query = "SELECT * FROM nr_playground_table1"
        conditions = []
        params = []

        if start_date:
            conditions.append("time >= %s::timestamp")
            params.append(start_date)

        if end_date:
            conditions.append("time <= %s::timestamp")
            params.append(f"{end_date} 23:59:59")

        if min_depth:
            conditions.append("depth >= %s")
            params.append(float(min_depth))

        if max_depth:
            conditions.append("depth <= %s")
            params.append(float(max_depth))

        if selected_magtype:
            conditions.append("magtype = ANY(%s)")
            params.append(selected_magtype)

        if selected_type:
            conditions.append("type = %s")
            params.append(selected_type)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY time DESC;"

        cursor.execute(query, params)
        rows = cursor.fetchall()

        # 4. Jika tombol Export Excel diklik (action == 'export')
        if action == 'export':
            if rows:
                df = pd.DataFrame(rows)
                # Hilangkan timezone dari kolom datetime agar openpyxl tidak crash
                for col in df.columns:
                    if pd.api.types.is_datetime64_any_dtype(df[col]) or isinstance(df[col].iloc[0], str) == False:
                        try:
                            df[col] = df[col].astype(str)
                        except Exception:
                            pass
            else:
                # Buat DataFrame kosong jika tidak ada data
                df = pd.DataFrame()

            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Data Filtered')
            output.seek(0)

            return send_file(
                output,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name='data_filtered_playground.xlsx'
            )

        # 5. Render HTML biasa jika bukan export
        columns = [desc[0] for desc in cursor.description] if cursor.description else []

        return render_template(
            'flask-dari-postgre-filter-2.html',
            rows=rows,
            columns=columns,
            magtype_options=magtype_options,
            type_options=type_options,
            filters={
                'start_date': start_date or '',
                'end_date': end_date or '',
                'min_depth': min_depth or '',
                'max_depth': max_depth or '',
                'magtype': selected_magtype,
                'type': selected_type or ''
            }
        )

    except Exception as e:
        return f"Terjadi kesalahan saat export data: {str(e)}", 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()