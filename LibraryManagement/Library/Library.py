import bcrypt
class Library:
    def __init__(this):
        this.__list_users = []
        this.__list_books =[]
        this.__current_user = []
    
    def register_user(this, user):
        this.__list_users.append(user)
    
    def add_books(this, books):
        this.__list_books.append(books)
        
    def get_currentUser(this):
        user = filter(lambda user: user, this.__current_user)
        for users in user:
            return users
    
    def display_users(this) -> str:
        for user in this.__list_users:
            print(user)
        
    def display_books(this) -> str:
        for books in this.__list_books:
            print(books)
    
    def find_book(this, title):
        filtered = next(filter(lambda book: book.get_title() == title, this.__list_books),None)
        return filtered if filtered else "Book not found"
    
    def login(this, email, password):
        
        #filter the list that match with the email and password before logging in
        filtered = list(filter(lambda user: user.get_email() == email 
        and bcrypt.checkpw(password.encode('utf-8'), user.get_password()),this.__list_users))
        
        this.__current_user.append(filtered)
        
        return filtered
    
    def log_out(this):
        this.__current_user.pop()
        