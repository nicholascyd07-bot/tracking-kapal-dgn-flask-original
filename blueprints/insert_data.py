import pandas as pd
from flask import Blueprint, render_template, request, redirect, url_for, flash
from psycopg2.extras import execute_values

from database import get_db_connection

insert_bp = Blueprint('insert_bp', __name__)

@insert_bp.route('/insert_data/', methods=['GET', 'POST'])
def insert_data():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Tidak ada file yang dipilih!', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('Tidak ada file yang dipilih!', 'error')
            return redirect(request.url)

        if not file.filename.endswith(('.xlsx', '.xls')):
            flash('Format file harus .xlsx atau .xls!', 'error')
            return redirect(request.url)

        conn = None
        cur = None
        try:
            # 1. Baca file Excel
            df = pd.read_excel(file)
            df.columns = df.columns.str.strip()

            # 2. Koneksi ke Database
            conn = get_db_connection()
            cur = conn.cursor()
            
            # 3. Ambil struktur kolom tabel di DB
            cur.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'nr_playground_table1';
            """)
            db_columns = [row[0] for row in cur.fetchall()]

            if not db_columns:
                flash("Tabel nr_playground_table1 tidak ditemukan di pangkalan data!", 'error')
                return redirect(request.url)

            # 4. Validasi kesesuaian kolom
            excel_columns = list(df.columns)
            missing_cols = set(db_columns) - set(excel_columns)
            
            if missing_cols:
                flash(f"Gagal! Kolom file Excel tidak cocok. Kolom kurang: {', '.join(missing_cols)}", 'error')
                return redirect(request.url)

            # 5. Filter & urutkan kolom sesuai DB
            df = df[db_columns]

            # PERBAIKAN UTAMA: Konversi tipe data Pandas/Numpy ke tipe data native Python
            # agar psycopg2 bisa memprosesnya tanpa error 500
            df = df.astype(object)
            df = df.where(pd.notnull(df), None)

            # 6. Query INSERT
            cols_str = ", ".join([f'"{col}"' for col in db_columns])  # Menggunakan kutip ganda untuk nama kolom
            query = f"""
                INSERT INTO nr_playground_table1 ({cols_str})
                VALUES %s
                ON CONFLICT (id) DO NOTHING;
            """

            # Konversi baris DataFrame menjadi list of tuple native Python
            values = [tuple(x) for x in df.to_numpy()]

            execute_values(cur, query, values)
            conn.commit()

            flash('Berhasil! Data telah dimasukkan ke dalam tabel nr_playground_table1.', 'success')
            return redirect(url_for('insert_bp.insert_data'))

        except Exception as e:
            if conn:
                conn.rollback()  # Rollback transaksi jika terjadi error
            flash(f'Terjadi kesalahan saat memproses file: {str(e)}', 'error')
            return redirect(request.url)

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    return render_template('insert_data.html')