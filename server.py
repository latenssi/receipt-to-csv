import sys
import io
from flask import Flask, request, send_file, render_template

import lib
from config import BaseConfig

app = Flask(__name__)
app.config.from_object(BaseConfig)

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        if 'file' not in request.files:
            return "Invalid request", 400

        file = request.files['file']

        if not file.filename or file.filename == '':
            return "Invalid request", 400

        proxy = io.StringIO()
        lib.write_csv_buffer(proxy, lib.parse_pdf(file))

        mem = io.BytesIO()
        mem.write(proxy.getvalue().encode('utf-8'))
        mem.seek(0)

        proxy.close()

        return send_file(
            mem,
            as_attachment=True,
            attachment_filename=file.filename.replace(".pdf", ".csv"),
            mimetype='text/csv'
        )

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
