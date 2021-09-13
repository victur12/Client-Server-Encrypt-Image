import cv2
import socket
import time
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
    
def comparar_img():

    #para comparar las imagenes necesitamos abrir las 2
    """
    Aqui uds tiene que ver lo de las rutas y cambiarlo para no tener problemas con rutas diferentes para
    para el ejemplo solo puse mis rutas
    """
    original= cv2.imread('I:/UAQ/Quinto/SD/Proyecto/diagrama.png')
    desencriptada = cv2.imread('I:/UAQ/Quinto/SD/Proyecto/server_image.png')

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

def recibir():
    import socket

    #Iniciaizamos el socket y le pasamos los parametros
    #AF_INET = Ip, Sock_STREAM =  TCP.
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Le decimos al socket que ip debe de escuchar y que puerto
    server.bind(('localhost', 9000))
    #Le decimos que va a tener que escuchar
    server.listen()

    #Instanciamos un objeto socket cliente para recibir datos
    client_socket, client_address= server.accept()

    file = open('desencriptado.png', "wb")
    image_chunk = client_socket.recv(2048) #stream base protocol, solo podemos recibir pocos datos

    print('123')
    while image_chunk:
        file.write(image_chunk)
        image_chunk = client_socket.recv(2048)


    file.close()
    client_socket.close()

def main():
    
    copiar()
    encriptar()

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(('localhost', 8050))

    file = open('I:/UAQ/Quinto/SD/Proyecto/github/Client-Server-Encrypt-Image/encriptado.png', 'rb')

    image_data  = file.read(2048)

    while image_data:
        cliente.send(image_data)
        image_data  = file.read(2048)
   
    file.close()
    cliente.close()


    print('-----------------Aqui se recibe la imagen----------------')

    recibir()



    # comparar_img()

main()