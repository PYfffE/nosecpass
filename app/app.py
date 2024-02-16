import garbage_collector

from flask import Flask, render_template, request, url_for, send_file
import memcached_toolkit
import os
from datetime import timedelta
from config import server_config


app = Flask(__name__)

app.config['DEBUG'] = server_config['DEBUG']
app.config['TEMP_LINK_DURATION'] = timedelta(hours=1)  # Время действия одноразовой ссылки
app.config['UPLOAD_DIR'] = 'uploads'

# Rewrite env from docker-compose  .env file
app.config.from_prefixed_env()



def save_file(file, filename):
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return filename

@app.route('/note', methods=['POST'])
def upload_note():
    if request.method == 'POST':
        uploaded_text = request.form['text_note'].replace('\r','')
        note_uuid = memcached_toolkit.create_note(uploaded_text)
        # host = request.headers.get('Host', '')
        temp_link = url_for('download', temp_uuid=note_uuid, _external=True, _scheme='https')
        # temp_link = f'https://{host}/download/{note_uuid}'
        return render_template('show_temp_link.html', temp_link=temp_link)


@app.route('/file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        file_uuid = memcached_toolkit.create_file(uploaded_file)
        temp_link = url_for('download', temp_uuid=file_uuid, _external=True, _scheme='https')
        return render_template('show_temp_link.html', temp_link=temp_link)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/download/<temp_uuid>')
def download(temp_uuid):
    file_meta = memcached_toolkit.get_created_file(temp_uuid)

    if file_meta is None:
        return render_template('404.html'), 404

    if file_meta['is_note']:
        note_data = open(os.path.join('./uploads', temp_uuid), 'r', encoding='utf-8').read()
        memcached_toolkit.remove_entry(temp_uuid)
        return render_template('note_display.html', note_data=note_data)

    else:
        if request.args.get('confirm') is None:
            return render_template('file_display.html')
        memcached_toolkit.remove_entry(temp_uuid)

        print('before_response')

        return send_file(os.path.join('./uploads', temp_uuid), download_name=file_meta['real_filename'], as_attachment=True)


if __name__ == '__main__':
    garbage_collector.init_scheduler()
    app.run()

else:
    garbage_collector.init_scheduler()