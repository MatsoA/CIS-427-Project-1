CIS 427 PROJECT 1

CODED BY:
    Hadi Zalzali
    Jaxon Pecora
    Matthew Alexander

TECHNOLOGIES USED:
    Python 3
    sqlite

To run:
Download both python scripts to the same folder:
    server.py
    client.py

Navigate to that folder in a terminal and run `python server.py`

While leaving that terminal running, open a new terminal window and navigate to the folder and run `python client.py` 

You should now be able to input commands to the server:

LIST                              - prints details of users currently stored in database

BALANCE                           - prints details of the current user tied to client

BUY SYMBOL COUNT PRICE ID         - User ID buys COUNT number of SYMBOL stock for PRICE
                                  - COUNT, PRICE, AND ID MUST BE INTEGERS  

SELL SYMBOL COUNT PRICE ID        - User ID sells COUNT number of SYMBOL stock for PRICE
                                  - COUNT, PRICE, AND ID MUST BE INTEGERS  

QUIT                              - closes client's connection to server

SHUTDOWN                          - closes server

 