import socket
import os
import cv2
from _thread import *

Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 8050
ThreadCount = 0
try:
    Server.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
Server.listen()

def recibir(connection):
    file = open('server_image.png', "wb")
    data = connection.recv(2048)
    while data:
        file.write(data)
        data = connection.recv(2048)
    
    file.close()

    connection.close()

def desencriptar():
    
    try:
        # tomamos el path de la imagen a desencriptar
        path = "I:/UAQ/Quinto/SD/Proyecto/github/Client-Server-Encrypt-Image/server_image.png"
        
        # pedimos el valor de la llave
        key ="123"
        key = bytes(key, 'ascii')
        # Imprimo los valores que estamos ocupando para verificar que este bien
        print('la direccion de la imagen es: ', path)
        print('Como es encriptacion simetrica la key debe de ser la misma')
        print('la llave de encriptacion es : ', key)
        
        # abrimos el archivo solo para leer
        fin = open(path, 'rb')
        
        # guardamos la imagen en la variable imagen
        imagen = fin.read()
        fin.close()
        
        #  convertimos la imagen en un array de bytes
        imagen = bytearray(imagen)

        # abrimos el archivo con el proposito de escribir
        for index, values in enumerate(imagen):
            for byte in key:
                imagen[index] = imagen[index] ^ byte

        # opening file for writing purpose
        fin = open(path, 'wb')
        
        # escribimos la imagen encriptada
        fin.write(imagen)
        fin.close()
        print('desencriptacion hecha...')

    except Exception:
        print('Error: ', Exception.__name__)
    
def enviar():

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(('localhost', 9000))

    file = open('server_image.png', 'rb')

    image_data  = file.read(2048)

    while image_data:
        cliente.send(image_data)
        image_data  = file.read(2048)
    

    file.close()
    cliente.close()

def threaded_client(connection):
    
    file = open('server_image.png', "wb")
    data = connection.recv(2048)
    while data:
        file.write(data)
        data = connection.recv(2048)

    file.close()

    connection.close()
    desencriptar()

    if  not data:
        print("no hay datos")
    
        print('-----------------Aqui se envia la imagen----------------')
        enviar()

        # file = open('server_image.png', 'rb')

        # image_data = file.read(2048)

        # while image_data:
        #     connection.send(image_data)
        #     image_data = file.read(2048)
        
        # file.close()

   

while True:
    Client, address = Server.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
Server.close()
print('Funciona')