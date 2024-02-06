from flask import Flask, request
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/img/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Загрузка фотографии для участия в миссии</title>
        <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
        <!-- Bootstrap CSS -->
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <style>
            body {
                background-color: #f8f9fa;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                border: 2px solid #007bff;
                border-radius: 10px;
                background-color: #fff;
                box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
                animation: slide-up 0.5s ease;
            }
            @keyframes slide-up {
                from {
                    opacity: 0;
                    transform: translateY(50px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            h1 {
                color: #007bff;
                text-align: center;
                margin-bottom: 30px;
                font-size: 2.5em;
            }
            .form-group {
                margin-bottom: 20px;
            }
            .btn-upload {
                background-color: #007bff;
                border-color: #007bff;
                transition: all 0.3s ease;
            }
            .btn-upload:hover {
                background-color: #0056b3;
                border-color: #0056b3;
            }
            .img-thumbnail {
                max-width: 100%;
                height: auto;
            }
            .success-message {
                text-align: center;
                color: #28a745;
                font-size: 1.5em;
                margin-top: 20px;
            }
            .error-message {
                text-align: center;
                color: #dc3545;
                font-size: 1.5em;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container mt-5">
            <h1>Загрузка фотографии для участия в миссии</h1>
            <form method="POST" action="/upload" enctype="multipart/form-data">
                <div class="form-group">
                    <input type="file" class="form-control-file" name="file" id="file">
                </div>
                <button type="submit" class="btn btn-primary btn-block btn-upload">Загрузить</button>
            </form>
            <div class="mt-4">
                <h2>Загруженное фото:</h2>
                <img src="" alt="Загруженное фото" class="img-thumbnail" id="uploaded_img">
            </div>
        </div>
        <div id="message"></div>
        <script>
            document.querySelector("#file").addEventListener("change", function() {
                const reader = new FileReader();
                reader.onload = function() {
                    document.querySelector("#uploaded_img").src = reader.result;
                }
                reader.readAsDataURL(this.files[0]);
            });
        </script>
    </body>
    </html>
    '''


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file.filename == '':
        return index().replace('<div id="message"></div>', '<p class="error-message">Файл не выбран</p>')
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return index().replace('<div id="message"></div>', '<p class="success-message">Файл успешно загружен!</p>')
    else:
        return index().replace('<div id="message"></div>',
                               '<p class="error-message">Допустимые форматы файлов: png, jpg, jpeg, gif</p>')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
