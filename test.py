import tkinter as tk
from tkinter import *
from customtkinter import *
from tkinter import messagebox

signup_window = tk.Tk()
signup_window.title("Cash Register App")
signup_window.resizable(0,0)
signup_window.geometry('500x400+300+100')
signup_window.configure(background = 'white')

def quit_logout():
    global bottomFrame
    
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
    
    menu_label = tk.Label(menuFrame, text= f'Welcome!', font=('Times New Roman', 20, 'bold'), background='white')
    menu_label.grid(row=0, column=0, pady=(20,0), columnspan=2)
    
    # menu buttons for the different classes
    menu1Button = CTkButton(menuFrame, text='Club1', width=210, cursor='hand2')
    menu1Button.grid(row=1, column=0, pady=(20,0), padx=20)

    menu1Button = CTkButton(menuFrame, text='Club2', width=210, cursor='hand2')
    menu1Button.grid(row=1, column=1, pady=(20,0), padx=20)

    menu1Button = CTkButton(menuFrame, text='Club3', width=210, cursor='hand2')
    menu1Button.grid(row=2, column=0, pady=(20,0), padx=20)

    menu1Button = CTkButton(menuFrame, text='Club4', width=210, cursor='hand2')
    menu1Button.grid(row=2, column=1, pady=(20,0), padx=20)

    quit_logout()

def login_page():
    menuFrame.grid_forget()
    bottomFrame.grid_forget()
    loginFrame.grid(row=0, column=0, sticky='nsew')

#Page of the login
loginFrame = CTkFrame(signup_window, fg_color='white')
loginFrame.grid(row=0, column=0, sticky='nsew')

#Exit button to be on every site
buttonQuit = CTkButton(loginFrame, 
                       text='Quit', text_color='black', fg_color='white', hover_color='white', cursor='hand2',
                       width=30, 
                       command=signup_window.destroy)
buttonQuit.grid(row=1, column=0, pady=(20,0), sticky='s')

# The Login stuff
inputFrame = CTkFrame(loginFrame, fg_color='white')
inputFrame.grid(row=0, column=0)
inputFrame.configure()

input_label = tk.Label(inputFrame, text='Log in to proceed', font=('Times New Roman', 20, 'bold'), background='white')
input_label.grid(row=0, column=0, pady=20)

nameEntry = CTkEntry(inputFrame,placeholder_text='Input Name', text_color='black', font=('Times New Roman', 10), height=30, width=480, fg_color='white')
nameEntry.grid(row=1, column=0, padx=10, pady=(0,10))


passwordEntry = CTkEntry(inputFrame,placeholder_text='Input Password', text_color='black',font=('Times New Roman', 10), height=30, width=480, fg_color='white', show='*')
passwordEntry.grid(row=2, column=0, padx=10, pady=(0,10))

buttonSubmit = CTkButton(inputFrame, text='Confirm', width=380, cursor='hand2', command=signup_user)
buttonSubmit.grid(row=3, column=0)





signup_window.mainloop()