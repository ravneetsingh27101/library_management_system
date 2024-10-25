import sqlite3
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox, simpledialog


def create_database():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )"""
    )

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        isbn TEXT NOT NULL,
        available INTEGER NOT NULL
    )"""
    )

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS BorrowedBooks (
        borrow_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        book_id INTEGER,
        borrow_date TEXT,
        return_date TEXT,
        returned INTEGER,
        FOREIGN KEY (user_id) REFERENCES Users(user_id),
        FOREIGN KEY (book_id) REFERENCES Books(book_id)
    )"""
    )

    conn.commit()
    conn.close()


def insert_sample_data():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    books = [
        ("To Kill a Mockingbird", "Harper Lee", "978-0061120084", 1),
        ("1984", "George Orwell", "978-0451524935", 1),
        ("The Great Gatsby", "F. Scott Fitzgerald", "978-0743273565", 1),
        ("The Catcher in the Rye", "J.D. Salinger", "978-0316769488", 1),
        ("Pride and Prejudice", "Jane Austen", "978-1503290563", 1),
    ]

    cursor.executemany(
        """INSERT INTO Books (title, author, isbn, available)
                          VALUES (?, ?, ?, ?)""",
        books,
    )

    conn.commit()
    conn.close()


create_database()
insert_sample_data()


class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("400x400")
        self.root.configure(bg="#f0f8ff")

        self.main_frame = tk.Frame(self.root, bg="#f0f8ff")
        self.main_frame.pack(pady=20)

        self.user_frame = tk.Frame(self.main_frame, bg="#f0f8ff")

        self.show_main_menu()

    def show_main_menu(self):
        self.clear_frame(self.main_frame)
        tk.Label(
            self.main_frame,
            text="Library Management System",
            font=("Helvetica", 18, "bold"),
            bg="#f0f8ff",
            fg="#4b0082",
        ).pack(pady=10)

        tk.Button(
            self.main_frame,
            text="Register",
            command=self.show_register_menu,
            bg="#add8e6",
            fg="#000080",
            font=("Helvetica", 12),
        ).pack(pady=10, fill="x")
        tk.Button(
            self.main_frame,
            text="Login",
            command=self.show_login_menu,
            bg="#add8e6",
            fg="#000080",
            font=("Helvetica", 12),
        ).pack(pady=10, fill="x")
        tk.Button(
            self.main_frame,
            text="Exit",
            command=self.root.quit,
            bg="#ff7f50",
            fg="#ffffff",
            font=("Helvetica", 12),
        ).pack(pady=10, fill="x")

    def show_register_menu(self):
        self.clear_frame(self.main_frame)
        tk.Label(
            self.main_frame,
            text="Register",
            font=("Helvetica", 16, "bold"),
            bg="#f0f8ff",
            fg="#4b0082",
        ).pack(pady=10)

        tk.Label(self.main_frame, text="Username", bg="#f0f8ff").pack(pady=5)
        self.reg_username = tk.Entry(self.main_frame)
        self.reg_username.pack(pady=5)

        tk.Label(self.main_frame, text="Password", bg="#f0f8ff").pack(pady=5)
        self.reg_password = tk.Entry(self.main_frame, show="*")
        self.reg_password.pack(pady=5)

        tk.Button(
            self.main_frame,
            text="Register",
            command=self.register_user,
            bg="#90ee90",
            font=("Helvetica", 12),
        ).pack(pady=10)
        tk.Button(
            self.main_frame,
            text="Back",
            command=self.show_main_menu,
            bg="#ff7f50",
            fg="#ffffff",
            font=("Helvetica", 12),
        ).pack(pady=5)

    def show_login_menu(self):
        self.clear_frame(self.main_frame)
        tk.Label(
            self.main_frame,
            text="Login",
            font=("Helvetica", 16, "bold"),
            bg="#f0f8ff",
            fg="#4b0082",
        ).pack(pady=10)

        tk.Label(self.main_frame, text="Username", bg="#f0f8ff").pack(pady=5)
        self.login_username = tk.Entry(self.main_frame)
        self.login_username.pack(pady=5)

        tk.Label(self.main_frame, text="Password", bg="#f0f8ff").pack(pady=5)
        self.login_password = tk.Entry(self.main_frame, show="*")
        self.login_password.pack(pady=5)

        tk.Button(
            self.main_frame,
            text="Login",
            command=self.login_user,
            bg="#90ee90",
            font=("Helvetica", 12),
        ).pack(pady=10)
        tk.Button(
            self.main_frame,
            text="Back",
            command=self.show_main_menu,
            bg="#ff7f50",
            fg="#ffffff",
            font=("Helvetica", 12),
        ).pack(pady=5)

    def show_user_menu(self, user_id):
        self.clear_frame(self.user_frame)
        self.user_id = user_id
        tk.Label(
            self.user_frame,
            text="User Menu",
            font=("Helvetica", 16, "bold"),
            bg="#f0f8ff",
            fg="#4b0082",
        ).pack(pady=10)

        tk.Button(
            self.user_frame,
            text="Display Available Books",
            command=self.display_books,
            bg="#add8e6",
            fg="#000080",
            font=("Helvetica", 12),
        ).pack(pady=5, fill="x")
        tk.Button(
            self.user_frame,
            text="Borrow a Book",
            command=self.borrow_book,
            bg="#add8e6",
            fg="#000080",
            font=("Helvetica", 12),
        ).pack(pady=5, fill="x")
        tk.Button(
            self.user_frame,
            text="Return a Book",
            command=self.return_book,
            bg="#add8e6",
            fg="#000080",
            font=("Helvetica", 12),
        ).pack(pady=5, fill="x")
        tk.Button(
            self.user_frame,
            text="Check Borrowed Books",
            command=self.check_borrowed_books,
            bg="#add8e6",
            fg="#000080",
            font=("Helvetica", 12),
        ).pack(pady=5, fill="x")
        tk.Button(
            self.user_frame,
            text="Logout",
            command=self.show_main_menu,
            bg="#ff7f50",
            fg="#ffffff",
            font=("Helvetica", 12),
        ).pack(pady=10, fill="x")

        self.user_frame.pack(pady=20)

    def clear_frame(self, frame):
        for widget in self.main_frame.winfo_children():
            widget.pack_forget()
        frame.pack()

    def register_user(self):
        username = self.reg_username.get()
        password = self.reg_password.get()

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Users (username, password) VALUES (?, ?)",
                (username, password),
            )
            conn.commit()
            messagebox.showinfo("Success", "Registration successful!")
            self.show_main_menu()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")
        finally:
            conn.close()

    def login_user(self):
        username = self.login_username.get()
        password = self.login_password.get()

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_id FROM Users WHERE username = ? AND password = ?",
            (username, password),
        )
        user = cursor.fetchone()

        if user:
            messagebox.showinfo("Success", f"Welcome, {username}!")
            self.show_user_menu(user[0])
        else:
            messagebox.showerror("Error", "Invalid username or password.")

        conn.close()

    def display_books(self):
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Books WHERE available = 1")
        available_books = cursor.fetchall()
        conn.close()

        book_window = tk.Toplevel(self.root)
        book_window.title("Available Books")

        canvas = tk.Canvas(book_window)
        scrollbar = tk.Scrollbar(book_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for book in available_books:
            book_label = tk.Label(
                scrollable_frame,
                text=f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}",
                bg="#f0f8ff",
                fg="#000080",
            )
            book_label.pack(pady=2)

        if not available_books:
            messagebox.showinfo("Available Books", "No books available at the moment.")

    def borrow_book(self):
        book_id = simpledialog.askinteger("Borrow Book", "Enter Book ID:")
        if book_id:
            conn = sqlite3.connect("library.db")
            cursor = conn.cursor()
            cursor.execute("SELECT available FROM Books WHERE book_id = ?", (book_id,))
            book = cursor.fetchone()

            if book and book[0] == 1:
                borrow_date = datetime.now().strftime("%Y-%m-%d")
                return_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
                cursor.execute(
                    "INSERT INTO BorrowedBooks (user_id, book_id, borrow_date, return_date, returned) VALUES (?, ?, ?, ?, ?)",
                    (self.user_id, book_id, borrow_date, return_date, 0),
                )
                cursor.execute(
                    "UPDATE Books SET available = 0 WHERE book_id = ?", (book_id,)
                )
                conn.commit()
                messagebox.showinfo("Success", "Book borrowed successfully!")
            elif book and book[0] == 0:
                messagebox.showwarning("Warning", "Book is not available.")
            else:
                messagebox.showerror("Error", "Book not found.")
            conn.close()

    def return_book(self):
        book_id = simpledialog.askinteger("Return Book", "Enter Book ID:")
        if book_id:
            conn = sqlite3.connect("library.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM BorrowedBooks WHERE user_id = ? AND book_id = ? AND returned = 0",
                (self.user_id, book_id),
            )
            borrowed_book = cursor.fetchone()

            if borrowed_book:
                cursor.execute(
                    "UPDATE BorrowedBooks SET returned = 1 WHERE borrow_id = ?",
                    (borrowed_book[0],),
                )
                cursor.execute(
                    "UPDATE Books SET available = 1 WHERE book_id = ?", (book_id,)
                )
                conn.commit()
                messagebox.showinfo("Success", "Book returned successfully!")
            else:
                messagebox.showwarning(
                    "Warning",
                    "You haven't borrowed this book or it was already returned.",
                )
            conn.close()

    def check_borrowed_books(self):
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT Books.title, Books.author, BorrowedBooks.borrow_date, BorrowedBooks.return_date FROM BorrowedBooks INNER JOIN Books ON BorrowedBooks.book_id = Books.book_id WHERE BorrowedBooks.user_id = ? AND BorrowedBooks.returned = 0",
            (self.user_id,),
        )
        borrowed_books = cursor.fetchall()
        conn.close()

        if borrowed_books:
            borrowed_window = tk.Toplevel(self.root)
            borrowed_window.title("Borrowed Books")
            for book in borrowed_books:
                tk.Label(
                    borrowed_window,
                    text=f"Title: {book[0]}, Author: {book[1]}, Borrowed on: {book[2]}, Return by: {book[3]}",
                    bg="#f0f8ff",
                ).pack(pady=5)
        else:
            messagebox.showinfo("Borrowed Books", "You have no borrowed books.")


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
