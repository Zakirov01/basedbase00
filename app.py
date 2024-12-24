from flask import Flask, request, render_template
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'data/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_data():
    # Обработка текстового ввода или файла
    if 'datafile' in request.files:
        file = request.files['datafile']
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            # Определяем тип файла
            if file.filename.endswith('.csv'):
                data = pd.read_csv(filepath)
            elif file.filename.endswith(('.xls', '.xlsx')):
                data = pd.read_excel(filepath)
            elif file.filename.endswith('.txt'):
                data = pd.read_csv(filepath, delimiter="\t", header=None)  # Чтение TXT
            else:
                return "Формат файла не поддерживается. Загрузите CSV, Excel или TXT."
    elif 'textdata' in request.form:
        text_data = request.form['textdata']
        # Преобразуем текст в таблицу (разделитель - запятая)
        rows = [row.split(",") for row in text_data.strip().split("\n")]
        data = pd.DataFrame(rows[1:], columns=rows[0])
    else:
        return "Необходимо загрузить файл или ввести данные!"

    # Обработка данных
    data = data.sort_values(by=data.columns[0])  # Сортировка по первому столбцу

    # Преобразуем данные в HTML
    table_html = data.to_html(classes='table table-bordered', index=False)

    return render_template('result.html', table_html=table_html)

if __name__ == '__main__':
    app.run(debug=True)
