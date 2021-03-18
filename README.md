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
- lfs
---
## How to install dependencies:
- Run 
  ```
  pip install requirements.txt
  ```
- Run
  ```
  git lfs install
  ```
---
## How to Run:
1. Locate yourself at root folder
2. Run the following command
   ```
   TCPenv\Scripts\activate
   ```
3. Start server with the following command. 
    - The first parameter is the # of minimum clients to start the file transfer. 
    - The second paramenter is the file to be sended:
        - 1 = 100MB
        - 2 = 250MB
        - 3 = SmallTestFile
   ```
   python src/server.py [numberOfMinimumClients] [File]
   ```
4. Start the needed clients in another command window (Need to repeat step 1 and 2)
   ```
   python src/client.py [id]
   ```