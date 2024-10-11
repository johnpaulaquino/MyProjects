from datetime import datetime , timedelta
class Book:
   
    def __init__(this, title, author,isbn, status):
        this.__title = title
        this.__author = author
        this.__isbn = isbn
        this.__status = status
        this.__duedate = ''
        this.__checkout_by = ''
    
    
    # Getters
    def get_title(this):
        return this.__title
    def get_author(this):
        return this.__author
    def get_isbn(this):
        return this.__isbn
    def get_status(this):
        return this.__status
    def get_duedate(this):
        return this.__duedate
    def get_checkout_by(this):
        return this.__checkout_by
        
    
    #Setters
    def set_title(this, title):
        this.__title = title
    def set_author(this, author):
        this.__author = author
    def set_isbn(this, isbn):
        this.__isbn = isbn
    def set_status(this, status):
        this.__status = status
    def set_duedate(this, duedate):
        this.__duedate = duedate
    def set_checkout_by(this, id):
        this.__checkout_by = id
        
    #String method
    def __str__(this) -> str:
        isDue = '' if this.__duedate == '' else f"Duedate: {this.__duedate}" 
        return f"Title: {this.__title}\nAuthor: {this.__author}\nISBN: {this.__isbn}\nstatus: {this.__status}\n{isDue}"
    
    
    
    #Books Functions
    def checkout(this) -> bool:
        if this.__status == "Available".lower() or this.__status == "Available".capitalize():
            return True
        else:
            return False
    
    
    def return_book(this):
        this.__status == "Available"
        
    def checkout_by(this) -> str:
        return f"Checkout by: {this.__checkout_by}"