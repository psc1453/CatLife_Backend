from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    dict_data = {
        "column_names": ['excrete_date', 'urine', 'stool'],
        "values": [
            ('2023-10-19', 4, 1),
            ('2023-10-20', 5, 2)
        ]
    }
    return dict_data


if __name__ == '__main__':
    app.run()
