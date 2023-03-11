import socket
import sqlite3
<<<<<<< Updated upstream
message = ""
=======
import random
import threading
global message
global amount
global price
global user_id
port = 3106 # Socket port number
message = "400 Invalid Message" # message sent to the client
response = "" # response from the client
command = "" # command from the client
amount = "" # amount of stocks from client arguments
price = "" # price of stocks from client arguments
user_id = "" # user ID from client arguments

>>>>>>> Stashed changes
two_hundred_ok = "200 OK \n"
conn = sqlite3.connect('test.db')

# Precondtion: the user and stock tables are created. stock_symbol is a string. amount, price, and user_id are integers
# Postcondtion: the buy stock is serviced

def buy(stock_symbol, amount, price, user_id):
    total = amount * price # amount of stocks * price of each stock
<<<<<<< Updated upstream
    global message # declaring message is a global variable

=======
    message = "" # creating message variable
>>>>>>> Stashed changes
    # creating sub databases for error checking
    cursor = conn.execute("SELECT * FROM USERS WHERE ID = " + str(user_id))
    cursor2 = conn.execute("SELECT usd_balance FROM USERS WHERE ID = " + str(user_id))
    cursor3 = conn.execute("SELECT stock_balance FROM STOCKS WHERE ID = " + str(user_id) + " AND '" + str(stock_symbol) + "'")

    if (len(cursor.fetchall()) == 0): # user id has not enteries in USER table
        message = "403: User " + str(user_id) + " does not exist"
<<<<<<< Updated upstream
        return None

=======
        return message
>>>>>>> Stashed changes
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

def sell(stock_symbol, amount, price, user_id):
    total = amount * price # amount of stocks * price of each stock
<<<<<<< Updated upstream
    global message # declaring message is a global variable

=======
    message = "" # creating message variable
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
        return None

=======
        return message
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
            message = two_hundred_ok + "SOLD: New balance: " + str(stock_balance - amount) + " " + str(stock_symbol) + ". USD balance $" + str(balance - total)
            return None
=======
            message = two_hundred_ok + "SOLD: New balance: " + str(stock_balance - amount) + " " + str(stock_symbol) + ". USD balance $" + str(balance + total)
            return message
>>>>>>> Stashed changes
        else: # user DOES own stocks of stock_symbol, update stock amount 
            conn.execute("UPDATE STOCKS SET stock_balance = (stock_balance - " + str(amount) + ") WHERE stock_symbol = '" + str(stock_symbol + "' AND user_id = ") + str(user_id))
            conn.commit()
            conn.execute("UPDATE USERS SET usd_balance = (usd_balance + " + str(total) + ") WHERE ID = " + str(user_id))
            conn.commit()
            message = two_hundred_ok + "SOLD: New balance: " + str(stock_balance - amount) + " " + str(stock_symbol) + ". USD balance $" + str(balance + total)
            return message  

# Precondtions: User and Stock Tables are created
# Postcondtions: All stock records are listed

def list():
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
<<<<<<< Updated upstream

    return None
=======
    return message
>>>>>>> Stashed changes

# Precondtions: User and Stock Tables are created
# Postcondtions: All user balance records are listed

def balance():
    cursor = conn.execute("Select * FROM USERS")
    records = cursor.fetchall()
    message = two_hundred_ok 
    if(len(records) != 0): # there are users in the database
        for userRecord in records: # for each user in user table, prints their stocks holdings
                message += "Balance for user " + str(userRecord[1]) + " " + str(userRecord[2]) + ": $" + str(userRecord[5]) + "\n"
    else: # there are not users in the database
        message = "403: There are no users in the database."
    return message


<<<<<<< Updated upstream
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(),3108))
s.listen(5)

=======
# Preconditions: Client connected to Server
# Postconditions: Client socket is closed, server closes and program ends
def shutdown():
    message = "200 OK"
    clientSocket.send(message.encode('ascii')) # Notifies client that program ends
    clientSocket.close() # Close Client Socket
    s.close()
    return message

# Precondtions: USERS table is created
# Postcondtions: The four users are created, if they already exists, no users are created
def  create_user():
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
    global amount
    global price
    global user_id

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
        price = float(price)
        user_id = int(user_id)
        return (True, "accepted", "no error")


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates socket
s.bind((socket.gethostname(),port)) # bind socket to part 
s.listen(5) # server starts listening


# Creates the tables if they don't exist
>>>>>>> Stashed changes
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

# Generates first user and assigns first stock
conn.execute("INSERT INTO USERS (first_name,last_name,user_name,password, usd_balance) \
      VALUES ('John', 'Doe', 'JDoe', 'password', 100)");
conn.commit()


#  Test Cases Here:
buy("TSLA",1,3,1)
buy("APPLE",1,3,1)
buy("Ford",1,3,1)
list()
balance()

cursor = conn.execute("SELECT ID, first_name, last_name, user_name, password, usd_balance from USERS")
for row in cursor:
    print("ID = " + str(row[0]))
    print ("first_name = " + str(row[1]))
    print ("last_name = " + str(row[2]))
    print ("user_name = " + str(row[3]))
    print ("password = " + str(row[4]))
    print ("usd_balance = "+ str(row[5]))
print("\n")
cursor = conn.execute("SELECT * from STOCKS")
for row in cursor:
    print("ID = " + str(row[0]))
    print ("stock_symbol = " + str(row[1]))
    print ("stock_name = "+ str(row[2]))
    print ("stock_balance = "+ str(row[3]))
    print ("user_id = "+ str(row[4]))


print("\n" + message)

print("Opened database successfully")
while False:
    clientSocket, address = s.accept()
    print("Connection established from address " + str(address))
    #handleRequest(string)
    clientSocket.send(bytes(message))
    clientSocket.close()

<<<<<<< Updated upstream
conn.close()
=======
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
            message = shutdown()
            break
        elif(command == "QUIT" and stock_symbol is None):
            command = ""
            break
        elif(command == "LIST" and stock_symbol is None ):
            print("Received: LIST\n")
            message = print_list()
        elif(command == "BALANCE" and stock_symbol is None):
            print("Received: BALANCE\n")
            message = balance()
        elif(command == "BUY" and user_id is not None):
            if(errorcheck(stock_symbol, amount, price, user_id)[0]):
                print("Received: BUY " + stock_symbol + " " + str(amount) + " " + str(price) + " " + str(user_id) + "\n")
                message = buy(stock_symbol, amount, price, user_id)
            else: 
                message = errorcheck(stock_symbol, amount, price, user_id)[1]
                print(errorcheck(stock_symbol, amount, price, user_id)[2])
        elif(command == "SELL" and user_id is not None):
            if(errorcheck(stock_symbol, amount, price, user_id)[0]):
                print("Received: SELL " + stock_symbol + " " + str(amount) + " " + str(price) + " " + str(user_id) + "\n")
                message = sell(stock_symbol, amount, price, user_id)
            else:
                message = errorcheck(stock_symbol, amount, price, user_id)[1]
                print(errorcheck(stock_symbol, amount, price, user_id)[2])



        #send response back to client
        clientSocket.send(message.encode('ascii'))
        
        #reset string holders 
        message = "400 Invalid Command"
        response = ""
    clientSocket.close() # close the socket


conn.close() # close the database
>>>>>>> Stashed changes
