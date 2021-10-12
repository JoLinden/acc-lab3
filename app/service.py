import celery.exceptions
from flask import Flask

import app.tasks as tasks

app = Flask(__name__)


@app.route('/pronouns/api/static', methods=['GET'])
def static_endpoint():
    return "Hello"


@app.route('/pronouns/api/count', methods=['GET'])
def count_endpoint():
    print("Count endpoint")
    data = tasks.add.delay(1, 3)
    print('Task started')
    try:
        result = data.get(timeout=5)
        print('Result received')
    except celery.exceptions.TimeoutError:
        print('Task error')
        return 'Celery could not be reached.'

    print('Returning result')
    return str(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
