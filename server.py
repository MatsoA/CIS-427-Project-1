import socket
import sqlite3
import random
import threading
global message
global amount
global price
global user_id
global command
global isShutDown
isShutDown = False
port = 8232# Socket port number
message = "400 Invalid Message" # message sent to the client
response = "" # response from the client
command = "" # command from the client
amount = "" # amount of stocks from client arguments
price = "" # price of stocks from client arguments
user_id = "" # user ID from client arguments
mutex = threading.Lock()

two_hundred_ok = "200 OK \n"
# Precondtion: the user and stock tables are created. stock_symbol is a string. amount, price, and user_id are integers
# Postcondtion: the buy stock is serviced
def buy(stock_symbol, amount, price, user_id,conn):
    total = amount * price # amount of stocks * price of each stock
    message = "" # creating message variable
    # creating sub databases for error checking
    cursor = conn.execute("SELECT * FROM USERS WHERE ID = " + str(user_id))
    cursor2 = conn.execute("SELECT usd_balance FROM USERS WHERE ID = " + str(user_id))
    cursor3 = conn.execute("SELECT stock_balance FROM STOCKS WHERE ID = " + str(user_id) + " AND '" + str(stock_symbol) + "'")
    if (len(cursor.fetchall()) == 0): # user id has not enteries in USER table
        message = "403: User " + str(user_id) + " does not exist"
        return message
    balance = float(cursor2.fetchall()[0][0]) # balance for current user
    if(balance < total): # the total price exceeds the balance for the user
        message = "403: Insufficent Balance"
        return message
    else: # passed logical error checking
        cursor3 = conn.execute("SELECT * FROM STOCKS WHERE stock_symbol = '" + stock_symbol + str("'") + str(" AND user_id = ") + str(user_id))
        if(len(cursor3.fetchall()) == 0): # user DOES NOT own any stocks of type stock_symbol, creates a new entry
            conn.execute("INSERT INTO STOCKS (stock_symbol,stock_balance,user_id) VALUES ('" + str(stock_symbol) + "', " + str(amount) + ", " + str(user_id) + ")")
            conn.commit()
            conn.execute("UPDATE USERS SET usd_balance = (usd_balance - " + str(total) + ") WHERE ID = " + str(user_id))
            conn.commit()
            message = two_hundred_ok + "BOUGHT: New balance: " + str(amount) + " " + str(stock_symbol) + ". USD balance $" + str(balance - total)
            return message
        else: # user DOES own stocks of stock_symbol, update stock amount 
            conn.execute("UPDATE STOCKS SET stock_balance = (stock_balance + " + str(amount) + ") WHERE stock_symbol = '" + str(stock_symbol) + "' AND user_id = " + str(user_id))
            conn.commit()
            conn.execute("UPDATE USERS SET usd_balance = (usd_balance - " + str(total) + ") WHERE ID = " + str(user_id))
            conn.commit()
            cursor3 = conn.execute("SELECT stock_balance FROM STOCKS WHERE user_id = " + str(user_id) + " AND stock_symbol = '" + str(stock_symbol) + "'")
            conn.commit()
            message = two_hundred_ok + "BOUGHT: New balance: " + str(float(cursor3.fetchall()[0][0])) + " " + str(stock_symbol) + ". USD balance $" + str(balance - total)
            return message


# Precondtion: the user and stock tables are created. stock_symbol is a string. amount, price, and user_id are integers
# Postcondtion: the sell stock is serviced
def sell(stock_symbol, amount, price, user_id,conn):
    total = amount * price # amount of stocks * price of each stock
    message = "" # creating message variable
    # creating sub databases for error checking
    cursor = conn.execute("SELECT * FROM USERS WHERE ID = " + str(user_id))
    cursor2 = conn.execute("SELECT stock_balance FROM STOCKS WHERE user_id = " + str(user_id) + " AND stock_symbol = '" + str(stock_symbol) + "'")
    cursor3 = conn.execute("SELECT stock_balance FROM STOCKS WHERE user_id = " + str(user_id) + " AND stock_symbol = '" + str(stock_symbol) + "'")
    cursor4 = conn.execute("SELECT usd_balance FROM USERS WHERE ID = " + str(user_id))
    owned_stock_balance = cursor3.fetchall() # list of current ownded stock balanced for the associated stock_symbol
    if (len(cursor.fetchall()) == 0): # user id has not enteries in USER table
        message = "403: User " + str(user_id) + " does not exist"
        return message
    elif(len(owned_stock_balance) == 0): # list containing stocks owned by user is empty for according stock_symbol.
        message = "403: User " + str(user_id) + " does not own any stock with symbol: " + stock_symbol
        return message
    balance = float(cursor4.fetchall()[0][0]) # balance for current user
    stock_balance = float(cursor2.fetchall()[0][0]) # stock_balance for the current user for the associated stock_symbol
    if(amount > stock_balance): # the amount of stocks to be sold is larger than stock balance
        message = "403: Insufficent Stock Balance"
        return message
    else: # passed logical error checking
        cursor3 = conn.execute("SELECT * FROM STOCKS WHERE stock_symbol = '" + stock_symbol + str("'"))
        if(amount == stock_balance): # deletes the entire entry since amount stock to be sold is equal to stock_balance
            conn.execute("DELETE FROM STOCKS WHERE stock_symbol = '" + str(stock_symbol) + "' AND user_id = " + str(user_id))
            conn.commit()
            conn.execute("UPDATE USERS SET usd_balance = (usd_balance + " + str(total) + ") WHERE ID = " + str(user_id))
            conn.commit()
            message = two_hundred_ok + "SOLD: New balance: " + str(stock_balance - amount) + " " + str(stock_symbol) + ". USD balance $" + str(balance + total)
            return message
        else: # user DOES own stocks of stock_symbol, update stock amount 
            conn.execute("UPDATE STOCKS SET stock_balance = (stock_balance - " + str(amount) + ") WHERE stock_symbol = '" + str(stock_symbol + "' AND user_id = ") + str(user_id))
            conn.commit()
            conn.execute("UPDATE USERS SET usd_balance = (usd_balance + " + str(total) + ") WHERE ID = " + str(user_id))
            conn.commit()
            message = two_hundred_ok + "SOLD: New balance: " + str(stock_balance - amount) + " " + str(stock_symbol) + ". USD balance $" + str(balance + total)
            return message  


# Precondtions: User and Stock Tables are created
# Postcondtions: All stock records are listed
def print_list(conn):
    #mutex.acquire()
    cursor = conn.execute("Select * FROM USERS")
    records = cursor.fetchall()
    message = two_hundred_ok 
    if(len(records) != 0): # there are users in the database
        for userRecord in records: # for each user in user table, prints their stocks holdings
                message += "The list of records in the Crypto database for user " + str(userRecord[0]) + ":\n"
                cursor = conn.execute("Select * FROM STOCKS WHERE user_id = " + str(userRecord[0]))
                relatedList = cursor.fetchall()
                i = 1
                if len(relatedList) != 0: # user does own stock
                    for stockRecord in relatedList: # for each stock in user holdings, print its information
                        message += str(i) + "\t " + str(stockRecord[1]) + " " + str(stockRecord[3]) + " " + str(stockRecord[4]) + "\n"
                        i += 1
                else:  # user does not own stock
                    message += "\tUser does not own any stock\n"  
    else: # there are not users in the database
        message = "403: There are no users in the database."
    #mutex.release()    
    return message


# Preconditions: User and Stock Tables are created
# Postconditions: All user balance records are listed
def balance(conn):
    cursor = conn.execute("Select * FROM USERS")
    records = cursor.fetchall()
    message = two_hundred_ok 
    if(len(records) != 0): # there are users in the database
        for userRecord in records: # for each user in user table, prints their stocks holdings
                message += "Balance for user " + str(userRecord[1]) + " " + str(userRecord[2]) + ": $" + str(userRecord[5]) + "\n"
    else: # there are not users in the database
        message = "403: There are no users in the database."
    return message


# Preconditions: Client connected to Server
# Postconditions: Client socket is closed, server closes and program ends
def shutdown(clientSocket):
    global isShutDown
    global threads
    message = "200 OK"
    clientSocket.send(message.encode('ascii')) # Notifies client that program ends
    #for socket in workers:
    #    socket.close() # Close Client Socket
    clientSocket.close()
    s.close()
    isShutDown = True
    #for thread in threads:
    #   thread.join()
    return message

# Precondtions: USERS table is created
# Postcondtions: The four users are created, if they already exists, no users are created
def  create_user(conn):
    #names = ["John", "Doe", "April", "Summer", "James", "Robert", "Elizabeth", "Jobs", "Robert", "David", "Mary", "Linda"]
    # conn.execute("INSERT INTO USERS (first_name,last_name,user_name,password, usd_balance) \
    #   VALUES ('" + str(names[random.randint(0,11)]) + "', '" + str(names[random.randint(0,11)]) + "', 'user_name', 'password', 100)"); # pushes new user into the user table
    try:
        conn.execute("INSERT INTO USERS (first_name,last_name,user_name,password, usd_balance, ID) \
        VALUES ('" + "Root" + "', '" + "User" + "', 'Root', 'Root01', 100 , 1)"); # pushes new user into the user table
        conn.commit()

        conn.execute("INSERT INTO USERS (first_name,last_name,user_name,password, usd_balance, ID) \
        VALUES ('" + "Mary" + "', '" + "Jones" + "', 'Mary', 'Mary01', 100 , 2)"); # pushes new user into the user table
        conn.commit()

        conn.execute("INSERT INTO USERS (first_name,last_name,user_name,password, usd_balance, ID) \
        VALUES ('" + "John" + "', '" + "Smith" + "', 'John', 'John01', 100 , 3)"); # pushes new user into the user table
        conn.commit()

        conn.execute("INSERT INTO USERS (first_name,last_name,user_name,password, usd_balance, ID) \
        VALUES ('" + "Moe" + "', '" + "Shukur" + "', 'Moe', 'Moe01', 100 , 4)"); # pushes new user into the user table
        conn.commit()
    except:
        pass # Users have already been created

    return None


# Precondtions: stock_symbol, i_amount, i_price, i_user_id are user inputs
# Postcondtions: determmines if there is any syntax error, if not, type casts user inputs for use for command functions
def errorcheck(stock_symbol, i_amount, i_price, i_user_id):
    message = ""
    amount = 0
    user_id = 0

    if( not (len(stock_symbol) <= 5 and stock_symbol.isalpha())): # invalid stock_symbol
        error = "RECEIVED: Invalid Command: Invalid Stock Symbol\n"
        message = "403: Invalid Format or Stock Symbol Doesn't Exist"
        return (False, message , error)
    elif (not (i_amount.isnumeric() and i_price.isnumeric() and i_user_id.isnumeric())): # invalid numeric arguments
        error = "RECEIVED: Invalid Command: Invalid Numeric Arguments\n"
        message = "403: Invalid Format for BUY or SELL Command Arguments"
        return (False, message, error)
    else : # valid inputs so typecast to correct type
        amount = int(i_amount)
        price = float(i_price)
        user_id = int(i_user_id)
        return (True, "accepted", "no error", amount, price, user_id)

def log_in(userName, password, conn):
    cursor = conn.execute("Select user_name , password FROM USERS")
    conn.commit()
    user_list = cursor.fetchall()
    match = False
    try:
        #print(user_list)
        match = (userName, password) in user_list
    except:
        print("error")

    if match == True:

        return (match, "200 OK")
    else:
        return (match, "403: Invalid User Name or Password")
    
def log_out():
    try:
        if isLoggedIn.my_data == True:
            isLoggedIn.my_data = False
            return "200 OK"
        else:
            return "403: Already Not Logged In"
    except:
        return "403: Already Not Logged In" # thread not created yet, log in did not occur yet

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates socket
s.bind((socket.gethostname(),port)) # bind socket to part 
s.listen(5) # server starts listening

conn = sqlite3.connect('dataBase.db')
# Creates the tables if they don't exist
conn.execute('''CREATE TABLE IF NOT EXISTS USERS(
    ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    first_name varchar(255), 
    last_name varchar(255), 
    user_name varchar(255), 
    password varchar(255), 
    usd_balance DOUBLE NOT NULL 
    );'''
    )
conn.execute('''CREATE TABLE IF NOT EXISTS STOCKS(
    ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    stock_symbol varchar(4) NOT NULL, 
    stock_name varchar(20), 
    stock_balance DOUBLE, 
    user_id int,  
    FOREIGN KEY (user_id) REFERENCES USERS(ID) 
    );'''
    )
    
create_user(conn)
# Enforces foreign keys, not on by default.
conn.execute("pragma foreign_keys = ON;")
conn.close() # close the database

def serve_request(clientSocket):
    #loop represents client's session with server
    global command
    global message
    global isShutDown
    command = ""
    amount = 0
    price = 0
    user_id = 0
    isLoggedIn.my_data = False

    while command != "QUIT" and isShutDown == False: 
        #wait for input from client
        response = clientSocket.recv(2018).decode('ascii').split()
        stock_symbol = None
        user_id = None

        #reset string holders 
        message = "400 Invalid Command"

        #parse input into commands and parameters
        for index, token in enumerate(response):
            if (index == 0):
                command = str(token)
            if (index == 1):
                stock_symbol = str(token)
            if (index == 2):
                amount = str(token)
            if (index == 3): 
                price = str(token)
            if (index == 4):
                user_id = str(token)


        #  Command Switch Board. Executes user command by calling corrosponding command function
        if(command == "SHUTDOWN" and stock_symbol is None):
            print("Received: SHUTDOWN\n")
            message = shutdown(clientSocket)
            break
        elif(command == "QUIT" and stock_symbol is None):
            command = ""
            break
        elif(command == "LIST" and stock_symbol is None ):
            if isLoggedIn.my_data == True:
                print("Received: LIST\n")
                conn = sqlite3.connect('dataBase.db')
                message = print_list(conn)
                conn.close()
            else:
                print("Received: LIST(NOT LOGGED IN)\n")
                message = "403: Not logged in"
        elif(command == "BALANCE" and stock_symbol is None):
            print("Received: BALANCE\n")
            conn = sqlite3.connect('dataBase.db')
            message = balance(conn)
            conn.close()
        elif(command == "BUY" and user_id is not None):
            if(errorcheck(stock_symbol, amount, price, user_id)[0]):
                print("Received: BUY " + stock_symbol + " " + str(amount) + " " + str(price) + " " + str(user_id) + "\n")
                amount, price, user_id = errorcheck(stock_symbol, amount, price, user_id)[3:6]
                print(amount, price, user_id)
                conn = sqlite3.connect('dataBase.db')
                message = buy(stock_symbol, amount, price, user_id,conn)
                conn.close()
            else: 
                message = errorcheck(stock_symbol, amount, price, user_id)[1]
                print(errorcheck(stock_symbol, amount, price, user_id)[2])
        elif(command == "SELL" and user_id is not None):
            if(errorcheck(stock_symbol, amount, price, user_id)[0]):
                amount, price, user_id = errorcheck(stock_symbol, amount, price, user_id)[3:6]
                print("Received: SELL " + stock_symbol + " " + str(amount) + " " + str(price) + " " + str(user_id) + "\n")
                conn = sqlite3.connect('dataBase.db')
                message = sell(stock_symbol, amount, price, user_id,conn)
                conn.close()
        elif(command == "LOGIN"):
            conn = sqlite3.connect('dataBase.db')
            print("Recieved Loggin Request\n")
            temp = log_in(stock_symbol, amount, conn)
            if temp[0] == True:
                isLoggedIn.my_data = True
            print(isLoggedIn.my_data)
            message = temp[1]
            conn.close()
        elif(command == "LOGOUT"):
            if isLoggedIn.my_data == True:
                message = log_out()
                print("RECEIVED: Logout Request")
            else: 
                message = log_out()
                print("RECIEVED: Logout Request(Not Logged In Case)")
        else:
            message = errorcheck(stock_symbol, amount, price, user_id)[1]
            print(errorcheck(stock_symbol, amount, price, user_id)[2])
        


        #send response back to client
        clientSocket.send(message.encode('ascii'))
        
        #reset string holders 
        message = "400 Invalid Command"
        response = ""
    clientSocket.close() # close the socket
    return (message,command)

workers = []
threads = []
isLoggedIn = threading.local()

while command != "SHUTDOWN":
    #wait for new client to connect
    clientSocket, address = s.accept()
#   print("Connection established from address " + str(address))
    client_thread = threading.Thread(target=serve_request, args = (clientSocket,))
    workers.append(clientSocket)
    threads.append(client_thread)
    client_thread.start()

    if isShutDown == True:
        print("shutdown worked")
        for thread in threads:
            thread.join()
    print(command)

