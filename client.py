#!/usr/bin/python3
import socket
import pickle
import os

""" ----- CONSTANTES ----- """
SEPARATOR = "<SEPARATOR>"

""" ----- VARIABLES ----- """
host = '192.168.1.114'
puerto = 65534
tamañoArchivo  = 0
nombreArchivo = ''
bufferSize = 4096

# Se crea un objeto socket s con dos parametros 
# 1. socket.AF_INET que significa que es IPv4 
# 2. socket.SOCK_STREAM que significa que sera sobre el protocolo TCP 
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# Defina a que puerto y a que maquina se conectara
s.connect((host,puerto))
# Recibe el mensaje, el parametro define el tamaño de los chunks que recibira, es decir cuanto recibira al mismo tiempo
archivoRecibido = s.recv(bufferSize).decode()
nombreArchivo, tamañoArchivo = archivoRecibido.split(SEPARATOR) 
nombreArchivo = os.path.basename(nombreArchivo)
tamañoArchivo = int(tamañoArchivo)
with open(nombreArchivo,'wb') as f:
    while True:
        linea = s.recv(bufferSize)
        if not linea:
            break
        f.write(linea)

s.close() 
    







   