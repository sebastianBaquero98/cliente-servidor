import socket
import os
import sys  
import hashlib
import time
from tqdm import tqdm
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
        self.HELLO = "HELLO"
        self.CONFIRM = "CONFIRM"
        self.GOODBYE = "GOODBYE"
        self.logger = logger("client")
        self.logger.log_info('[STARTING] Logs initialized for client')
        self.route=""


    def __call__(self):
        self.connect()
        self.client.sendall(self.HELLO.encode())
        fail=False
        with self.client,self.client.makefile('rb') as serverFile:
            fileSize = float(serverFile.readline().strip().decode())*self.HEADER
            fileExtension = serverFile.readline().strip().decode()
            self.logger.log_info(f'[MESSAGE] File size arrived {fileSize}')
            hashFile = serverFile.readline().strip().decode()
            self.logger.log_info(f'[MESSAGE] Hash digest arrived')
            self.logger.log_info(f'[MESSAGE] File transfer will begin')
            currentFileTransfer = fileSize
            length=0
            self.route = f'./recivedFiles/{self.name}-Prueba{self.prueba}.{fileExtension}'
            with open(self.route,'wb') as f:
                progress = 0
                length = fileSize
                pbar = tqdm(total=100,initial=progress)
                packet = min(fileSize,self.HEADER)
                data = serverFile.read(int(packet))
                while length>0:
                    length-=len(data)
                    progress = round((fileSize-length)/fileSize*100,0)
                    f.write(data)
                    pbar.update(progress)
                    if length>0:
                        packet = min(length,self.HEADER)
                        data += serverFile.read(int(packet)).strip()
                
            pbar.close()
            if length==0:
                self.logger.log_info(f'[MESSAGE] File transfer complete. Checking integrity')
                localHash = self.getHashFile()
                if localHash==hashFile:                  
                    self.logger.log_critical(f'[MESSAGE] File transfer complete. Integrity correct')
                    end_time = time.time()
                    self.client.sendall(self.CONFIRM.encode(),)
                    init_time = float(self.client.recv(self.HEADER).decode())
                    self.client.sendall(str(end_time).encode())
                else:
                    self.logger.log_critical(f'[MESSAGE] File transfer complete. Integrity fail')
                    fail=True
            else:
                self.logger.log_critical(f'[MESSAGE] File transfer complete. Incorrect file')
                fail=True
        if fail:
            os.remove(self.route)
            sys.exit(1)
            


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
    

    def getHashFile(self):
        h = hashlib.sha1()
        with open(self.route,'rb') as file:
            chunk = 0
            while chunk != b'':
                chunk = file.read(1024)
                h.update(chunk)
        return h.hexdigest()

            
if __name__ == '__main__':
    id = int(sys.argv[1])
    direccion = socket.gethostbyname(socket.gethostname())
    puerto =5050

    nuevoCliente = client(id,1,direccion,puerto)
    nuevoCliente()