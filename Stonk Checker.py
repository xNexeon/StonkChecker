from tkinter import *
import pymongo
from pprint import pprint
from yahoo_fin import stock_info as si
import time


## Varables

## Functions:

##Screens
def loginScreen(): # Main initial window
    global username_entryvar
    global pass_entryvar
    global login_screen
    login_screen = Tk()
    
    username_entry = Entry(login_screen)
    username_entry.place(x=24,y=10, width=200)
    username_entry.insert(0, "Username")
    username_entryvar = username_entry
    
    pass_entry = Entry(login_screen)
    pass_entry.place(x=24,y=35, width=200)
    pass_entry.insert(0, "Password")
    pass_entryvar = pass_entry
    
    login_btn = Button(text="Login", width=25, command=loginbtnPressed)
    login_btn.place(x=30,y=70)
    
    register_btn = Button(text="Register", width=25, command=registerbtnPressed)
    register_btn.place(x=30,y=100)    
    
    login_screen.title('Login')
    login_screen.geometry("245x140+10+10")
    login_screen.resizable(False, False)
    login_screen.mainloop()
    
def regScreen(): # Registration screen
    global username_entry1var
    global pass_entryconfirmvar
    global pass_entry1var
    global reg_screen
    reg_screen = Tk()
    
    
    username_entry1 = Entry(reg_screen)
    username_entry1.place(x=24,y=10, width=200)
    username_entry1.insert(0, "Username")
    username_entry1var = username_entry1
    
    pass_entry1 = Entry(reg_screen)
    pass_entry1.place(x=24,y=35, width=200)
    pass_entry1.insert(0, "Password")
    pass_entry1var = pass_entry1
    
    pass_entryconfirm = Entry(reg_screen)
    pass_entryconfirm.place(x=24,y=60, width=200)
    pass_entryconfirm.insert(0, "Confirm Password")
    pass_entryconfirmvar = pass_entryconfirm
    
    register_btn1 = Button(reg_screen, text="Register", width=25, command=actuallyRegister)
    register_btn1.place(x=30,y=100)  

    reg_screen.title('Register')
    reg_screen.geometry("245x140+10+10")
    reg_screen.resizable(False, False)
    reg_screen.mainloop()

def stockScreen():
    global gmepricelabel
    global kosspricelabel
    global amcpricelabel
    global nokpricelabel
    gmeprice = si.get_live_price("gme")
    kossprice = si.get_live_price("koss")
    amcprice = si.get_live_price("amc")
    nokprice = si.get_live_price("nok")
    stock_screen = Tk()
    
    gmelabel = Label(stock_screen, text="$GME: $", font=("verdana", 24))
    gmelabel.place(x=24,y=5)
        
    kosslabel = Label(stock_screen, text="$KOSS: $", font=("verdana", 24))
    kosslabel.place(x=5,y=50)
    
    amclabel = Label(stock_screen, text="$AMC: $", font=("verdana", 24))
    amclabel.place(x=24,y=95)
    
    noklabel = Label(stock_screen, text="$NOK: $", font=("verdana", 24))
    noklabel.place(x=24,y=140)

    
    gmepricelabel = Label(stock_screen, text="0", font=("verdana", 24))
    gmepricelabel.place(x=165,y=5)
    
    kosspricelabel = Label(stock_screen, text="0", font=("verdana", 24))
    kosspricelabel.place(x=165,y=50)
        
    amcpricelabel = Label(stock_screen, text="0", font=("verdana", 24))
    amcpricelabel.place(x=165,y=95)
    
    nokpricelabel = Label(stock_screen, text="0", font=("verdana", 24))
    nokpricelabel.place(x=165,y=140)
    
    
    updatestockbtn = Button(stock_screen, text="Update Stonks", command=updateStocks)
    updatestockbtn.place(x=105,y=500)
    

    
    
        
       
    
    stock_screen.title('Stonks')
    stock_screen.geometry("300x550+10+10")
    stock_screen.resizable(False, False)
    stock_screen.mainloop()


def updateStocks():
        gmeprice = round(si.get_live_price("gme"), 2)
        kossprice = round(si.get_live_price("koss"), 2)
        amcprice = round(si.get_live_price("amc"), 2)
        nokprice = round(si.get_live_price("nok"), 2)
        gmepricelabel["text"]=gmeprice
        kosspricelabel["text"]=kossprice
        amcpricelabel["text"]=amcprice
        nokpricelabel["text"]=nokprice
    
#### Buttons #####    
def loginbtnPressed(): # Logs loginbtn Pressed
    print("login_btn pressed")
    actuallyLogin()
    
def registerbtnPressed(): # Logs registerbtn Pressed
    print("register_btn pressed (Opening reg window)")
    regScreen()
   
#### Register functions ####   
def actuallyRegister(): # Push registration info to monogInsert function
    print("register_btn1 pressed (Actually registering user)")
    username_push = str(username_entry1var.get())
    password_push = str(pass_entry1var.get())
    pass_confirm = str(pass_entryconfirmvar.get())
    if password_push == pass_confirm: # Pass has to be equal to pass_confirm for push to work #
        mongopushRegister(username_push, password_push)
        print("Success (Pushing registration to database)")
        messagebox.showinfo(title="Success", message="Registration successful, you can now log in")
        reg_screen.withdraw()
    else:
        print("pass_confirm isn't equal to password_push")
        messagebox.showerror(title="Error", message="Check your password and try again")
        reg_screen.lift()
        

def mongopushRegister(username_push, password_push): # Mongo registration push function
    client = pymongo.MongoClient("mongodb+srv://nex:nikodem2002@cluster0.3r7u0.mongodb.net/<dbname>?retryWrites=true&w=majority")
    mydb = client["nexauthusers"]
    mycol = mydb["users"]
    datainsert = { "username": username_push, "password": password_push }
    x = mycol.insert_one(datainsert)
    
def actuallyLogin():
    global username_login
    global password_login
    
    print("Attempting to login user")
    username_login = str(username_entryvar.get())
    password_login = str(pass_entryvar.get())
    mongoreadloginDb()
    
 
def mongoreadloginDb(): # Mongo check if login exists function
    client = pymongo.MongoClient("mongodb+srv://nex:nikodem2002@cluster0.3r7u0.mongodb.net/<dbname>?retryWrites=true&w=majority")
    mydb = client["nexauthusers"]
    mycol = mydb["users"]
    myquery = { "username": username_login, "password": password_login }
    accountval = 0
    
    mydoc = mycol.find(myquery)
    for x in mydoc:
        print("Account exists in database")
        accountval = 1
    if accountval == 1 :
        print("Login successful")
        login_screen.withdraw()
        stockScreen()
    else:
        print("Invalid credentials")
        messagebox.showerror(title="Error", message="Incorrect credentials or account doesn't exist")
        


loginScreen()
        
#stockScreen()
    
    
    
    
    
    
