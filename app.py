from flask import Flask, request, render_template, redirect, url_for, flash
from flask_mail import Mail, Message
import sqlite3
import os


app = Flask(__name__)
app.secret_key = 'supersecretkey'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] ='testerusermxbw@gmail.com'
app.config['MAIL_PASSWORD'] = '_kukkAhattUtatI85'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

def get_db_connection():
    conn = sqlite3.connect('guests.sql')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rsvp', methods=['POST'])
def rsvp():
    name = request.form['name']
    status = request.form['status']
    food_allergies = request.form.get('food_allergies', '')
    song_request = request.form.get('song_request', '')

    conn = get_db_connection()
    guest = conn.execute('SELECT * FROM guests WHERE name = ?',
(name,)).fetchone()

    if guest is None:
        flash('Nimeä ei löytynyt vieraslistalta. Tarkkista oikeinkirjoitus.')
        return redirect(url_for('index'))

    conn.execute('UPDATE guests SET rsvp_status = ?, food_allergies = ?, song_request = ? WHERE name = ?', (status, food_allergies, song_request, name))
    conn.commit()
    conn.close()

    flash ('Kiitos vastauksestasi!')
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    conn = get_db_connection()
    guests = conn.execute('SELECT * FROM guests').fetchall()
    conn.close()
    return render_template('admin.html', guests=guests)

@app.route('/upload_photo', methods=['GET', 'POST'])
def upload_photo():
    if request.method == 'POST':
        if 'photo' not in request.files:
            flash('Tiedostoa ei valittu')
            return redirect(request.url)
        
        photo = request.files['photo']
        if photo.filename == '':
            flash ('Tiedostoa ei valittu')
            return redirect(request.url)
        
        if photo:
            msg = Message('Uusi valokuva häistä',
                          sender ='testerusermxbw@gmail.com',
                          recipients=['testerusermxbw@gmail.com'])
            msg.body = 'Vieraat ovat lähettäneet kuvia häistä.'
            msg.attach(photo.filename, photo.content_type, photo.read())
            mail.send(msg)

            flash('Kiitos kuvien lähettämisestä!')
            return redirect(url_for('upload_photo'))
        
    return render_template('upload_photo.html)')

if __name__ == '__main__':
    app.run(debug=True)
    

