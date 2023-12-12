from flask import Flask, render_template, request, redirect, url_for, send_file
import memcached_toolkit
import os
import uuid
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['TEMP_LINK_DURATION'] = timedelta(hours=1)  # Время действия одноразовой ссылки

def save_file(file, filename):
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return filename

@app.route('/note', methods=['POST'])
def upload_note():
    if request.method == 'POST':
        uploaded_text = request.form['text_note']
        temp_uuid = memcached_toolkit.create_note(uploaded_text)

        return url_for('download', temp_uuid=temp_uuid)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file:
            filename = save_file(uploaded_file)
            # Здесь можно добавить логику хранения временных ссылок и их срока действия
            return f"Файл загружен успешно. Ваша одноразовая ссылка: {url_for('download', temp_uuid=filename, _external=True)}"

    return render_template('index.html')

@app.route('/download/<temp_uuid>')
def download(temp_uuid):
    file_meta = memcached_toolkit.get_created_file(temp_uuid)
    if file_meta['creation_date']:
        return open(os.path.join('uploads', temp_uuid), 'r')
    return 'Heh'

if __name__ == '__main__':
    app.run(debug=True)
