
import sys
import os
import json
import bcrypt

# Add the parent directory (project root) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from LibraryManagement.Library.Library import Library

from LibraryManagement.User.Member import Member
from LibraryManagement.Book.Book import Book
from utils.validation import password_validation as validation


def login_logs(library):
    from datetime import datetime #Import the time 
    file_loc = os.path.join(os.getcwd(), 'LibraryManagement','data', '.log') # Get the location of the .log file
    today = datetime.today().strftime('%Y-%d-%m, %H:%M:%S') #Get the date and time today
    username = library.get_currentUser() # get the current user 
    for i in username: # ITerate the current user and get its id
        id = i.get_memberId()
    data = f'User {id} has successfully login, at s{today}.' #this will be the logs every time the user login
    
    try: # this will catch the error if there is a problem encounter
        with open(file_loc, 'a+') as file:
            file.seek(0) # it will seek in the top of the file
            file.write('\n') # Every time there is data need to insert, it will make a new line
            file.write(data) # appending the data into the file
    except Exception as e:
        print(f"{e}") # display the error if there is.

def hash_password(password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14)) 
    
    return hashed

def signup(library):
    while True:
        fname = input("Enter your firstname: ")
        lastname = input("Enter your lastname: ")
        email = input("Enter your email: ")
        password = input("Enter your password")

        if validation(password):
            password_hash = hash_password(password)
            member = Member(fname, lastname, email, password_hash)
            library.register_user(member)
            print('Successfully Created Account! ')
            
        else:
            print("Invalid Password")

def login(library):
    email = input("enter your email: ")
    password = input("Enter your password: ")
    
    result = library.login(email, password)
    if len(result) != 0:
        print('Successfully Log in!')
    else:
        print('Failed to Log in!')
        
def batch_register(library):
    json_file_path = os.path.join(os.getcwd(),'LibraryManagement','data', 'users.json')
    try:
        with open(json_file_path, 'r') as info:
            data = json.load(info)
        for users in data:
            if users:
                password = hash_password(users['password'])
                member = Member(users['fname'], users["lname"], users['email'], password)
                library.register_user(member)
        print('Successfully registered all users!')
    except Exception as filError:
        print(f"No directory {json_file_path}. Please Check your Directories")

def menu():
    print("Welcome to Library!")
    
    print("Do You have an Account? (1)Yes (2)No: ")
    while True:
        try:
            choice = int(input("Enter your Choice: "))
            if choice in [1,2]:
                return choice
            else:
                print("Please choice 1 and 2 only!")
        except Exception as e:
            print("You must enter Integer")



library = Library()
user = Member('Paul', 'a', 'asd', 'asdasd')

batch_register(library)

library.display_users()

choice = menu()
if choice == 1:
    login(library)
    
else:
    signup(library)
    login(library)


