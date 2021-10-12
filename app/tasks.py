from celery import Celery
from collections import Counter
import os
import pandas as pd

app = Celery('tasks', backend='rpc://', broker='amqp://guest:guest@rabbitmq:5672/')


def count_occurrences(text, words):
    occurrences = Counter(text.lower().split())
    return Counter({word: occurrences[word] for word in words})


def count_pronouns_in_file(filename):
    pronouns = ['han', 'hon', 'den', 'det', 'denna', 'denne', 'hen']

    data = pd.read_json(filename, lines=True)[['text', 'retweeted_status']]
    original_tweets = data.loc[data['retweeted_status'].isnull()]['text']
    all_tweets_texts = ' '.join(original_tweets)

    return count_occurrences(all_tweets_texts, pronouns)


@app.task
def pronouns_task():
    data_files = os.listdir('data')
    count = {
        'status': 'OK',
        'status_message': 'Data received.',
        'pronouns': Counter(),
        'total_pronouns': 0
    }

    for filename in data_files:
        count['pronouns'] += count_pronouns_in_file(f'data/{filename}')

    count['total_pronouns'] = sum(count['pronouns'].values())
    return count
