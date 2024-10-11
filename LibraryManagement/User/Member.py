from LibraryManagement.User.User import User
from datetime import datetime, timedelta
class Member(User):
    def __init__(this, fname, lname, email, password):
        this.__checkout_books = []
        super().__init__(fname, lname, email, password)
        this.__type = 'Member'
        
        
    #getters
    def get_checkout_date(this):
        return this.__checkout_time
    
    def getDuedate(this):
        return this.__duedate
    
    def get_type(this):
        return this.__type
    
    #Functions
    def checkout_book(this, book):
        today = datetime.today().strftime("%Y-%m-%d")
        object_date = datetime.strptime(today, "%Y-%m-%d")
        duedate = (object_date + timedelta(days=10)).strftime("%Y-%m-%d")
        if book.checkout():
            book.set_duedate(duedate)
            book.set_checkout_by(this.get_memberId())
            this.__checkout_books.append(book)
            print("Successfully checkout!")
        else:
            print("Sorry, this book is unavailable!")
        

    def display_my_books(this):
        for book in this.__checkout_books:
            print(book)
    
    