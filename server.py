import socket
import sqlite3
import random
global message
global amount
global price
global user_id
port = 3107 # Socket port number
message = "400 Invalid Message" # message sent to the client
response = "" # response from the client
command = "" # command from the client
amount = "" # amount of stocks from client arguments
price = "" # price of stocks from client arguments
user_id = "" # user ID from client arguments

two_hundred_ok = "200 OK \n"
conn = sqlite3.connect('dataBase.db')
# Precondtion: the user and stock tables are created. stock_symbol is a string. amount, price, and user_id are integers
# Postcondtion: the buy stock is serviced
def buy(stock_symbol, amount, price, user_id):
    total = amount * price # amount of stocks * price of each stock
    global message # declaring message is a global variable
    # creating sub databases for error checking
    cursor = conn.execute("SELECT * FROM USERS WHERE ID = " + str(user_id))
    cursor2 = conn.execute("SELECT usd_balance FROM USERS WHERE ID = " + str(user_id))
    cursor3 = conn.execute("SELECT stock_balance FROM STOCKS WHERE ID = " + str(user_id) + " AND '" + str(stock_symbol) + "'")
    if (len(cursor.fetchall()) == 0): # user id has not enteries in USER table
        message = "403: User " + str(user_id) + " does not exist"
        return None
    balance = float(cursor2.fetchall()[0][0]) # balance for current user
    if(balance < total): # the total price exceeds the balance for the user
        message = "403: Insufficent Balance"
        return None
    else: # passed logical error checking
        cursor3 = conn.execute("SELECT * FROM STOCKS WHERE stock_symbol = '" + stock_symbol + str("'") + str(" AND user_id = ") + str(user_id))
        if(len(cursor3.fetchall()) == 0): # user DOES NOT own any stocks of type stock_symbol, creates a new entry
            conn.execute("INSERT INTO STOCKS (stock_symbol,stock_balance,user_id) VALUES ('" + str(stock_symbol) + "', " + str(amount) + ", " + str(user_id) + ")")
            conn.commit()
            conn.execute("UPDATE USERS SET usd_balance = (usd_balance - " + str(total) + ") WHERE ID = " + str(user_id))
            conn.commit()
            message = two_hundred_ok + "BOUGHT: New balance: " + str(amount) + " " + str(stock_symbol) + ". USD balance $" + str(balance - total)
            return None
        else: # user DOES own stocks of stock_symbol, update stock amount 
            conn.execute("UPDATE STOCKS SET stock_balance = (stock_balance + " + str(amount) + ") WHERE stock_symbol = '" + str(stock_symbol) + "' AND user_id = " + str(user_id))
            conn.commit()
            conn.execute("UPDATE USERS SET usd_balance = (usd_balance - " + str(total) + ") WHERE ID = " + str(user_id))
            conn.commit()
            cursor3 = conn.execute("SELECT stock_balance FROM STOCKS WHERE user_id = " + str(user_id) + " AND stock_symbol = '" + str(stock_symbol) + "'")
            conn.commit()
            message = two_hundred_ok + "BOUGHT: New balance: " + str(float(cursor3.fetchall()[0][0])) + " " + str(stock_symbol) + ". USD balance $" + str(balance - total)
            return None


# Precondtion: the user and stock tables are created. stock_symbol is a string. amount, price, and user_id are integers
# Postcondtion: the sell stock is serviced
def sell(stock_symbol, amount, price, user_id):
    total = amount * price # amount of stocks * price of each stock
    global message # declaring message is a global variable
    # creating sub databases for error checking
    cursor = conn.execute("SELECT * FROM USERS WHERE ID = " + str(user_id))
    cursor2 = conn.execute("SELECT stock_balance FROM STOCKS WHERE user_id = " + str(user_id) + " AND stock_symbol = '" + str(stock_symbol) + "'")
    cursor3 = conn.execute("SELECT stock_balance FROM STOCKS WHERE user_id = " + str(user_id) + " AND stock_symbol = '" + str(stock_symbol) + "'")
    cursor4 = conn.execute("SELECT usd_balance FROM USERS WHERE ID = " + str(user_id))
    owned_stock_balance = cursor3.fetchall() # list of current ownded stock balanced for the associated stock_symbol
    if (len(cursor.fetchall()) == 0): # user id has not enteries in USER table
        message = "403: User " + str(user_id) + " does not exist"
        return None
    elif(len(owned_stock_balance) == 0): # list containing stocks owned by user is empty for according stock_symbol.
        message = "403: User " + str(user_id) + " does not own any stock with symbol: " + stock_symbol
        return None
    balance = float(cursor4.fetchall()[0][0]) # balance for current user
    stock_balance = float(cursor2.fetchall()[0][0]) # stock_balance for the current user for the associated stock_symbol
    if(amount > stock_balance): # the amount of stocks to be sold is larger than stock balance
        message = "403: Insufficent Stock Balance"
        return None
    else: # passed logical error checking
        cursor3 = conn.execute("SELECT * FROM STOCKS WHERE stock_symbol = '" + stock_symbol + str("'"))
        if(amount == stock_balance): # deletes the entire entry since amount stock to be sold is equal to stock_balance
            conn.execute("DELETE FROM STOCKS WHERE stock_symbol = '" + str(stock_symbol) + "' AND user_id = " + str(user_id))
            conn.commit()
            conn.execute("UPDATE USERS SET usd_balance = (usd_balance + " + str(total) + ") WHERE ID = " + str(user_id))
            conn.commit()
            message = two_hundred_ok + "SOLD: New balance: " + str(stock_balance - amount) + " " + str(stock_symbol) + ". USD balance $" + str(balance + total)
            return None
        else: # user DOES own stocks of stock_symbol, update stock amount 
            conn.execute("UPDATE STOCKS SET stock_balance = (stock_balance - " + str(amount) + ") WHERE stock_symbol = '" + str(stock_symbol + "' AND user_id = ") + str(user_id))
            conn.commit()
            conn.execute("UPDATE USERS SET usd_balance = (usd_balance + " + str(total) + ") WHERE ID = " + str(user_id))
            conn.commit()
            message = two_hundred_ok + "SOLD: New balance: " + str(stock_balance - amount) + " " + str(stock_symbol) + ". USD balance $" + str(balance + total)
            return None  


# Precondtions: User and Stock Tables are created
# Postcondtions: All stock records are listed
def print_list():
    cursor = conn.execute("Select * FROM USERS")
    records = cursor.fetchall()
    global message
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
    return None


# Preconditions: User and Stock Tables are created
# Postconditions: All user balance records are listed
def balance():
    cursor = conn.execute("Select * FROM USERS")
    records = cursor.fetchall()
    global message
    message = two_hundred_ok 
    if(len(records) != 0): # there are users in the database
        for userRecord in records: # for each user in user table, prints their stocks holdings
                message += "Balance for user " + str(userRecord[1]) + " " + str(userRecord[2]) + ": $" + str(userRecord[5]) + "\n"
    else: # there are not users in the database
        message = "403: There are no users in the database."
    return None


# Preconditions: Client connected to Server
# Postconditions: Client socket is closed, server closes and program ends
def shutdown():
    message = "200 OK"
    clientSocket.send(message.encode('ascii')) # Notifies client that program ends
    clientSocket.close() # Close Client Socket
    s.close()

# Precondtions: USERS table is created
# Postcondtions: a new user which a random name is generated. Since the client cannot declare their names, we will randomly generate them since balance command reveals user's names
def  create_user():
    names = ["John", "Doe", "April", "Summer", "James", "Robert", "Elizabeth", "Jobs", "Robert", "David", "Mary", "Linda"]
    conn.execute("INSERT INTO USERS (first_name,last_name,user_name,password, usd_balance) \
      VALUES ('" + str(names[random.randint(0,11)]) + "', '" + str(names[random.randint(0,11)]) + "', 'user_name', 'password', 100)"); # pushes new user into the user table
    conn.commit()
    return None


# Precondtions: stock_symbol, i_amount, i_price, i_user_id are user inputs
# Postcondtions: determmines if there is any syntax error, if not, type casts user inputs for use for command functions
def errorcheck(stock_symbol, i_amount, i_price, i_user_id):
    global message
    global amount
    global price
    global user_id

    if( not (len(stock_symbol) <= 5 and stock_symbol.isalpha())): # invalid stock_symbol
        print("RECEIVED: Invalid Command: Invalid Stock Symbol\n")
        message = "403: Invalid Format or Stock Symbol Doesn't Exist"
        return False
    elif (not (i_amount.isnumeric() and i_price.isnumeric() and i_user_id.isnumeric())): # invalid numeric arguments
        print("RECEIVED: Invalid Command: Invalid Numeric Arguments\n")
        message = "403: Invalid Format for BUY or SELL Command Arguments"
        return False
    else : # valid inputs so typecast to correct type
        amount = int(i_amount)
        price = float(price)
        user_id = int(user_id)
        return True


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates socket
s.bind((socket.gethostname(),port)) # bind socket to part 
s.listen(5) # server starts listening


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
    

# Enforces foreign keys, not on by default.
conn.execute("pragma foreign_keys = ON;")


while command != "SHUTDOWN":
    #wait for new client to connect
    clientSocket, address = s.accept()
#   print("Connection established from address " + str(address))
    create_user()
    #loop represents client's session with server
    while command != "QUIT": 
        #wait for input from client
        response = clientSocket.recv(2018).decode('ascii').split()
        stock_symbol = None
        user_id = None


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
            shutdown()
            break
        elif(command == "QUIT" and stock_symbol is None):
            command = ""
            break
        elif(command == "LIST" and stock_symbol is None ):
            print("Received: LIST\n")
            print_list()
        elif(command == "BALANCE" and stock_symbol is None):
            print("Received: BALANCE\n")
            balance()
        elif(command == "BUY" and user_id is not None):
            if(errorcheck(stock_symbol, amount, price, user_id)):
                print("Received: BUY " + stock_symbol + " " + str(amount) + " " + str(price) + " " + str(user_id) + "\n")
                buy(stock_symbol, amount, price, user_id)
        elif(command == "SELL" and user_id is not None):
            if(errorcheck(stock_symbol, amount, price, user_id)):
                print("Received: SELL " + stock_symbol + " " + str(amount) + " " + str(price) + " " + str(user_id) + "\n")
                sell(stock_symbol, amount, price, user_id)



        #send response back to client
        clientSocket.send(message.encode('ascii'))
        
        #reset string holders 
        message = "400 Invalid Command"
        response = ""
    clientSocket.close() # close the socket


conn.close() # close the database