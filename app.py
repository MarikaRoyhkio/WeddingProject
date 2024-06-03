from flask import Flask, request, render_template, redirect, url_for, flash, session

import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def get_db_connection():
    conn = sqlite3.connect('guestlist.sql')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/rsvp', methods=['GET', 'POST'])
def rsvp():
    if request.method == 'POST':
        guests = []
        for i in range(1, 5):
            name = request.form.get(f'name_{i}')
            if name:
                status = request.form.get(f'status_{i}')
                food_allergies = request.form.get(f'food_allergies_{i}', '') if status == 'Kyllä' else ''
                song_request = request.form.get(f'song_request_{i}', '') if status == 'Kyllä' else ''
                guests.append((name, status, food_allergies, song_request))

        conn = get_db_connection()
        for guest in guests:
            name, status, food_allergies, song_request = guest
            print(f'Käsitellään vierasta {name}')
            guest_record = conn.execute('SELECT * FROM guests WHERE name = ?', (name,)).fetchone()
            if guest_record is None:
                flash(f'Nimeä {name} ei löydy vieraslistalta. ')
                conn.close()
                return redirect(url_for('rsvp'))
            
            print(f'Päivitetään vierasta {name}:n tietoja. Status: {status}, Allergiat: {food_allergies}, Toive: {song_request}')
            conn.execute('UPDATE guests SET rsvp_status = ?, food_allergies = ?, song_request = ? WHERE name = ?', 
                         (status, food_allergies, song_request, name))
        conn.commit()
        conn.close()

        flash ('Kiitos vastauksestasi!')
        return redirect(url_for('rsvp'))
    
    return render_template('rsvp.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    responded_guests = conn.execute('SELECT * FROM guests WHERE rsvp_status IS NOT NULL').fetchall()
    non_responded_guests = conn.execute('SELECT * FROM guests WHERE rsvp_status IS NULL').fetchall()
    conn.close()

    print('Responded Guests:')
    for guest in responded_guests:
        print(dict(guest))
        
    print('Non-responded Guests:')
    for guest in non_responded_guests:
        print(dict(guest))
    
    return render_template('admin.html', responded_guests=responded_guests, non_responded_guests=non_responded_guests)

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
            filename = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
            photo.save(filename)
            flash('Kiitos kuvien lähettämisestä!')
            return redirect(url_for('upload_photo'))
        
    return render_template('upload_photo.html')

@app.route('/schedule')
def schedule():
    return render_template('schedule.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()

        if user:
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            flash('Virheellinen käyttäjätunnus tai salasana')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

@app.route('/create_admin', methods=['GET', 'POST'])
def create_admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        
        flash('Admin-käyttäjä luotu onnistuneesti')
        return redirect(url_for('login'))
    
    return render_template('create_admin.html')

if __name__ == '__main__':
    app.run(debug=True)
    

