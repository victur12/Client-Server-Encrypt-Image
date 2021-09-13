import cv2
import socket
import os
from random import choice


def encriptar(path_Destino, extension):
    #Asignamos los valores de la llave
    
   
    try:
            # le mandamos el path de la imagen que queremos encriptar
        path = path_Destino + "/encriptado" + extension
            
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
  
def copiar(path_Inicio, path_Destino, extension):
    
    #vamos a copiar la imagen para así en un futuro comparar la imagen original y la desencriptada
    #primero inicio abriendo la imagen con opencv
    imagen = cv2.imread(path_Inicio)
    #y despues solo copio la imagen original
    path_nuevo = path_Destino + "/encriptado" +extension
    cv2.imwrite(path_nuevo, imagen)
    
def comparar_img(path_Inicio,path_Destino, extension):

    #para comparar las imagenes necesitamos abrir las 2
    """
    Aqui uds tiene que ver lo de las rutas y cambiarlo para no tener problemas con rutas diferentes para
    para el ejemplo solo puse mis rutas
    """
    original= cv2.imread(path_Inicio)
    desencriptada = cv2.imread(path_Destino + '/desencriptado'+ extension)

    #Aqui solo estoy sacando el tamaño de las imagenes para despues comparar y ver si son iguales
    originalImg = original.shape
    desencriptadaImg = desencriptada.shape

    #Una vez entrado al if lo que hago es sacar un substrac,
    #esto lo que hace es que si hay una diferencia en las imagenes los marca
    #esto devuelve una imagen negra si son iguales y si hay diferencias solo marca las diferencias con otro color
    if originalImg == desencriptadaImg:
        print ("las imagenes tiene el mismo tamaño")
        diferencia = cv2.subtract(original,desencriptada)
    
        #una ves teniendo el subtrac lo que hago es dividirlo por codigo de color para verificar que esten bien
        b, g, r = cv2.split(diferencia)

        #lo que hago en este if es ocupar una funcion que valida que haya 0 cambios de negro para así estar seguro que son iguale
        if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) ==0 and cv2.countNonZero(r)==0:
            print("las imagenes son las mimsmas")
        else:
            print("las imagenes no son iguales")

def recibir(path_Destino, extension):
    import socket

   
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server.bind(('localhost', 9000))
   
    server.listen()

   
    client_socket, client_address= server.accept()

    file = open(path_Destino+'/desencriptado' + extension, "wb")
    image_chunk = client_socket.recv(2048)

    print('123')
    while image_chunk:
        file.write(image_chunk)
        image_chunk = client_socket.recv(2048)


    file.close()
    client_socket.close()

def main():
    
    longitud = 18

    valores = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ<=>@#%&+"

    key = ""
    key = key.join([choice(valores) for i in range(longitud)])
    print('Esta es la llave que van a ocupar \n'+ key)

    print ("Inciando procesos")

    path_Inicio = input('Meta la ruta de la imagen ')
    path_Destino = input('Meta la ruta donde quiera que se guarde ' )

    root, extension =os.path.splitext(path_Inicio)


    copiar(path_Inicio, path_Destino, extension)
    encriptar(path_Destino, extension)

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(('localhost', 8050))

    file = open(path_Destino +'/encriptado' + extension, 'rb')

    cliente.send(extension.encode('ascii'))

    cliente.send(key.encode('ascii'))
    
    image_data  = file.read(2048)

    while image_data:
        cliente.send(image_data)
        image_data  = file.read(2048)
   
    file.close()
    cliente.close()


    recibir(path_Destino, extension)

    comparar_img(path_Inicio, path_Destino, extension)

main()

# I:/UAQ/Quinto/SD/Proyecto/github/Client-Server-Encrypt-Image/Servidor