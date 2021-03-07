#!/usr/bin/python3
import socket
import pickle
import os
from threading import Thread
""" ----- CONSTANTES ----- """

HEADERSIZE = 10
""" ----- VARIABLES ----- """
host = '192.168.1.114'
puerto = 65534
fileSize = 0
nombreArchivo = ""



es1 = False
numeroDeConexiones = 0
def nuevaConexCliente(sCliente, IPCliente, nombreA, tamañoA):
    SEPARATOR = "<SEPARATOR>"
    bufferSize = 4096
    print("----- El servidor TCP se conecto satisfactoriamente a "+ str(direcciónIPCliente)+" -----")
    # Se envia el nombre del archivo y el tamaño al cliente
    
    sCliente.send(f"{nombreA}{SEPARATOR}{tamañoA}".encode())
    with open(nombreA,'rb') as archivo:
        while True:
            linea = archivo.read(bufferSize)
            print(linea)
            if not linea:
                print("No linea")
                #No hay mas que transmitir
                break
            sCliente.sendall(linea)
    sCliente.close()

# Se crea un objeto socket s con dos parametros 
# 1. socket.AF_INET que significa que es IPv4 
# 2. socket.SOCK_STREAM que significa que sera sobre el protocolo TCP 
print("----- Que Archivo deseas enviar (100 o 200) -----")
respuesta = int(input())
print("----- ¿A cuantos servidores cliente les quiere mandar el archivo "+str(respuesta)+"? -----")
numeroClientes = int(input())
if respuesta == 100:
    nombreArchivo = "t1pickle.txt"
    fileSize = os.path.getsize(nombreArchivo)
    es1 = True
else:
    nombreArchivo = "t2pickle.txt"
    fileSize = os.path.getsize(nombreArchivo)
    es1=False



s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# Se le asigna una dirección IP y un puerto de transmisión 
s.bind((host,puerto))
# Pone a escuchar al socket, el parametro define el tamaño del buffer """
s.listen(numeroClientes)

#Se aceptan conexiones hasta que la cantidad de conexiones se sastisfaga
while numeroDeConexiones < numeroClientes:
    # Se guarda objeto del socket del cliente y la dirección ip del cliente
    socketCliente, direcciónIPCliente = s.accept()
    # Se crea un thread para cada conexion
    Thread(target=nuevaConexCliente,args=(socketCliente,direcciónIPCliente,nombreArchivo,fileSize)).start()
    numeroDeConexiones = numeroDeConexiones + 1
    

    

