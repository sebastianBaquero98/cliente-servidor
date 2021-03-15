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
        self.HEADER = 2**20
        self.ADDR = (addr, port)
        self.FORMAT = "latin-1"
        self.HELLO = "HELLO"
        self.CONFIRM = "CONFIRM"
        self.GOODBYE = "GOODBYE"
        self.logger = logger("client")
        self.logger.log_info('[STARTING] Logs initialized for client')


    def __call__(self):
        self.connect()
        msg=[]
            
        """Recibir hash
         """
        self.client.sendall(bytes(self.HELLO,self.FORMAT))  #Manda mensaje de Hello
        msg.append(self.client.recv(self.HEADER).decode(self.FORMAT).replace("\r",""))
        self.client.sendall(bytes(self.CONFIRM,self.FORMAT))

        """Verificar integridad con el hash
        """            
        with open(f'./recivedFiles/{self.name}-Prueba{self.prueba}.txt','w') as f:
            print(msg)
            f.writelines(msg)
        
        self.client.sendall(bytes(self.GOODBYE,self.FORMAT))



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
            
if __name__ == '__main__':
    id = int(sys.argv[1])
    direccion = socket.gethostbyname(socket.gethostname())
    puerto =5050

    nuevoCliente = client(id,1,direccion,puerto)
    nuevoCliente()