from flask import Flask, render_template, request, url_for, flash
import psycopg2.extras

app = Flask(__name__)
app.secret_key = 'ferygantengsekali'

DB_HOST = 'localhost'
DB_NAME = 'data_mahasiswa'
DB_USER = 'postgres'
DB_PASS = 'Ncnc1234'

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

@app.route('/')
def index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = 'SELECT * FROM mahasiswa'
    cur.execute(s)
    list_users = cur.fetchall()
    return render_template('index.html', list_users = list_users)

@app.route('/add_mahasiswa', methods=['POST'])
def add_mahasiswa():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        name = request.form['name']
        jurusan = request.form['jurusan']
        ipk = request.form['ipk']
        cur.execute('INSERT INTO mahasiswa (name, jurusan, ipk) VALUES (%s,%s,%i)', (name, jurusan, ipk))
        conn.commit()
        flash ('Mahasiswa berhasil ditambah')
        return redirect(url_for('index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_mahasiswa(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT FROM mahasiswa WHERE id = %s' (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', mahasiswa = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_mahasiswa(id):
    if request.method == 'POST':
        name = request.form['name']
        jurusan = request.form['jurusan']
        ipk = request.form['ipk']
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            UPDATE mahasiswa
            SET name = %s,
                jurusan = %s,
                ipk = %i
            WHERE id = %s
            """, (name, jurusan, ipk, id))
    flash ('Mahasiswa berhasil di update')
    conn.commit()
    return redirect(url_for('index'))

@app.route('/delete/<string:id>', methods = ['POST', 'GET'])
def delete_mahasiswa(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('DELETE FROM mahasiswa WHERE id = {0}'.format(id))
    conn.commit()
    flash('Data mahasiswa berhasil dihapus')
    return redirect(url_for(index))


if __name__ == '__main__':
    app.run(debug=True)
