import celery.exceptions
from flask import Flask

import tasks

app = Flask(__name__)


@app.route('/pronouns/api/count', methods=['GET'])
def pronouns():
    data = tasks.add.delay(1, 3)
    try:
        result = data.get(timeout=5)
    except celery.exceptions.TimeoutError:
        return ''

    return str(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
