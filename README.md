# CIS 427 PROJECT 2

CODED BY:
    Hadi Zalzali
        - Database operations such as LIST, BALANCE, BUY, and SELL
    Jaxon Pecora
        - User / Client Socket, Exception handling
    Matthew Alexander
        - User / Client Socket, QUIT and SHUTDOWN, and Command Switchboard
TECHNOLOGIES USED:
    Python 3
    sqlite

VIDEO DEMONSTRATION: https://www.youtube.com/watch?v=4F4xj15sJhE
GITHUB: https://github.com/MatsoA/CIS-427-Project-1

*Program must be run in a LINUX enviornment*

## To run:
Download both python scripts to the same folder:
    server.py
    client.py

Navigate to that folder in a terminal and run `python server.py`

While leaving that terminal running, open a new terminal window and navigate to the folder and run `python client.py ip`
Note: to find the ip of an ubuntu machine, type `hostname -I` in the ubuntu terminal(use this for the ip argument).  

You should now be able to input commands to the server:

LOGIN USERNAME PASSWORD           - Logs in user into client. Must be done before other commands can be ran

LOGOUT                            - Logs out user from client

LIST                              - prints list of stocks logged in user has

BALANCE                           - prints details of the current user logged in

BUY SYMBOL COUNT PRICE ID         - User ID buys COUNT number of SYMBOL stock for PRICE
                                  - COUNT, PRICE, AND ID MUST BE INTEGERS  

SELL SYMBOL COUNT PRICE ID        - User ID sells COUNT number of SYMBOL stock for PRICE
                                  - COUNT, PRICE, AND ID MUST BE INTEGERS  

DEPOSIT AMOUNT                    - Adds AMOUNT Dollars to logged in user's balance

LOOKUP SYMBOL                     - Returns details for specific stock logged in user has

QUIT                              - closes client's connection to server


**Must be logged in as root user:**

WHO                               - List of clients currently logged into server

SHUTDOWN                          - closes server

 

## Test Cases and Screenshots
Test case table: https://docs.google.com/spreadsheets/d/1zphCUK0-7hR-K2ytNo2Xd8XJjP4WLqQRvfzh2x21w50/edit?usp=sharing

Screenshots: https://docs.google.com/document/d/1dc-WxsSsrVSedc-YseZptLUXn6mqzGM4EqP5L2DXxBE/edit?usp=sharing

