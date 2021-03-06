import socket
import select
import errno
import sys 
import requests
import functionsx

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

print("Hola \nBienvenido a Quiz O&M este juego trata de ver quien responde mas preguntas de manera correcta en un tiempo de 3 minutos \nDesas inicar ? \n1. Si \n2. No")
start_game = input();

if start_game == "0":
    print("Bueno, hasta luego, cuando estes listo puedes regresar")
    sys.exit()

print("Muy bien, primero dinos cual es tu nombre")

my_username = input("Nombre: ")
print(f"Muy bien {my_username}, iniciemos")
point = 0

questions = functionsx.question()
for question in questions:
    print(functionsx.make_unicode(question['question']))
    numberResponse = 1
    answer = input("1.True\n2.False\n")        
    if question['correct_answer'] == "True" and answer == "1":
        point = point+5
        print("Respuesta correcta")
    elif question['correct_answer'] == "False" and answer == "2":
        point = point+5
        print("Respuesta correcta")
    else:
        print(f"Respuesta incorrecta, debiste escoger {functionsx.make_unicode(question['correct_answer'])}")

print(f"Puntaje Total {point}")

sys.exit()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))

client_socket.setblocking(False)

username = my_username.encode("utf-8")
username_header = f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")

client_socket.send(username_header + username)

while True:
    message = input(f"{my_username} > ")
    if message:
        message = message.encode("utf-8")
        message_header = f"{len(message) :< {HEADER_LENGTH}}".encode("utf-8")
        client_socket.send(message_header + message)
    
    try:
        while True:
            # receive things
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print("connection closed by the server")
                sys.exit()
            username_length = int(username_header.decode("utf-8").strip())
            username = client_socket.recv(username_length).decode("utf-8")

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode("utf-8").strip())
            message = client_socket.recv(message_length).decode("utf-8")

            print(f"{username} > {message}")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error', str(e))
            sys.exit()
        continue

    except Exception as e:
        print('General error', str(e)) 
        sys.exit()
