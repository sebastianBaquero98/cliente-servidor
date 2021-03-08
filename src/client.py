import socket
import os
import sys
from logger import logger


class client():

    def __init__(self, id: int, prueba: int, addr: str, port: int):
        """Función que crea un cliente
        Args:
            id (int): Id del cliente
            prueba (int): Numero de Prueba a practicar
            addr (str): Dirección IP del servidor
            port (int): Puerto del servidor
        """
        self.name = f"Cliente{id}"
        self.prueba = prueba
        self.HEADER = 1024
        self.ADDR = (addr, port)
        self.FORMAT = "latin-1"
        self.DISCONECT_STATUS = "DISCONNECT"
        self.READY_STATUS = "READY"
        self.STAND_BY_STATUS = "STAND BY"
        self.SEND = "SEND"
        self.logger = logger("client")
        self.logger.log_info('[STARTING] Logs initialized for client')
        self.status = "STAND BY"
        self.transferComplete = False

    def __call__(self):
        self.connect()
        while not self.transferComplete:
            self.listen()
            self.sendall()

            

    def connect(self):
        """Función para conectase al servidor
        """
        try:
            #Conexion al servidor
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(self.ADDR)
        except Exception as ex:
            self.logger.log_critical(ex)
            raise ex

    def listen(self):
        """Función de escucha del cliente
        """
        try:
            self.logger.log_info("[LISTENING] Listening for a message")

            #Se recibe un mensaje
            msg_lenght = self.client.recv(self.HEADER).decode(self.FORMAT)

            
            #Se verifica que no sea vacio
            if msg_lenght:
                
                #Se obtiene el contenido
                msg = msg_lenght

                #Si esta en standby
                if msg == self.STAND_BY_STATUS:
                    self.logger.log_info(f"[LISTENING] Listening for a message {self.STAND_BY_STATUS}")
                    self.status=self.STAND_BY_STATUS

                #Si esta en ready
                elif msg == self.READY_STATUS and self.status==self.STAND_BY_STATUS:
                    self.logger.log_info(f"[LISTENING] Listening for a message {self.READY_STATUS}")
                    self.status=self.READY_STATUS

                #Si ya estaba en ready (Va a reibir el file)
                elif self.status==self.READY_STATUS:

                    self.logger.log_info(f"[LISTENING] Listening for file")

                    #Se crea el arhivo
                    #Open in write binary
                   
                    data = self.client.recv(self.HEADER).decode(self.FORMAT)    #No esta escuchando esto, pero el server si lo envia
                    with open(f"./recivedFiles/{self.name}-Prueba{self.prueba}.txt",'wb') as f:
                        while data:
                            f.write(data)
                            data = self.client.recv(self.HEADER).decode(self.FORMAT)

                    f.close()
                    self.transferComplete=True
                    self.client.close()

        except Exception as ex:
            self.logger.log_critical(ex)
            raise ex
        
    def sendall(self):

        try:
            self.logger.log_info("[MESSAGE] Sending a message")
            """Función para enviar un mensaje al servidor segun el estado del cliente
            """
            if self.transferComplete:
                self.client.sendall(bytes(self.DISCONECT_MSG,self.FORMAT))
                self.logger.log_info(f"[MESSAGE] Sending a message {self.DISCONECT_MSG}")
    
            elif self.status==self.STAND_BY_STATUS:
                self.client.sendall(bytes(self.STAND_BY_STATUS,self.FORMAT))
                self.logger.log_info(f"[MESSAGE] Sending a message {self.STAND_BY_STATUS}")
    
            elif self.status==self.READY_STATUS:
                self.client.sendall(bytes(self.READY_STATUS,self.FORMAT))
                self.logger.log_info(f"[MESSAGE] Sending a message {self.READY_STATUS}")
        
        except Exception as ex:
            self.logger.log_critical(ex)
            raise ex
            
if __name__ == '__main__':
    id = int(sys.argv[1])
    direccion = socket.gethostbyname(socket.gethostname())
    puerto =5050

    nuevoCliente = client(id,1,direccion,puerto)
    nuevoCliente()