import requests
import json
from flask import Flask


# изменения кода:
# добавляем в начало списка текущую и предыдущую даты курсов валют, а так же заголовки столбцов
def get_valutes_list():
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    response = requests.get(url)
    data = json.loads(response.text)

    # создаём словарь со значениями даты курсов валют, для упрощения нет преобразования даты
    dict1 = dict()
    dict1["Date"] = data['Date']                    # текущая дата курсов валют
    dict1["PreviousDate"] = data['PreviousDate']    # предыдущая дата курсов валют

    # создаём заголовки из ключей словаря первой валюты
    dict2 = dict()

    for caption in data['Valute']['AUD']:
        dict2[caption] = caption

    valutes_capt = list()
    valutes_capt.append(dict1)
    valutes_capt.append(dict2)

    # получаем значения всех валют, помещаем в список
    valutes = list(data['Valute'].values())

    return valutes_capt + valutes


app = Flask(__name__)


def create_html(valutes):
    text = '<h1>Курсы валют</h1>'
    cdate = valutes[0]['Date']          # для упрощения нет преобразования даты
    pdate = valutes[0]['PreviousDate']  # для упрощения нет преобразования даты
    text += f'<p>Дата: {cdate}</p>'
    text += f'<p>Предыдущая дата: {pdate}</p>'
    text += '<table>'
    text += '<tr>'
    for _ in valutes[0]:
        text += f'<th><th>'
    text += '</tr>'
    for valute in valutes:
        if (valute == valutes[0]):
            continue
        text += '<tr>'
        for v in valute.values():
            text += f'<td>{v}</td>'
        text += '</tr>'

    text += '</table>'
    return text


@app.route("/")
def index():
    valutes = get_valutes_list()
    html = create_html(valutes)
    return html


if __name__ == "__main__":
    app.run()