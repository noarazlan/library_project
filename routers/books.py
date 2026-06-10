import sqlite3
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Initialize Jinja2 templates directory for rendering HTML files
templates = Jinja2Templates(directory="templates")

# Create an APIRouter instance to group book-related endpoint
router = APIRouter(
    prefix="/books",
    tags=["books"]
)

# Route to serve the initial HTML search page (Keep only ONE get route for "/")
@router.get("/", response_class=HTMLResponse)
async def get_search_page(request: Request):
    # Render the search form, setting both error and recommended_books to None initially
    return templates.TemplateResponse(
        request=request, 
        name="search_book.html", 
        context={"request": request, "error": None, "recommended_books": None}
    )

# Route to handle the form submission and search for the book
@router.post("/search", response_class=HTMLResponse)
async def search_book(request: Request, book_name: str = Form(...)):
    try:
        # Establish a connection to the SQLite database
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()

        search_book = f"%{book_name.strip()}%"

        # Secure SQL query using parameterized input to prevent SQL Injection
        query = "SELECT * FROM Books WHERE LOWER(title) like LOWER(?);"
        cursor.execute(query, (search_book,))
        
        # Fetch the first matching row
        book_found = cursor.fetchall()
        #conn.close()

        # Check if the book was not found in the database
        if not book_found:
            # Re-render the search page with an error message, explicitely setting recommended_books to None
            return templates.TemplateResponse(
                request=request, 
                name="search_book.html", 
                context={"request": request, "error": f"The book '{book_name}' does not exist in our library.", "recommended_books": None}
            )
        
        return templates.TemplateResponse(request=request, name="search_results.html", context={"request":request, "books":book_found, "search_text":book_name})
    
    
       
    except Exception as e:
        print(f"Server Error: {e}")
        return templates.TemplateResponse(
            request=request, 
            name="search_book.html", 
            context={"request": request, "error": "An error occurred on the server.", "recommended_books": None}
        )
   



@router.post("/details" , response_class=HTMLResponse)
async def book_details(request:Request, book_id:int = Form()):

    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    cursor.execute("select * from Books where id = ?",(book_id,))

    book_found = cursor.fetchone()


    if book_found is None:
        conn.close()
        return templates.TemplateResponse(
                request=request, 
                name="search_book.html", 
                context={"request": request, "error": "Book not found", "recommended_books": None}
            )
    

    cursor.execute("select * from Loans where book_id = ? and actual_return_date is Null",(book_id,))

    active_loan = cursor.fetchone()
        
    conn.close()

    is_available = True if active_loan is None else False

    # Map the database columns to a context dictionary for Jinja2
    book_context = {
        "request": request,
        "title": book_found[1],
        "book_id": book_found[0],
        "author": book_found[2],
        "summary": book_found[3],
        "category": book_found[4],
        "price": book_found[5],
        "rating": book_found[6],
        "is_available": is_available
        }    
        # Successfully found the book; render the dynamic details page
    return templates.TemplateResponse(request=request, name="book_details.html", context=book_context)
        








@router.post("/search-author", response_class=HTMLResponse)
async def search_author(request:Request, author_name: str = Form()):

    search_author = f"%{author_name.strip()}%"
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    cursor.execute("select * from Books where lower(author) like lower(?)", (search_author,))
    author = cursor.fetchall()
    conn.close()

    if not author:
        return templates.TemplateResponse(
            request=request, 
            name="search_book.html", 
            context={"request": request, "error": f"The author '{search_author}' does not exist in our library.", "recommended_books": None}
        )
    
    return templates.TemplateResponse(request=request, name="author.html", context={"request":request, "author_name":author_name, "books":author})






# Route to get and display recommended books on the same page
@router.get("/recommended", response_class=HTMLResponse)
async def get_recommended_books(request: Request):
    try:
        # Establish a connection to the SQLite database
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()

        # Query to fetch top 10 books
        query = "SELECT title, rating FROM Books ORDER BY rating DESC LIMIT 10;"
        cursor.execute(query)
        recommended = cursor.fetchall()
        conn.close()
        
        # Render the SAME search page, but this time pass the recommended books list
        return templates.TemplateResponse(
            request=request, 
            name="search_book.html", 
            context={"request": request, "error": None, "recommended_books": recommended}
        )

    except Exception as e:
        print(f"Server Error: {e}")
        return templates.TemplateResponse(
            request=request, 
            name="search_book.html", 
            context={"request": request, "error": "Could not load recommendations.", "recommended_books": None}
        )
    
# Handles joining the waitlist and calculating the return date 
@router.post("/waitlist", response_class=HTMLResponse)
async def join_waitlist(request: Request, book_id: int = Form(...)):
    try:
        from datetime import datetime, timedelta
        
        # Check user authentication via browser cookies
        user_id_str = request.cookies.get("id_user")

        if not user_id_str:
            return "Error: You must be logged in to join the waitlist."
        
        id_user_connected = int(user_id_str)

        # Connect to the SQLite database
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()

        # Check if the user is already in the waitlist for this specific book
        cursor.execute("SELECT * FROM Waitlist WHERE book_id = ? AND id_user = ?;", (book_id, id_user_connected))
        already_exists = cursor.fetchone()

        # Fetch book details to re-render the page correctly later
        cursor.execute("SELECT * FROM Books WHERE id = ?;", (book_id,))
        book = cursor.fetchone()

        # Prevent duplicate entries on the waitlist
        if already_exists:
            conn.close()
            
            return templates.TemplateResponse(
                request=request,
                name="book_details.html",
                context={
                    "request": request,
                    "book_id": book[0],
                    "title": book[1],
                    "author": book[2],
                    "summary": book[3],
                    "category": book[4],
                    "price": book[5],
                    "rating": book[6],
                    "is_available": False,
                    "message": "⚠️ You are already in the waitlist for this book! You cannot join twice."
                }
            )

        # Get the active loan's due date to calculate expected availability
        cursor.execute("SELECT return_due_date FROM Loans WHERE book_id = ? AND actual_return_date IS NULL;", (book_id,))
        loan = cursor.fetchone()

        # Count how many people are already waiting ahead of this user
        cursor.execute("SELECT COUNT(*) FROM Waitlist WHERE book_id = ?;", (book_id,))
        people_ahead = cursor.fetchone()[0]

        # Insert the new waitlist record into the database with today's date
        today_str = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO Waitlist (book_id, id_user, joined_date) VALUES (?, ?, ?);", (book_id, id_user_connected, today_str))
        conn.commit()
        conn.close()

        # Waitlist logic and dynamic return date calculation (14 days per person ahead)
        if loan and loan[0]:
            current_due_date = datetime.strptime(loan[0], "%Y-%m-%d")
            final_expected_date = current_due_date + timedelta(days=people_ahead * 14)
            final_date_str = final_expected_date.strftime("%Y-%m-%d")

            if people_ahead == 0:
                msg = f"Success! You joined the waitlist. You are 1st in line! Expected availability date: {final_date_str}."
            else:
                msg = f"Success! You joined the waitlist. There are {people_ahead} people ahead of you. Expected date: {final_date_str}."
        else:
            msg = "Success! You joined the waitlist. The book will be available for you soon."

        # Re-render the book details page with the success message
        return templates.TemplateResponse(
            request=request,
            name="book_details.html",
            context={
                "request": request,
                "book_id": book[0],
                "title": book[1],
                "author": book[2],
                "summary": book[3],
                "category": book[4],
                "price": book[5],
                "rating": book[6],
                "is_available": False,
                "message": msg
            }
        )

    except Exception as e:
        print(f"Waitlist Error: {e}")
        return f"An error occurred while joining the waitlist: {e}"
    











     