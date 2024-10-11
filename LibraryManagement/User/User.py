import uuid
class User:
    
    def __init__(this, fname, lname,email,password):
        unique_id = uuid.uuid4()
        this.__fname = fname
        this.__lname = lname
        this.__member_id = unique_id
        this.__email = email
        this.__password = password
        
        
        # Getters
    def get_firstname(this):
        return this.__fname
    def get_lastname(this):
        return this.__lname
    def get_memberId(this):
        return this.__member_id
    def get_email(this):
        return this.__email
    def get_password(this):
        return this.__password
    
    #Setters
    def set_firstname(this,firstname):
        this.__title = firstname
    def set_lastname(this,lastname):
        this.__lname = lastname
    def set_email(this,email):
        this.__email = email
    def set_password(this,password):
        this.__password = password
        
    

    def __str__(this):
        return f"Member Id: {this.__member_id}\nFirstname: {this.__fname}\nLastname: {this.__lname}\nEmail: {this.__email}\n"