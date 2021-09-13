import socket
import cv2
 
def encriptar():
    #Asignamos los valores de la llave
    
    key = "123"
    
   
    try:
            # le mandamos el path de la imagen que queremos encriptar
        path = "I:/UAQ/Quinto/SD/Proyecto/github/Client-Server-Encrypt-Image/encriptado.png"
            
            # pedimos la llave para poder encriptar
        key =input('Ingresa el valor de la llave para encriptar : ')
        key = bytes(key, 'ascii')
        


        # imprimimos la direccion de la imagen y la llave 
        print('El path de la imagen es: ', path)
        print('la llave es: ', key)

        # Abrimos el archivo solo para leerlo
        fin = open(path, 'rb')

        # guardamos los datos de la imagen en imagen
        imagen = fin.read()
        fin.close()

        # convertimos la imagen en un array de bytes
        # para realizar mas facilmente el cifrado
        imagen = bytearray(imagen)

        # realizamos la operacion XOR en cada valor del array
        for index, values in enumerate(imagen):
            for byte in key:
                imagen[index] = imagen[index] ^ byte

        # abrimos el archivo con el proposito de escribir
        fin = open(path, 'wb')

        # escribimos la imagen encriptada
        fin.write(imagen)
        fin.close()
        print('encriptacion hecha...')

    except Exception :
        print('Error', Exception.__name__)
  
def copiar():
    
    
    #vamos a copiar la imagen para así en un futuro comparar la imagen original y la desencriptada
    #primero inicio abriendo la imagen con opencv
    imagen = cv2.imread('diagrama.png')
    #y despues solo copio la imagen original
    cv2.imwrite("encriptado.png", imagen)
    
ClientSocket = socket.socket()
host = '127.0.0.1'
port = 8050

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

copiar()
encriptar()

image_chunk = ClientSocket.recv(2048)

while True:
    # Input = input('Say Something: ')
    file = open('I:/UAQ/Quinto/SD/Proyecto/github/Client-Server-Encrypt-Image/encriptado.png', 'rb')

    image_data = file.read(2048)

    while image_data:
        ClientSocket.send(image_data)
        image_data =file.read(2048)

    file.close()

    file = open('desencriptada.png', "wb")

    image_chunk = ClientSocket.recv(2048)

    while image_chunk:
        file.write(image_chunk)
        image_chunk = ClientSocket.recv(2048)
    file.close()

    # print(Response.decode('utf-8'))

ClientSocket.close()