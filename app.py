from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'malana123'  # ubah ini jadi lebih aman di produksi
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'zip', 'rar', 'txt', 'html', 'mp4', 'mp3'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('Tidak ada file yang dipilih')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('Nama file kosong')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        flash(f'Berhasil diupload: {file.filename}')
        return redirect(url_for('index'))
    else:
        flash('Ekstensi file tidak diizinkan')
        return redirect(request.url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
