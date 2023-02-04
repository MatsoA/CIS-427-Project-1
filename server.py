import socket
import sqlite3
message = ""
two_hundred_ok = "200 OK \n"
stockCount = 1
userCount = 1
conn = sqlite3.connect('test.db')
def buy(stock_symbol, amount, price, user_id):
    total = amount * price # amount of stocks * price of each stock
    global message # declaring message is a global variable

    # creating sub databases for error checking
    cursor = conn.execute("SELECT * FROM USERS WHERE ID = " + str(user_id))
    cursor2 = conn.execute("SELECT usd_balance FROM USERS WHERE ID = " + str(user_id))
    cursor3 = conn.execute("SELECT stock_balance FROM STOCKS WHERE ID = " + str(user_id) + " AND '" + str(stock_symbol) + "'")

    

    if (len(cursor.fetchall()) == 0): # user id has not enteries in USER table
        message = "User " + str(user_id) + " does not exist"
        return None

    balance = float(cursor2.fetchall()[0][0]) # balance for current user

    if(balance < total): # the total price exceeds the balance for the user
        message = "Insufficent Balance"
        return None
    else: # passed logical error checking
        cursor3 = conn.execute("SELECT * FROM STOCKS WHERE stock_symbol = '" + stock_symbol + str("'"))
        if(len(cursor3.fetchall()) == 0): # user DOES NOT own any stocks of type stock_symbol, creates a new entry
            global stockCount
            stockCount = stockCount + 1
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
        message = "User " + str(user_id) + " does not exist"
        return None
    elif(len(owned_stock_balance) == 0): # list containing stocks owned by user is empty for according stock_symbol.
        message = "User " + str(user_id) + " does not own any stock with symbol: " + stock_symbol
        return None

    balance = float(cursor4.fetchall()[0][0]) # balance for current user
    stock_balance = float(cursor2.fetchall()[0][0]) # stock_balance for the current user for the associated stock_symbol

    if(amount > stock_balance): # the amount of stocks to be sold is larger than stock balance
        message = "Insufficent Stock Balance"
        return None
    else: # passed logical error checking
        cursor3 = conn.execute("SELECT * FROM STOCKS WHERE stock_symbol = '" + stock_symbol + str("'"))
        if(amount == stock_balance): # deletes the entire entry since amount stock to be sold is equal to stock_balance
            conn.execute("DELETE FROM STOCKS WHERE stock_symbol = '" + str(stock_symbol) + "' AND user_id = " + str(user_id))
            conn.commit()
            conn.execute("UPDATE USERS SET usd_balance = (usd_balance + " + str(total) + ") WHERE ID = " + str(user_id))
            conn.commit()
            message = two_hundred_ok + "SOLD: New balance: " + str(stock_balance - amount) + " " + str(stock_symbol) + ". USD balance $" + str(balance - total)
            return None
        else: # user DOES own stocks of stock_symbol, update stock amount 
            conn.execute("UPDATE STOCKS SET stock_balance = (stock_balance - " + str(amount) + ") WHERE stock_symbol = '" + str(stock_symbol + "' AND user_id = ") + str(user_id))
            conn.commit()
            conn.execute("UPDATE USERS SET usd_balance = (usd_balance + " + str(total) + ") WHERE ID = " + str(user_id))
            conn.commit()
            message = two_hundred_ok + "SOLD: New balance: " + str(stock_balance - amount) + " " + str(stock_symbol) + ". USD balance $" + str(balance + total)
            return None  

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(),3108))
s.listen(5)

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
      VALUES ('Hadi', 'Zazali', 'hzal', 'password', 100)");
conn.commit()


#  Test Cases Here:
buy('APPLE', 2, 4, 1)
buy('GOOGLE', 2, 4, 1)
buy('Tesla', 2, 4, 1)

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

print(message)

print("Opened database successfully")
while False:
    clientSocket, address = s.accept()
    print("Connection established from address " + str(address))
    #handleRequest(string)
    clientSocket.send(bytes(message))
    clientSocket.close()

conn.close()
