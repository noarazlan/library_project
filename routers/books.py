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

        # Secure SQL query using parameterized input to prevent SQL Injection
        query = "SELECT * FROM Books WHERE LOWER(title) = LOWER(?);"
        cursor.execute(query, (book_name.strip(),))
        
        # Fetch the first matching row
        book_found = cursor.fetchone()
        conn.close()

        # Check if the book was not found in the database
        if book_found is None:
            # Re-render the search page with an error message, explicitely setting recommended_books to None
            return templates.TemplateResponse(
                request=request, 
                name="search_book.html", 
                context={"request": request, "error": f"The book '{book_name}' does not exist in our library.", "recommended_books": None}
            )

        # Map the database columns to a context dictionary for Jinja2
        book_context = {
            "request": request,
            "title": book_found[1],
            "author": book_found[2],
            "summary": book_found[3],
            "category": book_found[4],
            "price": book_found[5],
            "rating": book_found[6]
        }    
        # Successfully found the book; render the dynamic details page
        return templates.TemplateResponse(request=request, name="book_details.html", context=book_context)
        
    except Exception as e:
        print(f"Server Error: {e}")
        return templates.TemplateResponse(
            request=request, 
            name="search_book.html", 
            context={"request": request, "error": "An error occurred on the server.", "recommended_books": None}
        )
   

# Route to get and display recommended books on the same page
@router.get("/recommended", response_class=HTMLResponse)
async def get_recommended_books(request: Request):
    try:
        # Establish a connection to the SQLite database
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()

        # Query to fetch books with a rating of 4.5 or higher
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