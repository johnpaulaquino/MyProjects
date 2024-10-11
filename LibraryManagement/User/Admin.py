import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from LibraryManagement.User.User import User
from LibraryManagement.Library.Library import Library

class Admin(User):
   
    def __init__(this, fname, lname, email, password):
        super().__init__(fname, lname, email, password)
        this.__library = Library()
        this.__type = 'Admin'
    def add_book(this, book):
        this.__library.add_books(book)
    
    def add_user(this, user):
        this.__library.register_user(user)
    
    def update_user_info(this):
        pass
    
    def get_books(this):
        return this.__books
    
    def get_users(this):
        return this.__users
    
    def get_type(this):
        return this.__type
    


