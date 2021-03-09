import socket
import threading
import threading
import sys
import os
import hashlib
from logger import logger


class server():
    """Clase servidor TCP
    """

    def __init__(self, min_env: int, file: int):
        """Función para crear un servidor
        Args:
            min_env (int): Minimo numero de conexiones para enviar el archivo
            file (int): Archivo a seleccionar:
                        1. Arhcivo 100MB
                        2. Archivo 200MB
        """

        # Server asserts
        assert 1 <= min_con <= 25, "El numero maximo de conexiones son 25"
        assert 1 <= file <= 3, "El archivo no es el indicado"

        # Server class constant
        self.HEADER = 1024
        self.PORT = 5050
        self.ADDR = (socket.gethostbyname(socket.gethostname()), self.PORT)
        self.FORMAT = "latin-1"
        self.DISCONECT_MSG = "DISCONNECT"
        self.READY_MSG = "READY"
        self.STAND_BY_MSG = "STAND BY"
        self.SEND = "SEND"
        self.MIN_CON = min_con
        self.PATHS = ["./testFiles/100MBFile.txt","./testFiles/250MBFile.txt","./testFiles/SmallTestFile.txt"]
        self.HASH = hashlib.md5()

        # Logger setup
        self.logger = logger('server')
        self.logger.log_info('[STARTING] Logs initialized')

        # Server connect
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        self.logger.log_info("[STARTING] Server is starting...")
        self.connected=True

        # Listado de clientes
        self.clients = []
        self.fileIndex = file-1

        # Selección de archivo a enviar
        self.file = open(self.PATHS[self.fileIndex], "rb")



    def handle_client(self, conn:socket, addr:tuple):
        """Función que maneja las nuevas conexiones con el cliente

        Args:
            conn ([type]): Conexión del cliente
            addr (str): Dirección del cliente
        """
        try:
            # Logea la nueva conexión
            self.logger.log_info(f"[NEW CONNECTION] {addr} connected")
            self.connected = True
            while self.connected:
                self.sendall(conn,addr)
                self.connected = self.listen(conn,addr)
                


        # Si ocurre un error critico que acabe els erver
        except Exception as ex:
            pass
            self.logger.log_critical(ex)
            raise ex

    def start(self):
        try:
            """Función que inicaliza el servidor
            """
            # Se logea que el servidor comienza a escuchar por ADDR[0]
            self.logger.log_info("[STARTING] Server is listening...")
            self.server.listen()
            self.logger.log_info(
                f"[LISTENING] Server is listening on {self.ADDR[0]}")

            # Siempre y cuando se este escuchando
            while self.connected:

                # Acepta la conexión
                conn, addr = self.server.accept()
                self.logger.log_info(f"[CONNECTED] Connection stablished with {addr}")
                self.clients.append((conn,addr))
                # Se crea un thread para manejar los clientes
                thread = threading.Thread(
                    target=self.handle_client, args=(conn, addr))
                thread.start()

                # Se logea la nueva conexión
                self.logger.log_info(msg = f"[ACTIVE CONNECTIONS] {len(self.clients)}" )
            self.logger.log_critical("[SHUTDOWN] Server is on shutdown")
        except Exception as ex:
            self.logger.log_critical(ex)
            raise ex


    def sendall(self,conn:socket,addr:tuple):
        """Función para mandar un mensaje a los clientes
        """
        self.logger.log_info(f"[MESSAGE] Server is trying to send message to {addr}")
        # Si se tiene menos de las conexiones requeridas
        if len(self.clients) < self.MIN_CON:   
        # Se manda un mensaje al cliente de que permanesca en stand by
            conn.sendall(bytes(self.STAND_BY_MSG,self.FORMAT))
            self.logger.log_info(
                f"[MESSAGE] Please client {addr} Stand by for minimun required clients")

                # Esta listo para enviar
        else:
            # Se cambian las conexiones activas a listo
            conn.sendall(bytes(self.READY_MSG,self.FORMAT))
            self.logger.log_info(f"[MESSAGE] Client {addr} change state to ready")
                    
                

    def listen(self,conn:socket,addr:tuple):
        self.logger.log_info(f"[LISTENING] Server is trying to retrive message from {addr}")
        try:
            self.connected = True
            # Obtinene el header del mensaje. Si el cliente envia un mensaje
            msg_lenght = conn.recv(self.HEADER).decode(self.FORMAT)
            # Si existe el mensaje (Si se envio)
            if msg_lenght:
                 # Mensaje
                msg = msg_lenght

                # Si es de deconexción
                if msg == self.DISCONECT_MSG:
                    connected = False  # Cambia el estado
                    # Se remueve la conexión del listado de conexiones
                    self.clients.remove((conn,addr))
                    self.logger.log_info(
                        f"[{self.DISCONECT_MSG}] Client with address {addr} disconnected")  # Se logea la info
                    conn.close()
                    self.connected=False
                    self.clients.remove((conn,addr))

                elif msg == self.STAND_BY_MSG:
                    self.logger.log_info(
                    f"[{self.STAND_BY_MSG}] Client with address {addr} is on stand by")  # Se logea la info

                elif msg == self.READY_MSG:
                    self.logger.log_info(
                                f"[{self.READY_MSG}] Client with address {addr} is ready")  # Se logea la info

                    filename = os.path.basename(self.PATHS[self.fileIndex])
                    filesize = os.path.getsize(self.PATHS[self.fileIndex])
                    self.logger.log_info(f"[MESSAGE] Client {addr} will recive file {file_name} with size {filesize}")
                    #self.logger.log_info(f"[MESSAGE] Client {client[1]} will recive hash of file")

                    data = self.file.read(self.HEADER)

                    """ ANTES DE ENVIAR EL TEXTO
                        ES NECESARIO PRIMERO CONFIRMAR QUE EL CLIENTE ESTE LISTO
                        SE TIENE QUE ENVIAR UN MENSAJE DESDE EL CLIENTE
                        INDICANDO QUE LA TRANSFERENCIA PUEDE COMENZAR
                        Y DESPUES PONER EL CLIENTE A ESCUCHAR
                        Y EL SERVIDOR A ENVIAR
                    """

                    while data:
                        print(data)
                        conn.sendall(data)
                        data = self.file.read(self.HEADER)

                    self.file.close()
                    # Se acaba la conexion
                    self.logger.log_info(f"[MESSAGE] Client {addr} will recived file {file_name} with size {filesize}")

                    

        except Exception as ex:
            self.logger.log_critical(ex)
            raise ex
        


if __name__ == '__main__':
    min_con,file_name = int(sys.argv[1]),int(sys.argv[2])
    serverTCP = server(min_con,file_name)
    serverTCP.start()
