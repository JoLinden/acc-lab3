import celery.exceptions
from flask import Flask

import app.tasks as tasks

app = Flask(__name__)


@app.route('/pronouns/api/static', methods=['GET'])
def static_endpoint():
    return 'Service running.'


@app.route('/pronouns/api/count', methods=['GET'])
def count_endpoint():
    print("Count endpoint")
    data = tasks.pronouns_task.delay()
    print('Task started')
    try:
        result = data.get(timeout=600)
        print('Result received')
    except celery.exceptions.TimeoutError:
        print('Task error')
        return {
            'status': 'ERROR',
            'status_message': 'Celery could not be reached.',
            'pronouns': {},
            'total_pronouns': 0,
            'total_tweets': 0
        }

    print('Returning result')
    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
