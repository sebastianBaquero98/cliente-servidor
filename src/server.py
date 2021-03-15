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
        self.HEADER = 2**20
        self.PORT = 5050
        self.ADDR = (socket.gethostbyname(socket.gethostname()), self.PORT)
        self.FORMAT = "latin-1"
        self.HELLO = "HELLO"
        self.CONFIRM = "CONFIRM"
        self.GOODBYE = "GOODBYE"
        self.MIN_CON = min_con
        self.PATHS = ["./testFiles/100MBFile.txt","./testFiles/250MBFile.txt","./testFiles/SmallTestFile.txt"]
        self.HASH = hashlib.md5()
        self.SEMAPHORE = threading.Semaphore()
        self.EVENT = threading.Event()
        
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
            self.listen(conn,addr)
            self.sendall(conn,addr)
            conn.close()
        except Exception as ex:
            self.logger.log_critical(ex)
            raise ex
            sys.exit(1)


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
            self.logger.log_critical("[SHUTDOWN] Server is on shutdown")
        except Exception as ex:
            self.logger.log_critical(ex)
            raise ex
            sys.exit(1)


    def sendall(self,conn:socket,addr:tuple)->bool:
        """Función que hace el envio de mensajes

        Args:
            conn (socket): [description]
            addr (tuple): [description]
        """
        self.logger.log_info(f"[MESSAGE] Server is trying to send message to {addr}")
        
            
        with self.file as f: #Con conn y el file
            data = f.read(self.HEADER) #Se lee el primer pedazo
            packetNumber = 1
            while data: #Siempre que la variablee no sea nula
                try:
                    self.logger.log_info(f"[MESSAGE] Packet {packetNumber} is being send {addr}")
                    conn.sendall(data)  #Se envia  
                    msgRecv = conn.recv(self.HEADER).decode(self.FORMAT)
                    if msgRecv and msgRecv==self.CONFIRM:  #Si confirma el mensaje, se cambia
                        self.logger.log_info(f"[MESSAGE] Packet {packetNumber} arrived to {addr}")
                        data = f.read(self.HEADER)
                        packetNumber+=1
                except Exception as ex:
                    self.logger.log_critical(ex)    #Se logea el timeout
                    raise ex

        msgRecv = conn.recv(self.HEADER).decode(self.FORMAT)
        if msgRecv and msgRecv==self.GOODBYE:
            self.logger.log_info(f"[MESSAGE] Client {addr} recived file. Close connection now")
            self.clients.remove((conn,addr))
            conn.close()
        
        if len(self.clients)==0:
            self.send=True

    def listen(self,conn:socket,addr:tuple):
        """Función que escucha los mensajes que envia el thread.
            Es el encargado de manejar la sincronización de los clientes

        Args:
            conn (socket): Socket de conexión
            addr (tuple): Dirección de conexión

        Returns:
            msg (str): Ultimo mensaje enviado por addr
        Raises:
            ex: Excepción que dañe todo
        """
        try:
            #Obtiene el mensaje
            self.logger.log_info(f"[MESSAGE] Listening for message of {addr}")
            msg = conn.recv(self.HEADER).decode(self.FORMAT)

            if msg:
                #Handshake inicial
                if msg == self.HELLO:
                    self.logger.log_info(f"[MESSAGE] Hello Message of {addr}")
                    self.synch()    #A mimir
        except Exception as ex:
            self.logger.log_critical(ex)
            raise ex
        

    def synch(self):
        """Metodo para sincronizar los clientes con un semaforo
        """
        with self.SEMAPHORE:
            self.logger.log_info(f"[CONNECTION] {len(self.clients)} Clients ready")
            if len(self.clients)==self.MIN_CON:
                self.EVENT.set()
            else: 
                self.EVENT.wait()

if __name__ == '__main__':
    min_con,file_name = int(sys.argv[1]),int(sys.argv[2])
    serverTCP = server(min_con,file_name)
    serverTCP.start()
