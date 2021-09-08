import cv2
import socket

def socket():
    import socket

    #Iniciaizamos el socket y le pasamos los parametros
    #AF_INET = Ip, Sock_STREAM =  TCP.
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Le decimos al socket que ip debe de escuchar y que puerto
    server.bind(('localhost', 8050))
    #Le decimos que va a tener que escuchar
    server.listen()

    #Instanciamos un objeto socket cliente para recibir datos
    client_socket, client_address= server.accept()

    file = open('server_image.png', "wb")
    image_chunk = client_socket.recv(2048) #stream base protocol, solo podemos recibir pocos datos


    while image_chunk:
        file.write(image_chunk)
        image_chunk = client_socket.recv(2048)


    file.close()
    client_socket.close()



def desencriptar():
    
    try:
        # tomamos el path de la imagen a desencriptar
        path = "I:/UAQ/Quinto/SD/Proyecto/github/Client-Server-Encrypt-Image/server_image.png"
        
        # pedimos el valor de la llave
        key =input('Ingresa el valor de la llave para encriptar : ')
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
    


"""
Tienen que crear una funcion que reenvie la imagen ya desencriptada al cliente para que este pueda verificar si son
correctas
"""

    
socket()
desencriptar()

