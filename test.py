import tkinter as tk
from customtkinter import *
from PIL import Image
from tkinter import messagebox
from database import Database
from teamwork import *
import sqlite3
import csv

# # The window set ups
signup_window = tk.Tk()
signup_window.title("Cash Register App")
signup_window.resizable(0,0)
signup_window.geometry('500x400+300+100')
signup_window.configure(background = 'white')


# # THE WINDOWS
# LOGINPAGE
def login():
    '''Logs the user in, reads the role and department of the person logged in and directs them to their individual page'''
    if nameEntry.get() == '' or passwordEntry.get() == '':
        messagebox.showerror('Alert', 'Fill in both inputs.')

    else:
        user = db.get_user(nameEntry.get(), passwordEntry.get())
        if user is None:
            messagebox.showerror('No such user',
                                 'Login or password is incorrect.')
        else: 
            messagebox.showinfo('Success',f"You've been logged in as {user}")
            if user == 'user':
                user_page()
            # treasurer page
            if user == 'treasurer':
                treas_page()
            # financial officer page
            if user == 'finofficer':
                # finoff_page()
                pass
            # admin page
            if user == 'admin':
                admin_page()

def login_page():
    '''Loads in the login page upon loging out'''
    for widget in signup_window.winfo_children():  # Get all widgets in the window
        if isinstance(widget, CTkFrame):  # Check if it's a Frame
            widget.grid_forget()

    loginFrame.grid(row=0, column=0, sticky='nsew') # reframes and makes the login page appear

    nameEntry.delete(0, "end")  # Clears the name in the login
    passwordEntry.delete(0, "end")  # Clears the password in the login
        

def toobad():
    '''Pop up for the forget password option'''
    messagebox.showerror('LMAO', 'too bad')

# QUIT AND LOGOUT
def quit_logout():
    '''A custom Quit button next to a LogOut button to put underneath all other windows but the login'''
    
    # input variable buttomFrame
    global bottomFrame
    
    # create 
    bottomFrame = CTkFrame(signup_window, fg_color='white')
    bottomFrame.grid(row=1, column=0, sticky='s', columnspan=2)
    
    buttonQuit = CTkButton(bottomFrame, 
                       text='Quit', text_color='black', fg_color='white', cursor='hand2', hover_color='white',
                       width=30, 
                       command=signup_window.destroy, hover='underline')
    buttonQuit.grid(row=0, column=0, pady=(20,0), sticky='s')
    
    buttonLouOut = CTkButton(bottomFrame, 
                       text='Log Out', text_color='black', fg_color='white', cursor='hand2', hover_color='white',
                       width=50, 
                       command=login_page)
    buttonLouOut.grid(row=0, column=1, pady=(20,0), sticky='s')


def user_page():
    ''' A function to show the 'functionality' for users
    which was not defined in the exercise'''

    global userFrame

    #deletes the login page
    loginFrame.grid_forget()

    # new frame made
    userFrame = CTkFrame(signup_window, fg_color='white')
    userFrame.grid(row=0, column=0, sticky='nsew', padx=50)
    cat_picture = CTkImage(light_image=Image.open("a21740a7b0f6b96a92e4805c8df8aa7e.jpg"), size=(400, 300))
    look = CTkLabel(userFrame, text='Look at this dinky cat!', font=('', 10, 'bold'), text_color='black')
    look.grid(row=1, column=0)
    label = CTkLabel(userFrame, image=cat_picture, text="")  # text="" removes text overlay
    label.grid(row=0, column=0)

    # quit and logout buttons are added
    quit_logout()
    

# # ADMIN POWERS
def admin_page():
    '''adds the functions that admins can do'''
    global adminFrame
    
    for widget in signup_window.winfo_children():
        if isinstance(widget, CTkFrame):
            widget.grid_forget()
    
    adminFrame = CTkFrame(signup_window, fg_color='white')
    adminFrame.grid(row=0, column=0, pady=20, columnspan=2)
    
    admin_label = tk.Label(adminFrame, text= f'Welcome {nameEntry.get()}!', font=('Times New Roman', 20, 'bold'), background='white')
    admin_label.grid(row=0, column=0, pady=20, columnspan=2)    
    
    addUser = CTkButton(adminFrame, text='Add User', width=210, cursor='hand2', command=add_user)
    addUser.grid(row=1, column=0, pady=(20,0), padx=20)
    updateUser = CTkButton(adminFrame, text='Update User', width=210, cursor='hand2', command=update_user)
    updateUser.grid(row=1, column=1, pady=(20,0), padx=20)
    removeUser = CTkButton(adminFrame, text='Remove User', width=210, cursor='hand2', command=remove_user)
    removeUser.grid(row=2, column=0, pady=(20,0), padx=20)
    addClub = CTkButton(adminFrame, text='Add a Club', width=210, cursor='hand2', command=add_club)
    addClub.grid(row=2, column=1, pady=(20,0), padx=20)
    printStat = CTkButton(adminFrame, text='Print Statement', width=460, cursor='hand2', command=db.save_data) #command=db.department_balances)
    printStat.grid(row=3, column=0, columnspan =2, pady=(20,0), padx=20)
    
    quit_logout()


def add_club():
    '''A function to add a new club, assigning a person to be a treasurer'''

    global addFrame
    global clubinput
    global moneyinput
    
    def submit_form():
        # actually turns the inputs into a new member
        try:
            club = clubinput.get()
            money = int(moneyinput.get())
            login = treasurerinput.get()
        except:
            messagebox.showerror("Input Error", "Please put in valid inputs")
            return

        # Validation
        if login == '' or  club == '' or money == '':
            messagebox.showerror("Input Error", "Please fill in all fields!")
            return
        if money <0:
            messagebox.showerror("Alert", "Do not take on loans")
            return

        # look if login is valid
        try:
            id = db.get_id(login)[0][0]
            print(id)
        except: 
            messagebox.showerror("Alert", "No such person in the registry")
            return

        # add the club
        department = db.get_department(login)[0][0]
        print(department)
        db.assign_treasurer(id, department)
        db.update_department(login, club)
        Account(club, money)
        messagebox.showinfo("Success", f"You created the club {club}")
        
        clubinput.delete(0, "end")  # Clears the name in the login
        moneyinput.delete(0, "end")  # Clears the password in the login
        treasurerinput.delete(0, "end")  # Clears the password in the login
        

    for widget in signup_window.winfo_children():
        if isinstance(widget, CTkFrame):
            widget.grid_forget()
    
    quit_logout()
    
    addFrame = CTkFrame(signup_window, fg_color='white', width=500)
    addFrame.grid(row=0, column=0, sticky='nsew')
    
    clubinputLabel = CTkLabel(addFrame, text='Input a Name for the new club:', text_color='black', width=220)
    clubinputLabel.grid(row=0, column=0, pady=20, padx=20, sticky='w')
    clubinput = CTkEntry(addFrame, fg_color='white', width=200, text_color='black')
    clubinput.grid(row=0, column=1)
    
    moneyinputLabel = CTkLabel(addFrame, text='Input a starting € amount for the the club:', text_color='black', width=200)
    moneyinputLabel.grid(row=1, column=0, pady=20, padx=20, sticky='w')
    moneyinput = CTkEntry(addFrame, fg_color='white', width=200, text_color='black')
    moneyinput.grid(row=1, column=1)
    
    treasurerinputLabel = CTkLabel(addFrame, text='Input a Name for the member in charge:', text_color='black', width=200)
    treasurerinputLabel.grid(row=2, column=0, pady=20, padx=20, sticky='w')
    treasurerinput = CTkEntry(addFrame, fg_color='white', width=200, text_color='black')
    treasurerinput.grid(row=2, column=1)
    
    # Button to Submit whatever is in the name or password bubbles
    buttonSubmit = CTkButton(addFrame, text='Submit', width=150, cursor='hand2', command=submit_form)
    buttonSubmit.grid(row=4, column=1, sticky='e')
    buttonBack = CTkButton(addFrame, text='Back', width=150, cursor='hand2', command=lambda: (admin_page()))
    buttonBack.grid(row=4, column=0, sticky='w', padx=20)
        

def add_user():
    '''Adding new members as users'''
    def submit_form():
        # actually turns the inputs into a new member
        login = memberinput.get()
        password = passwordinput.get()
        role = 'user'
        department = departmentinput.get()
        
        all_deps = db.all_departments()
        
        
        # Validation
        if login == '' or  password == '' or department == '':
            messagebox.showerror("Input Error", "Please fill in all fields!")
            return
        if department not in all_deps:
            messagebox.showerror("Alert", "No such department")
            return
        if department == 'club':
            messagebox.showerror("Alert", "No such department")
            return
            
                
        # Call the add_user function to add the user
        db.add_user(login, password, role, department)
        messagebox.showinfo("Success", f"You signed up {login}")
        
        memberinput.delete(0, "end")  # Clears the name in the login
        passwordinput.delete(0, "end")  # Clears the password in the login
        departmentinput.delete(0, "end")  # Clears the password in the login

    # deletes all frames from before
    for widget in signup_window.winfo_children():
        if isinstance(widget, CTkFrame):
            widget.grid_forget()

    # load in the quit and logout buttons
    quit_logout()
    # load in the actual frame
    adduserFrame = CTkFrame(signup_window, fg_color='white', width=500)
    adduserFrame.grid(row=0, column=0, sticky='nsew')
    # member input
    memberinputLabel = CTkLabel(adduserFrame, text='Input a login name for the new member:', text_color='black', width=200)
    memberinputLabel.grid(row=0, column=0, pady=20, padx=20, sticky='w')
    memberinput = CTkEntry(adduserFrame, fg_color='white', width=200, text_color='black')
    memberinput.grid(row=0, column=1)
    # password input
    passwordinputLabel = CTkLabel(adduserFrame, text='Input a password for the new member:', text_color='black', width=200)
    passwordinputLabel.grid(row=1, column=0, pady=20, padx=20, sticky='w')
    passwordinput = CTkEntry(adduserFrame, fg_color='white', width=200, text_color='black')
    passwordinput.grid(row=1, column=1)
    # department input
    departmentinputLabel = CTkLabel(adduserFrame, text='Input a club for the member:', text_color='black', width=200)
    departmentinputLabel.grid(row=2, column=0, pady=20, padx=20, sticky='w')
    departmentinput = CTkEntry(adduserFrame, fg_color='white', width=200, text_color='black')
    departmentinput.grid(row=2, column=1)
    
    # Button to Submit whatever is in the name or password bubbles
    buttonSubmit = CTkButton(adduserFrame, text='Submit', width=150, cursor='hand2', command=submit_form)
    buttonSubmit.grid(row=4, column=1, sticky='e')
    buttonBack = CTkButton(adduserFrame, text='Back', width=150, cursor='hand2', command=lambda: (admin_page()))
    buttonBack.grid(row=4, column=0, sticky='w', padx=20)

def update_user():
    '''updating member's department'''
    def submit_form():
        # actually turns the inputs into a new member
        login = memberinput.get()
        department = departmentinput.get()
        role = str(roleinput.get())
        password = passwordinput.get()
        all_deps = db.all_departments()
        
        # Validation
        if login == '' or department == '':
            messagebox.showerror("Input Error", "Please fill in all fields!")
            return

        user = db.get_user(login, password)
        if user is None:
            messagebox.showerror('No such user',
                                 'Login or password is incorrect.')
            return

        if department not in all_deps:
            messagebox.showerror("Alert", "No such department")
            return
        
        if role not in ['user', 'treasurer', 'finofficer']:
            messagebox.showerror("Alert", "No such role")
            return

        if role == 'finofficer':
            department = 'club'
        # Call the add_user function to add the user
        db.update_user(login, password, role, department)
        messagebox.showinfo("Success", f"You updated {login}")
        
        memberinput.delete(0, "end")  # Clears the name
        passwordinput.delete(0, "end")  # Clears the password
        roleinput.delete(0, "end")  # Clears the role
        departmentinput.delete(0, "end")  # Clears the department
    
    for widget in signup_window.winfo_children():
        if isinstance(widget, CTkFrame):
            widget.grid_forget()

    # load in the quit and logout buttons
    quit_logout()
    # load in the actual frame
    userFrame = CTkFrame(signup_window, fg_color='white', width=500)
    userFrame.grid(row=0, column=0, sticky='nsew')
    # member input
    memberinputLabel = CTkLabel(userFrame, text='Input the person you want to change:', text_color='black', width=220)
    memberinputLabel.grid(row=1, column=0, pady=20, padx=20, sticky='w')
    memberinput = CTkEntry(userFrame, fg_color='white', width=200, text_color='black')
    memberinput.grid(row=1, column=1)
    # password input
    passwordinputLabel = CTkLabel(userFrame, text='Input their password to verify:', text_color='black', width=200)
    passwordinputLabel.grid(row=2, column=0, pady=20, padx=20, sticky='w')
    passwordinput = CTkEntry(userFrame, fg_color='white', width=200, text_color='black')
    passwordinput.grid(row=2, column=1)
    # role input
    roleinputLabel = CTkLabel(userFrame, text='Input a role for the member:', text_color='black', width=200)
    roleinputLabel.grid(row=3, column=0, pady=20, padx=20, sticky='w')
    roleinput = CTkEntry(userFrame, fg_color='white', width=200, text_color='black')
    roleinput.grid(row=3, column=1)
    # department input
    departmentinputLabel = CTkLabel(userFrame, text='Input a department for the member:', text_color='black', width=200)
    departmentinputLabel.grid(row=4, column=0, pady=20, padx=20, sticky='w')
    departmentinput = CTkEntry(userFrame, fg_color='white', width=200, text_color='black')
    departmentinput.grid(row=4, column=1)
    
    # Button to Submit whatever is in the name or password bubbles
    buttonSubmit = CTkButton(userFrame, text='Submit', width=150, cursor='hand2', command=submit_form)
    buttonSubmit.grid(row=5, column=1, columnspan = 2, sticky='e')
    buttonBack = CTkButton(userFrame, text='Back', width=150, cursor='hand2', command=lambda: (admin_page()))
    buttonBack.grid(row=5, column=0, columnspan = 2, sticky='w', padx=20)


def remove_user():
    def submit_form():
        # actually turns the inputs into a new member
        login = memberinput.get()
        password = passwordinput.get()
        
        # Validation
        if login == '' or password == '':
            messagebox.showerror("Input Error", "Please fill in all fields!")
            return

        user = db.get_user(login, password)
        if user is None:
            messagebox.showerror('No such user',
                                 'Login or password is incorrect.')
            return
        
        id = db.get_id(login)[0][0]
        db.delete_user(id)
        messagebox.showinfo("Success", f"You deleted {login}")
        
        memberinput.delete(0, "end")  # Clears the name
        passwordinput.delete(0, "end")  # Clears the password
        
    
    for widget in signup_window.winfo_children():
        if isinstance(widget, CTkFrame):
            widget.grid_forget()

    # load in the quit and logout buttons
    quit_logout()
    # load in the actual frame
    userFrame = CTkFrame(signup_window, fg_color='white', width=500)
    userFrame.grid(row=0, column=0, sticky='nsew')
    # member input
    memberinputLabel = CTkLabel(userFrame, text='Input the person you want to change:', text_color='black', width=220)
    memberinputLabel.grid(row=1, column=0, pady=20, padx=20, sticky='w')
    memberinput = CTkEntry(userFrame, fg_color='white', width=200, text_color='black')
    memberinput.grid(row=1, column=1)
    # password input
    passwordinputLabel = CTkLabel(userFrame, text='Input their password to verify:', text_color='black', width=200)
    passwordinputLabel.grid(row=2, column=0, pady=20, padx=20, sticky='w')
    passwordinput = CTkEntry(userFrame, fg_color='white', width=200, text_color='black')
    passwordinput.grid(row=2, column=1)
    
    # Button to Submit whatever is in the name or password bubbles
    buttonSubmit = CTkButton(userFrame, text='Delete', width=150, cursor='hand2', command=submit_form)
    buttonSubmit.grid(row=5, column=1, columnspan = 2, sticky='e')
    buttonBack = CTkButton(userFrame, text='Back', width=150, cursor='hand2', command=lambda: (admin_page()))
    buttonBack.grid(row=5, column=0, columnspan = 2, sticky='w', padx=20)

# TRESURER POWERS
def treas_page():
    '''adds the functions that treasurers can do to the menu'''
    global treasFrame

    for widget in signup_window.winfo_children():
        if isinstance(widget, CTkFrame):
            widget.grid_forget()

    treasFrame = CTkFrame(signup_window, fg_color='white')
    treasFrame.grid(row=0, column=0, pady=20, columnspan=2, sticky='nsew')

    treas_label = tk.Label(treasFrame, text= f'Welcome {nameEntry.get()}!', font=('Times New Roman', 20, 'bold'), background='white')
    treas_label.grid(row=0, column=0, pady=(20,0), columnspan=2) 

    withdraw_transer = CTkButton(treasFrame, text='Issue Finances', width=210, cursor='hand2', command=make_withdraw)
    withdraw_transer.grid(row=1, column=0, pady=(20,0), padx=20)

    view_history = CTkButton(treasFrame, text='View History', width=210, cursor='hand2', command=db.save_transactions)
    view_history.grid(row=1, column=1, pady=(20,0), padx=20)

    transfer_transer = CTkButton(treasFrame, text='Issue transfer', width=210, cursor='hand2', command=transfer)
    transfer_transer.grid(row=2, column=0, pady=(20,0), padx=20)

    quit_logout()


def make_withdraw():

    def submit_form():
    # actually turns the inputs into a new member
        try:
            withdraw = withdrawinput.get()
            deposit = depositinput.get()
            login = nameEntry.get()
            department = db.get_department(login)[0][0]
        except:
            messagebox.showerror("Input Error", "Please put in valid inputs!")
            return

    # Validation
        if not withdraw and not deposit:
            messagebox.showerror("Input Error", "Please fill at least one field!")
            return
        elif withdraw and not deposit:
        # Call the withdraw function
            if db.make_withdraw(department, int(withdraw)) is not None:
                messagebox.showinfo('Success', 'Money withdrawn!' )
            else: messagebox.showerror('Alert', 'Not enough money in the account!')
        elif deposit and not withdraw:
        # Call the deposit function
            db.make_deposit(department, int(deposit))
            messagebox.showinfo('Success', 'Money deposited' )
        elif deposit and withdraw:
        # Call both functions
            db.make_deposit(department, int(deposit))
            db.make_withdraw(department, int(withdraw))
            messagebox.showinfo('Success', 'Money deposited and withdrawn!' )
        
        withdrawinput.delete(0, "end")  # Clears the name
        depositinput.delete(0, "end")  # Clears the password

    for widget in signup_window.winfo_children():
        if isinstance(widget, CTkFrame):
            widget.grid_forget()

    quit_logout()

    withdrawFrame = CTkFrame(signup_window, fg_color='white', width=500)
    withdrawFrame.grid(row=0, column=0)

    withdrawLabel = CTkLabel(withdrawFrame, text='set the amount you want to withdraw', text_color='black', width=200)
    withdrawLabel.grid(row=0, column=0, pady=20, padx=20, sticky='w')
    withdrawinput = CTkEntry(withdrawFrame, fg_color='white', width=220, text_color='black')
    withdrawinput.grid(row=0, column=1, padx=(0,20))

    depositLabel = CTkLabel(withdrawFrame, text='set the amount you want to deposit', text_color='black', width=200)
    depositLabel.grid(row=1, column=0, pady=20, padx=20, sticky='w')
    depositinput = CTkEntry(withdrawFrame, fg_color='white', width=220, text_color='black')
    depositinput.grid(row=1, column=1, padx=(0,20))

    buttonSubmit = CTkButton(withdrawFrame, text='Submit', width=150, cursor='hand2', command=submit_form)
    buttonSubmit.grid(row=5, column=1, columnspan = 2, sticky='e', padx=20)
    buttonBack = CTkButton(withdrawFrame, text='Back', width=150, cursor='hand2', command=lambda: (treas_page()))
    buttonBack.grid(row=5, column=0, columnspan = 2, sticky='w', padx=20)


def transfer():
    def submit_form():
    # actually turns the inputs into a new member
        try:
            isfrom = db.get_department(nameEntry.get())[0][0]
            print(isfrom)
            department = departmentinput.get()
            transfer = int(transferinput.get())
            all_deps = db.all_departments()
            print(all_deps)
        except:
            messagebox.showerror("Input Error", "Please put in valid inputs!")
            return

    # Validation
        if not department and not transfer:
            messagebox.showerror("Input Error", "Please fill at least one field!")
            return
        
        if department not in all_deps:
            messagebox.showerror("Alert", "No such department")
            return

        db.transfer(transfer, isfrom, department)
        departmentinput.delete(0, "end")  # Clears the name
        transferinput.delete(0, "end")  # Clears the password

    for widget in signup_window.winfo_children():
        if isinstance(widget, CTkFrame):
            widget.grid_forget()

    quit_logout()

    transferFrame = CTkFrame(signup_window, fg_color='white', width=500)
    transferFrame.grid(row=0, column=0)

    transferLabel = CTkLabel(transferFrame, text='set the amount you want to transfer', text_color='black', width=200)
    transferLabel.grid(row=0, column=0, pady=20, padx=20, sticky='w')
    transferinput = CTkEntry(transferFrame, fg_color='white', width=220, text_color='black')
    transferinput.grid(row=0, column=1, padx=(0,20))

    departmentLabel = CTkLabel(transferFrame, text='Set what club gets the transfer', text_color='black', width=200)
    departmentLabel.grid(row=1, column=0, pady=20, padx=20, sticky='w')
    departmentinput = CTkEntry(transferFrame, fg_color='white', width=220, text_color='black')
    departmentinput.grid(row=1, column=1, padx=(0,20))

    buttonSubmit = CTkButton(transferFrame, text='Submit', width=150, cursor='hand2', command=submit_form)
    buttonSubmit.grid(row=5, column=1, columnspan = 2, sticky='e', padx=20)
    buttonBack = CTkButton(transferFrame, text='Back', width=150, cursor='hand2', command=lambda: (treas_page()))
    buttonBack.grid(row=5, column=0, columnspan = 2, sticky='w', padx=20)



# FINOFFICER POWERS
def finofficer_addition():
    '''adds the functions that financial officers can do to the menu'''
    global finofFrame
    
    for widget in signup_window.winfo_children():
        if isinstance(widget, CTkFrame):
            widget.grid_forget()
    
    finofFrame = CTkFrame(signup_window, fg_color='white')
    finofFrame.grid(row=3, column=0, pady=20, columnspan=2)
    
    finof_label = tk.Label(finofFrame, text= f'Welcome {nameEntry.get()}!', font=('Times New Roman', 20, 'bold'), background='white')
    finof_label.grid(row=0, column=0, pady=(20,0), columnspan=2) 
    view_status = CTkButton(finofFrame, text='View Status', width=210, cursor='hand2')
    view_status.grid(row=0, column=0, pady=(20,0), padx=20)




### DATABASE SHIT
db = Database(sqlite3.connect('database.db'),
              sqlite3.connect('database.db').cursor())

members = [('Mary_Brown', 'NqKX069L', 'admin', 'club'),
           ('John_Elder', 'OnH139sp', 'finofficer', 'club'),
           ('Wes_Smith', '850QuL96', 'treasurer', 'football'),
           ('Bob_Miller', '0ITF8cO2', 'user', 'football'),
           ('Dan_White', 'tSh8c8j3', 'treasurer', 'hiking'),
           ('Tim_Smith', 'Yor4T4Z2', 'user', 'hiking'),
           ('Joe_Black', 'fC584HGq', 'user', 'football'),
           ('Laura_Lie', '3S2k5WYu', 'user', 'hiking'),
           ('Rico_Salieri', 'c1jV1k4p', 'user', 'football'),
           ('Anton_Kusnezow', '253DzRap', 'user', 'hiking')]

for i in members:
    db.add_user(*i)


# # Page of the login
loginFrame = CTkFrame(signup_window, fg_color='white')
loginFrame.grid(row=0, column=0, sticky='nsew')

#Exit button to be on every site
buttonQuit = CTkButton(loginFrame, 
                       text='Quit', text_color='black', fg_color='white', hover_color='white', cursor='hand2',
                       width=30, 
                       command=signup_window.destroy)
buttonQuit.grid(row=1, column=0, pady=(20,0), sticky='s')

# entire login frame
inputFrame = CTkFrame(loginFrame, fg_color='white')
inputFrame.grid(row=0, column=0)
inputFrame.configure()

# Title welcome screen
input_label = tk.Label(inputFrame, text='Log in to proceed', font=('Times New Roman', 20, 'bold'), background='white')
input_label.grid(row=0, column=0, pady=20)

# Login name input bubble
nameEntry = CTkEntry(inputFrame,placeholder_text='Input Name', text_color='black', font=('Times New Roman', 10), height=30, width=480, fg_color='white')
nameEntry.grid(row=1, column=0, padx=10, pady=(0,10))

# Password input bubble
passwordEntry = CTkEntry(inputFrame,placeholder_text='Input Password', text_color='black',font=('Times New Roman', 10), height=30, width=480, fg_color='white', show='*')
passwordEntry.grid(row=2, column=0, padx=10, pady=(0,10))

# Button to click for when the password is forgotten
forgot_label = CTkButton(inputFrame, text='Forgot Password?', width=180, cursor='hand2', text_color='black', fg_color='white', hover_color='white', command=toobad)
forgot_label.grid(row=3, column=0, sticky='e')

# Button to Submit whatever is in the name or password bubbles
buttonSubmit = CTkButton(inputFrame, text='Confirm', width=380, cursor='hand2', command=login)
buttonSubmit.grid(row=4, column=0)

# keeps the window open for as long as it is not exited out of
signup_window.mainloop()