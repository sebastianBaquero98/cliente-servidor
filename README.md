# TCP Server for file transfer
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)

---
## Authors:
- Martin Galvan
- Sebastian Baquero
- Juan Gonzalez
---

## Dependencies:
- tqdm = 4.59.0
---
## How to install dependencies:
- Run 
  ```
  pip install requirements.txt
  ```
- If it fails, run
  ```
  pip install tqdm
  ```
---
## How to Run Server on Windowns:
1. Locate yourself at root folder
2. For server files, download files from this links and put in testFile folder
   - [100MBFile.bin](https://www.dropbox.com/s/gqo5v7kblsop98s/100MBFile.bin)
   - [250MBFile.bin](https://www.dropbox.com/s/tbs0p9zpmyeuihd/250MBFile.bin)

3. Start server with the following command. 
    - The first parameter is the # of minimum clients to start the file transfer. 
    - The second paramenter is the file to be sended:
        - 1 = 100MB
        - 2 = 250MB
        - 3 = SmallTestFile
   ```
   python src/server.py [numberOfMinimumClients] [File]
   ```

## How to Rin Client on Windows
Start the needed clients in another command window from root folder
```
python src/client.py [id]
   ```
