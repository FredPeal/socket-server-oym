import requests
import sys
import socket
import errno
import select

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


def sendToServer(username, point):
    HEADER_LENGTH = 10
    IP = "127.0.0.1"
    PORT = 1234
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))
    client_socket.setblocking(False)
    message = "Hola Mundo"
    if message:
        message = message.encode("utf-8")
        message_header = f"{len(message) :< {HEADER_LENGTH}}".encode("utf-8")
        client_socket.send(message_header + message)
