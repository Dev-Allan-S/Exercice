import json

class Library:
    def __init__(self):
        self.library = []
        self.load_books()

    def add_book(self, book):
        a = self.find_book(book.b_name, book.author)
        if a:
            print("This book already in library")
        else:
            self.library.append(book)
            self.save_books()

    def list_book(self):
        count = 0
        for book in self.library:
            count+=1
            print(f"N:{count}, Id:{book.b_id} Book:{book.b_name}, Author:{book.author}, Borrowed:{book.borrowed} ")

    def find_book(self, book_name, author):
        for book in self.library:
            if book.b_name==book_name and book.author==author:
                return book
        return None

    def delete_book(self, book_name, book_author):
        a = self.find_book(book_name, book_author)
        if a:
            self.library.remove(a)
            print("Book deleted")
            self.save_books()
        else:
            print("Book not found")

    def borrow_book(self, book_name, book_author):
        b = self.find_book(book_name, book_author)
        if b:
            if b.borrow_book():
                print("Good reading")
                self.save_books()
            else:
                print("Sorry this book already borrowed")
        else:
            print("Sorry, book not found")

    def return_book(self, book_name, book_author):
        b = self.find_book(book_name, book_author)
        if b:
            if b.return_book():
                print("Liked your reading")
                self.save_books()
            else:
                print("This book, isn't mine")
        else:
            print("Sorry, book not found")

    def save_books(self):
        books_data = []
        for book in self.library:
            books_data.append(book.__dict__)
        with open("library.json", "w") as library_json_file:
            library_json_file.write(json.dumps({"books":books_data}, indent=4))
    
    def load_books(self):
        try:
            with open("library.json", "r") as l_books:
                books = json.load(l_books)
            self.library = Book.prepare_books(books["books"])
            
        except json.decoder.JSONDecodeError:
            print("Db empty, please add some book")

        except FileNotFoundError:
            print("Db not found")

    def __str__(self):
        return f"{self.library}"

class Book:
    b_id=1
    def __init__(self, b_name, author, borrowed=False, b_id=None):
        self.b_name=b_name
        self.author=author
        self.borrowed=borrowed
        if b_id is not None and isinstance(b_id, int) and b_id > 0:
            self.b_id=b_id
        else:
            self.b_id=Book.b_id
            Book.b_id +=1

    @classmethod
    def load_book(cls, book):
        return cls(
            book["b_name"],
            book["author"],
            book["borrowed"],
            book["b_id"]
        )
    
    def borrow_book(self):
        if self.borrowed==False:
            self.borrowed=True
            return True
        else:
            return False

    def return_book(self):
        if self.borrowed==True:
            self.borrowed=False
            return True
        else:
            return False

    @staticmethod
    def prepare_books(list_book):
        load_books = []
        for book in list_book:
            b=Book.load_book(book)
            load_books.append(b)
        highest_id=Book.find_highest_id(load_books)
        Book.b_id=highest_id
        books = Book.fix_id(load_books)
        return books

    @staticmethod
    def find_highest_id(list_book):
        highest_id=0
        for book_id in list_book:
            if book_id.b_id>=highest_id:
                highest_id=book_id.b_id
        return highest_id+1

    @staticmethod
    def fix_id(book):
        temp_id = []
        fix_book=[]
        for b in book:
            if b.b_id in temp_id:
                b.b_id=Book.b_id
                Book.b_id+=1
            fix_book.append(b)
            temp_id.append(b.b_id)
        return fix_book

    def __str__(self):
        return f"{self.b_id}, {self.b_name}, {self.author}, {self.borrowed}"

    def __repr__(self):
        return self.__str__()

library=Library()

library.save_books()