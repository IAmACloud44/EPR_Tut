import tkinter as tk
from customtkinter import *
from PIL import Image
from tkinter import messagebox
from database import *
from teamwork import *
import csv

# # The window set ups
signup_window = tk.Tk()
signup_window.title("Cash Register App")
signup_window.resizable(0,0)
signup_window.geometry('500x400+300+100')
signup_window.configure(background = 'white')


# # The window part fucntions
def quit_logout():
    '''A custom Quit button next to a LogOut button to put underneath all other windows but the login'''
    
    # input variable buttomFrame
    global bottomFrame
    
    # create 
    bottomFrame = CTkFrame(signup_window, fg_color='white')
    bottomFrame.grid(row=1, column=0, sticky='s')
    
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


def menu():
    '''
    Function to create the choice of what Clubs to manage
    '''
    global menuFrame
    #deletes the login page, but not the quit button
    loginFrame.grid_forget()
    
    #new Frame created
    menuFrame = CTkFrame(signup_window, fg_color='white')
    menuFrame.grid(row=0, column=0, sticky='nsew')
    
    menu_label = tk.Label(menuFrame, text= f'Welcome {nameEntry.get()}!', font=('Times New Roman', 20, 'bold'), background='white')
    menu_label.grid(row=0, column=0, pady=(20,0), columnspan=2)
    
    # menu buttons for the different classes
    menu1Button = CTkButton(menuFrame, text='Football', width=210, cursor='hand2')
    menu1Button.grid(row=1, column=0, pady=(20,0), padx=20)

    menu1Button = CTkButton(menuFrame, text='Hiking', width=210, cursor='hand2')
    menu1Button.grid(row=1, column=1, pady=(20,0), padx=20)

    menu1Button = CTkButton(menuFrame, text='Club3', width=210, cursor='hand2')
    menu1Button.grid(row=2, column=0, pady=(20,0), padx=20)

    menu1Button = CTkButton(menuFrame, text='Club4', width=210, cursor='hand2')
    menu1Button.grid(row=2, column=1, pady=(20,0), padx=20)

    quit_logout()


def login_page():
    '''Loads in the login page upon loging out'''
    for widget in signup_window.winfo_children():  # Get all widgets in the window
        if isinstance(widget, CTkFrame):  # Check if it's a Frame
            widget.grid_forget()

    loginFrame.grid(row=0, column=0, sticky='nsew') # reframes and makes the login page appear

    nameEntry.delete(0, "end")  # Clears the name in the login
    passwordEntry.delete(0, "end")  # Clears the password in the login


def admin_addition():
    '''adds the functions that admins can do to the menu'''
    global adminFrame
    
    adminFrame = CTkFrame(menuFrame, fg_color='white')
    adminFrame.grid(row=3, column=0, pady=20, columnspan=2)
    
    addClub = CTkButton(adminFrame, text='Add a Club', width=210, cursor='hand2', command=add_club)
    addClub.grid(row=0, column=0, pady=(20,0), padx=20)
    printStat = CTkButton(adminFrame, text='Print Statement', width=210, cursor='hand2')
    printStat.grid(row=0, column=1, pady=(20,0), padx=20)
    

def treas_addition():
    '''adds the functions that treasurers can do to the menu'''
    treasFrame = CTkFrame(menuFrame, fg_color='white')
    treasFrame.grid(row=3, column=0, pady=20, columnspan=2)
    
    withdraw_transer = CTkButton(treasFrame, text='Issue Finances', width=210, cursor='hand2')
    withdraw_transer.grid(row=0, column=0, pady=(20,0), padx=20)
    view_history = CTkButton(treasFrame, text='View History', width=210, cursor='hand2', command=Treasurer.view_transaction_history)
    view_history.grid(row=0, column=1, pady=(20,0), padx=20)
    

def finofficer_addition():
    '''adds the functions that financial officers can do to the menu'''
    treasFrame = CTkFrame(menuFrame, fg_color='white')
    treasFrame.grid(row=3, column=0, pady=20, columnspan=2)
    
    view_status = CTkButton(treasFrame, text='View Status', width=210, cursor='hand2')
    view_status.grid(row=0, column=0, pady=(20,0), padx=20)


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


# # The functionalities in the windows
def check_role():
    '''reads the role and department of the person logged in and directs them to their individual page'''
    
    role, department = login_check(csv_file = 'users.csv')
    #user page
    if role == 'user':
        user_page()
    # treasurer page
    if role == 'treasurer':
        menu()
        treas_addition()
    # financial officer page
    if role == 'finofficer':
        menu()
        admin_addition()
    # admin page
    if role == 'admin':
        menu()
        admin_addition()

    return department


def login_check(csv_file):
    '''Checks the login data, whether the person loging in is in the list or not'''
    with open(csv_file, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            if len(row)<5:
                continue
            if row[1] == nameEntry.get() and row[2] == passwordEntry.get():
                return row[3], row[4]
    return False


def login():
    '''The function of the 'submit button', it checks what is in the input bubbles and:
    - rejects non filled bubbles
    - verifies the login data and lets people into the menu OR
    - tell you that you did a mistake
    '''

    csv_file = 'users.csv'

    # Empty bubble checks
    if nameEntry.get() == '' or passwordEntry.get() == '':
        messagebox.showerror('Alert', 'Fill in both inputs.')
    # actual login check    
    elif login_check(csv_file):
        check_role()
    # tells you that you did a mistake
    else:
        messagebox.showerror('Alert', 'Wrong Login or Password')


def toobad():
    '''Pop up for the forget password option'''
    messagebox.showerror('LMAO', 'too bad')
    

def add_club():
    global addFrame
    global clubinput
    global moneyinput

    for widget in signup_window.winfo_children():
        if isinstance(widget, CTkFrame):
            widget.grid_forget()
    
    quit_logout()
    
    addFrame = CTkFrame(signup_window, fg_color='white', width=500)
    addFrame.grid(row=0, column=0)
    
    clubinputLabel = CTkLabel(addFrame, text='Input a Name for the new club:', text_color='black', width=200)
    clubinputLabel.grid(row=0, column=0, pady=20, padx=20, sticky='w')
    clubinput = CTkEntry(addFrame, fg_color='white', width=200, text_color='black')
    clubinput.grid(row=0, column=1)
    
    moneyinputLabel = CTkLabel(addFrame, text='Input a starting € amount for the the club:', text_color='black', width=200)
    moneyinputLabel.grid(row=1, column=0, pady=20, padx=20, sticky='w')
    moneyinput = CTkEntry(addFrame, fg_color='white', width=200, text_color='black')
    moneyinput.grid(row=1, column=1)
    
    # Button to Submit whatever is in the name or password bubbles
    buttonSubmit = CTkButton(addFrame, text='Submit', width=150, cursor='hand2', command=add_club_button)
    buttonSubmit.grid(row=4, column=1, columnspan = 2, sticky='e')
    buttonBack = CTkButton(addFrame, text='Back', width=150, cursor='hand2', command=lambda: (menu(), admin_addition()))
    buttonBack.grid(row=4, column=0, columnspan = 2, sticky='w', padx=20)
    

def add_club_button():
    club = clubinput.get()
    try:
        money = int(moneyinput.get())
        money = float(moneyinput.get())
        print(money)
    except:
        messagebox.showerror('Alert', 'Invalid Input')
    if money < 0 or money < 0.0:
        messagebox.showerror('Alert', f'Don\'t take up loans you cannot pay')
        return
    try:
        if club == '' or money == '':
            messagebox.showerror('Alert', 'Please fill in all bubbles')
        else:
            club = Account(club, int(money))
            print(club.balance)
            messagebox.showinfo('Success', f'Successfully created {clubinput.get()}')
            moneyinput.delete(0, "end")  # Clears the name in the login
            clubinput.delete(0, "end")  # Clears the password in the login
    except:
        messagebox.showerror('Alert', 'This is not a monetary sum')
    



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