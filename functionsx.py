import requests
import sys

if sys.version_info[0] >= 3:
    unicode = str

def make_unicode(input):
    if type(input) != unicode:
        input =  input.decode('utf-8')
    return input
    
def question():
    url = "https://opentdb.com/api.php"
    params = {'amount': 50, 'category': 9, 'type':'boolean'}
    r = requests.get(url = url, params=params)
    data = r.json()
    questions = data['results']
    return questions