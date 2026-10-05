import io
import base64
from flask import Blueprint, render_template, request
from psycopg2.extras import RealDictCursor
from database import get_db_connection

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

disaster_type_pie_bp = Blueprint('disaster_type_pie_bp', __name__)

@disaster_type_pie_bp.route('/disaster_type_pie/', methods=['GET'])
def disaster_type_pie():
    # 1. Tangkap parameter filter dari query URL (tanpa 'type')
    start_date = request.args.get('start_date') or None
    end_date = request.args.get('end_date') or None
    min_depth = request.args.get('min_depth') or None
    max_depth = request.args.get('max_depth') or None
    
    selected_magtype = request.args.getlist('magtype')
    selected_magtype = [m for m in selected_magtype if m]

    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # 2. Ambil opsi checklist magtype untuk form
        cur.execute("SELECT DISTINCT magtype FROM nr_playground_table1 WHERE magtype IS NOT NULL ORDER BY magtype;")
        magtype_options = [row['magtype'] for row in cur.fetchall()]

        # 3. Susun Query Dinamis dengan Filter
        base_query = """
            SELECT type, COUNT(*) as total
            FROM nr_playground_table1
        """
        conditions = ["type IS NOT NULL"]
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

        # Gabungkan klausa WHERE
        query = base_query + " WHERE " + " AND ".join(conditions) + " GROUP BY type ORDER BY total DESC;"

        cur.execute(query, params)
        data = cur.fetchall()

        # Matplotlib Chart Generator
        chart_url = None
        if data:
            labels = [row['type'].capitalize() for row in data]
            totals = [row['total'] for row in data]

            fig, ax = plt.subplots(figsize=(6, 5))
            colors = ['#3498db', '#e74c3c', '#2ecc71', '#f1c40f', '#9b59b6']
            
            wedges, texts, autotexts = ax.pie(
                totals, 
                labels=labels, 
                autopct='%1.1f%%',
                startangle=140,
                colors=colors[:len(labels)],
                wedgeprops=dict(edgecolor='white', linewidth=1.5)
            )

            plt.setp(autotexts, size=10, weight="bold", color="white")
            plt.setp(texts, size=11)
            ax.set_title("Perbandingan Jumlah Kejadian Berdasarkan Jenis Bencana", fontsize=12, pad=20)
            plt.tight_layout()

            img_bytes = io.BytesIO()
            plt.savefig(img_bytes, format='png', dpi=150, bbox_inches='tight')
            img_bytes.seek(0)
            plt.close(fig)

            chart_url = base64.b64encode(img_bytes.getvalue()).decode('utf-8')

        return render_template(
            'disaster_type_pie.html', 
            chart_url=chart_url, 
            raw_data=data,
            magtype_options=magtype_options,
            filters={
                'start_date': start_date or '',
                'end_date': end_date or '',
                'min_depth': min_depth or '',
                'max_depth': max_depth or '',
                'magtype': selected_magtype
            }
        )

    except Exception as e:
        return f"Terjadi kesalahan saat membuat chart: {str(e)}", 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()