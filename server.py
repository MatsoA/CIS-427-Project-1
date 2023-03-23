import socket
import sqlite3
import random
import threading
import sys

global message
global amount
global price
global user_id
global command
global isShutDown
isShutDown = False
port = 8361# Socket port number
message = "400 Invalid Message" # message sent to the client
response = "" # response from the client
command = "" # command from the client
amount = "" # amount of stocks from client arguments
price = "" # price of stocks from client arguments
user_id = "" # user ID from client arguments
mutex = threading.Lock()

two_hundred_ok = "200 OK \n"

# Keeps track of local thread storage
class threadLocalStorage:
    isLoggedIn = threading.local() # Keeps track of log in status
    userName = threading.local() # Keeps track of username of logged user
    passWord = threading.local() # Keeps track of password of logged user
    userID = threading.local() # Keeps track of userID of logged user

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
    if current_user.userName.my_data == "Root" and current_user.passWord.my_data == "Root01" and current_user.userID.my_data == 1:
        cursor = conn.execute("Select * FROM USERS ")
        records = cursor.fetchall()
        message = two_hundred_ok 
        if(len(records) != 0): # there are users in the database
            for userRecord in records: # for each user in user table, prints their stocks holdings
                    #message += "The list of records in the Crypto database for user " + str(userRecord[0]) + ":\n"
                    cursor = conn.execute("Select * FROM STOCKS WHERE user_id = " + str(userRecord[0]))
                    relatedList = cursor.fetchall()
                    i = 1
                    if len(relatedList) != 0: # user does own stock
                        for stockRecord in relatedList: # for each stock in user holdings, print its information
                            message += str(i) + "\t " + str(stockRecord[1]) + " " + str(stockRecord[3]) + " " + str(userRecord[1])  +  "\n"
                            i += 1
        else: # there are not users in the database
            message = "403: There are no users in the database."   
        return message
    else:
        cursor = conn.execute("Select * FROM USERS WHERE ID = " + str(current_user.userID.my_data))
        records = cursor.fetchall()
        message = two_hundred_ok 
        if(len(records) != 0): # there are users in the database
            for userRecord in records: # for each user in user table, prints their stocks holdings
                    message += "The list of records in the Crypto database for " + str(userRecord[1]) + ":\n"
                    cursor = conn.execute("Select * FROM STOCKS WHERE user_id = " + str(userRecord[0]))
                    relatedList = cursor.fetchall()
                    i = 1
                    if len(relatedList) != 0: # user does own stock
                        for stockRecord in relatedList: # for each stock in user holdings, print its information
                            message += str(i) + "\t " + str(stockRecord[1]) + " " + str(stockRecord[3])  + "\n"
                            i += 1
                    else:  # user does not own stock
                        message += "\tUser does not own any stock\n"  
        else: # there are not users in the database
            message = "403: There are no users in the database."   
        return message


# Preconditions: User and Stock Tables are created
# Postconditions: All user balance records are listed
def balance(conn):
    filter = ""
    if current_user.userName.my_data == "Root" and current_user.passWord.my_data == "Root01" and current_user.userID.my_data == 1:
        filter = "" # Root User, Show all balances
    else:
        filter = " where ID = " + str(current_user.userID.my_data)

    cursor = conn.execute("Select * FROM USERS" + filter)
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
    if current_user.userName.my_data == "Root":
        message = "200 OK"
        clientSocket.send(message.encode('ascii')) # Notifies client that program ends
        #for socket in workers:
        #    socket.close() # Close Client Socket
        clientSocket.close()
        s.close()
        isShutDown = True
        sys.exit()
        #for thread in threads:
        #   thread.join()
    else :
        message = "failed incorrect user"
    return message

# Precondtions: USERS table is created
# Postcondtions: The four users are created, if they already exists, no users are created
def  create_user(conn):
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

# Precondtions: username and password are strings, thread is connected using conn to database
# Postconditons: Returns whether there is a match in records and the appropriate message to client.
def log_in(userName, password, conn):
    cursor = conn.execute("Select user_name , password FROM USERS")
    conn.commit()
    cursor2 = conn.execute("Select ID FROM USERS")
    conn.commit()
    user_list = cursor.fetchall() # list of users
    ID_list = cursor2.fetchall() # list of ID's
    match = False # returned to indicate if there was a match between username and password in database
    index = 0
    try:
        match = (userName, password) in user_list # True if there is a match, False if there is no match
        index = user_list.index((userName, password)) # The index of this match, used to match ID to user.
    except:
        pass # did not find user
    #    print("Login Error")
    for entry in who_list:
            if str(entry[0]) == userName:
                return (False, "403: Already Logged In On a Different Client")
            
    if current_user.isLoggedIn.my_data == False: # If is not currently logged in
        if match == True: # If there is a match
            return (match, "200 OK", userName, password, int(ID_list[index][0])) # Returns information needed to update current user information 
        else:
            return (match, "403: Invalid User Name or Password") # Returns false with error message
    else: 
        return (False, "403: Already Logged In On This Client") # Handles case where user is already logged in.
    
# Precondtions: none
# Postcondtions: current client is logged out if they are already logged in.
def log_out():
    try:
        if current_user.isLoggedIn.my_data == True:
            current_user.isLoggedIn.my_data = False
            return "200 OK"
        else:
            return "403: Already Not Logged In"
    except:
        return "403: Already Not Logged In" # thread not created yet, log in did not occur yet

# Precondtions: amount is a floating number, current client is connected to database using conn
# Postconditons: balance is updated if amount is a postive number
def deposit(amount, conn):
    if amount > 0:
        conn.execute("UPDATE USERS SET usd_balance = (usd_balance + " + str(amount) + ") WHERE ID = " + str(current_user.userID.my_data))
        conn.commit()
        cursor2 = conn.execute("Select usd_balance FROM USERS where ID = "  + str(current_user.userID.my_data))
        balance = cursor2.fetchall()
        return "deposit successfully, New Balance $" + str(balance[0][0])
    else:
        return "401: Amount is Zero or Less"

# Precondtions: user is root user and logged in.
# Postcondtions: the current logged in users and their IP Addresses are returned
def who():
    if(len(who_list) != 0):
        message = "The list of active users:\n"
        for entry in who_list:
            message += str(entry[0]) + "\t" + str(entry[1][0]) + "\n"
        return message
    else:
        return("403: Unauthorized Use of Who Command") # Client is logged out and accessed the who command

# Precondtions: user is logged in, stock is a string, client thread is connected to database using conn
# Postcondtions: list of records with stock name(either full name or symbol) are returned for the logged user.
def lookup(stock, conn):
    cursor = conn.execute("Select stock_symbol, stock_name, stock_balance  FROM STOCKS WHERE user_id = " + str(current_user.userID.my_data))
    conn.commit()
    canidates = cursor.fetchall()
    if len(canidates) != 0:
        message = ""
        count = 0
        for i in range(len(canidates)):
            if canidates[i][0] == stock or canidates[i][1] == stock:
                message += stock + "\t" + str(canidates[i][2]) + "\n"
                count += 1
        if count > 0: # Search did yield a result
            start_message = "Found " + str(count) + " match\n"
            return start_message + message 
        else:
            return "404: Your search did not match any records." # Search did not yield any results
    else:
        return "404: Your search did not match any records." # No stocks in database for this user

# Precondtions: 
# Postcondtions: 
def serve_request(address,clientSocket):
    #loop represents client's session with server
    global command
    global message
    global isShutDown
    command = ""
    current_user.isLoggedIn.my_data = False

    while command != "QUIT" and isShutDown == False: 
        #wait for input from client
        response = clientSocket.recv(2018).decode('ascii').split()
        stock_symbol = None
        amount = None
        price = None
        user_id = None

        #reset string holders 
        if isShutDown == True: # close the socket
            message = "SHUTDOWN" # close the socket
        else:
            message = "400 Invalid Command"

        #parse input into commands and parameters
        for index, token in enumerate(response):
            if (index == 0):
                command = str(token).upper()
            if (index == 1):
                stock_symbol = str(token).upper()
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
            if current_user.isLoggedIn.my_data == True: # Is Logged In
                who_list.remove((current_user.userName.my_data, address)) # removes user if they forgot to logout before quitting
            else:
                pass
            break
        elif(command == "LIST" and stock_symbol is None ):
            if current_user.isLoggedIn.my_data == True:
                print("Received: LIST\n")
                conn = sqlite3.connect('dataBase.db')
                message = print_list(conn)
                conn.close()
            else:
                print("Received: LIST (Not Logged In Case)\n")
                message = "403: Not Logged In"
        elif(command == "BALANCE" and stock_symbol is None):
            if current_user.isLoggedIn.my_data == True: # Is Logged In
                print("Received: BALANCE\n")
                conn = sqlite3.connect('dataBase.db')
                message = balance(conn)
                conn.close()
            else:
                message = "403: Not Logged In"
                print("Received: BALANCE Request (Not Logged In Case)")
        elif(command == "BUY"):
            if current_user.isLoggedIn.my_data == True: ## User Is Logged In Case
                if(errorcheck(stock_symbol, amount, price, str(current_user.userID.my_data))[0]):
                    print("Received: BUY " + stock_symbol + " " + str(amount) + " " + str(price) + " " + str(current_user.userID.my_data) + " (Logged In Case)\n")
                    amount, price, user_id = errorcheck(stock_symbol, amount, price, str(current_user.userID.my_data))[3:6]
                    conn = sqlite3.connect('dataBase.db')
                    message = buy(stock_symbol, amount, price, current_user.userID.my_data,conn)
                    conn.close()
                else: # Did Not Pass Error Check
                    message = errorcheck(stock_symbol, amount, price,  str(current_user.userID.my_data))[1]
                    print(errorcheck(stock_symbol, amount, price,  str(current_user.userID.my_data))[2])
            else: # User is Not Logged In Case
                message = "403: Not Logged In"
                print("Received: BUY " + stock_symbol + " " + str(amount) + " " + str(price) + " (Not Logged In Case)\n")
        elif(command == "SELL"):
            if current_user.isLoggedIn.my_data == True: ## User Is Logged In Case
                if(errorcheck(stock_symbol, amount, price, str(current_user.userID.my_data))[0]):
                    amount, price, user_id = errorcheck(stock_symbol, amount, price, str(current_user.userID.my_data))[3:6]
                    print("Received: SELL " + stock_symbol + " " + str(amount) + " " + str(price) + " " + str(current_user.userID.my_data) + " (Logged In Case)\n")
                    conn = sqlite3.connect('dataBase.db')
                    message = sell(stock_symbol, amount, price, current_user.userID.my_data,conn)
                    conn.close()
                else: #Did Not Pass Error Check
                    message = errorcheck(stock_symbol, amount, price,  str(current_user.userID.my_data))[1]
                    print(errorcheck(stock_symbol, amount, price,  str(current_user.userID.my_data))[2])
            else: # User is Not Logged In Case
                message = "403: Not Logged In"
                print("Received: SELL " + stock_symbol + " " + str(amount) + " " + str(price) + " (Not Logged In Case)\n")
            
        elif(command == "LOGIN" and len(response) == 3):
            conn = sqlite3.connect('dataBase.db')
            print("Recieved Login Request\n")

            username = response[1]
            password = response[2] 
            login_response = log_in(username, password, conn)

            if login_response[0] == True:
                current_user.isLoggedIn.my_data = True
                current_user.userName.my_data = login_response[2]
                current_user.passWord.my_data = login_response[3]
                current_user.userID.my_data = login_response[4]
                entry = (current_user.userName.my_data, address)
                who_list.append(entry)

            message = login_response[1]
            conn.close()
        elif(command == "LOGOUT" and stock_symbol is None):
            if current_user.isLoggedIn.my_data == True:
                message = log_out()
                who_list.remove((current_user.userName.my_data, address))
                print("RECEIVED: LOGOUT Request")
            else: 
                message = log_out()
                print("RECIEVED: LOGOUT Request (Not Logged In Case)")
        elif(command == "DEPOSIT" and len(response) == 2):
            if current_user.isLoggedIn.my_data == True:
                print("Received: DEPOSIT\n")
                deposit_amount = response[1]
                conn = sqlite3.connect('dataBase.db')
                message = deposit(int(deposit_amount), conn)
                conn.close()
            else:
                print("Received: DEPOSIT (NOT LOGGED IN CASE)\n")
                message = "403: Not Logged In"

        elif(command == "WHO" and stock_symbol == None):
            if current_user.isLoggedIn.my_data == True: # Is Logged In
                if current_user.userName.my_data == "Root" and current_user.passWord.my_data == "Root01" and current_user.userID.my_data == 1: ## Is Root User
                    message = who()
                    print("Received: WHO Request (Root User Case)")
                else: # Logged in but not Root User
                    message = "403: Not Authorized to Issue This Command"
                    print("Received: WHO Request (Not Root User Case)")
            else:
                message = "403: Not Logged In"
                print("Received: WHO Request (Not Logged In Case)")
        elif(command == "LOOKUP" and len(response) == 2):
            if current_user.isLoggedIn.my_data == True: # Is Logged In
                conn = sqlite3.connect('dataBase.db')
                message = lookup(stock_symbol,conn)
                conn.close()
                print("Received: LOOKUP Request (Logged In Case)")
            else:
                message = "403: Not Logged In"
                print("Received: LOOKUP Request (Not Logged In Case)")

        #send response back to client
        clientSocket.send(message.encode('ascii'))
        
        #reset string holders 
        message = "400 Invalid Command"
        response = ""
    clientSocket.close() # close the socket
    return (message,command)


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



workers = [] # Place Holder, does nothing currently
threads = [] # Place Holder, does nothing currently

#isLoggedIn = threading.local()



current_user = threadLocalStorage()
who_list = [] # Used to keep track of logged users

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates socket
s.bind((socket.gethostname(),port)) # bind socket to part 
s.listen(5) # server starts listening
print(command)
while command != "SHUTDOWN":
    #wait for new client to connect
    clientSocket, address = s.accept()
#   print("Connection established from address " + str(address))
    client_thread = threading.Thread(target=serve_request, args = (address, clientSocket,))

    workers.append(clientSocket) # Does nothing currently
    threads.append(client_thread) # Does nothing currently 

    client_thread.start()
    if isShutDown == True: # not working
        print("shutdown worked")
        for thread in threads:
            thread.join()
   

