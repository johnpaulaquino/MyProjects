from Book.Book import Book
from User.Member import Member
from Library.Library import Library



libray = Library()

list= []
member = Member("Paul", "asdasd", "Asdasdsad","asdasdasd")
member1 = Member("Paul", "asdasd", "asd","assssasd")

list.append(member)
list.append(member1)
email = 'Asdasdsad'
password = 'asdasdasd'

filteresdd = filter(lambda user : user.get_email() == email 
                 and user.get_password() == password, list)

print(filteresdd)
for i in filteresdd:
    print(i)
    print(i.get_memberId())