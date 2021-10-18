import matplotlib.pyplot as plt
import json

request_text = open('response.txt', 'r').read()
frequencies = json.loads(request_text)

hist = frequencies['pronouns']
hist.update({n: hist[n]/frequencies['total_tweets'] for n in hist.keys()})

plt.bar(list(frequencies['pronouns'].keys()), hist.values())
plt.ylabel('Frequency')
plt.savefig('output/histogram.png', bbox_inches='tight')
plt.show()
