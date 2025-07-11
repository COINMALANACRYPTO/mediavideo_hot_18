from flask import Flask, render_template, request, send_from_directory, flash, redirect, url_for
import os
import uuid

app = Flask(__name__)
app.secret_key = "malana123"
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
        flash('❌ Tidak ada file dikirim')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('⚠️ Nama file kosong')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1]
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        download_link = url_for('download_file', filename=filename, _external=True)
        flash(f'✅ Berhasil diupload! 🔗 <a href="{download_link}" target="_blank">{download_link}</a>')
        return redirect(url_for('index'))
    else:
        flash('❌ Ekstensi file tidak diperbolehkan')
        return redirect(url_for('index'))

@app.route('/file/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
