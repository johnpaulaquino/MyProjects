Project Challenge: Library Management System
Requirements:
Classes:

Book: Represents a book in the library.
Attributes: title, author, ISBN, status (available/checked out).
Methods: check_out(), return_book(), display_info().
Member: Represents a library member.
Attributes: name, member_id, list of checked-out books.
Methods: check_out_book(book), return_book(book), display_checked_out_books().

Library: Represents the library itself.
Attributes: list of books, list of members.
Methods: add_book(book), register_member(member), find_book_by_title(title), display_all_books().

Relationships:

A Library contains multiple Books and Members.
A Member can check out multiple Books, but a Book can only be checked out by one Member at a time.
Additional Features (optional but encouraged):

Implement a system to handle overdue books.
Allow members to reserve books that are currently checked out.
Add a simple user interface (CLI) for interaction.
Guidelines:
Focus on encapsulation by using private attributes where appropriate.
Use inheritance if you want to create specialized types of books or members (e.g., eBooks, premium members).
Think about how you can make your code reusable and maintainable.
Consider error handling for actions like checking out a book that's already checked out.
Deliverables:
Define your class structures and methods.
Write a brief explanation of how OOP principles (encapsulation, inheritance, polymorphism) are applied in your project.
Optionally, create a few test cases to demonstrate the functionality.
This project will allow you to apply your knowledge of OOP concepts and design a system that’s both functional and organized. Good luck, and have fun coding!
