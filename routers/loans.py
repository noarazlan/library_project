from fastapi import APIRouter, Request , Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import sqlite3
from datetime import date, timedelta

router = APIRouter(  prefix="/loans", tags=["loans"])
templates = Jinja2Templates(directory= "templates")

@router.post("/borrow")
async def borrow_book(request:Request, book_id : int = Form()):

    user_id = request.cookies.get("id_user")

    if user_id is None:
        return RedirectResponse(url="/login", status_code=303)
    
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    
    cursor.execute("select return_due_date from Loans where actual_return_date is Null and id_user = ?",(user_id,))
    counter = cursor.fetchall()
    for day in counter:
        due_date = date.fromisoformat(day[0])
        if date.today() > due_date + timedelta(days=10):
            conn.close()
            return templates.TemplateResponse(request, "index.html", {"Message" : "You cannot borrow more books because you didny return one of your books and its passed 10 days from returning date"})

    cursor.execute("select count(*) from Loans where id_user = ? and actual_return_date is Null",(user_id,))
    counter = cursor.fetchone()[0]
    if counter >= 3:
        conn.close()
        return templates.TemplateResponse(request, "index.html", {"Message" : "You cannot borrow more then 3 book at the same time"})
    
    
    cursor.execute("SELECT * FROM Loans WHERE book_id = ? AND actual_return_date IS NULL;", (book_id,))
    active_loan = cursor.fetchone()

    if active_loan:
        conn.close()
        return templates.TemplateResponse(request, "index.html",
            {
                "Message": "This book is already borrowed"
            }
        )

    borrow_date = date.today()
    return_due_date = borrow_date + timedelta(days=14)


    cursor.execute("insert into Loans(id_user,book_id,borrow_date,return_due_date,actual_return_date) values(?,?,?,?,?)",
                    ( user_id, book_id, borrow_date.isoformat(),return_due_date.isoformat(), None))
    
    conn.commit()
    conn.close()

    return RedirectResponse(url="/profile", status_code=303)



@router.post("/return-confirm")
async def return_confirm(request:Request, loan_id : int = Form(), book_title : str = Form()):
    return templates.TemplateResponse(request, "returns.html", {"loan_id" : loan_id, "book_title": book_title})

@router.post("/return")
async def return_book(request:Request, loan_id:int = Form()):

    user_id = request.cookies.get("id_user")

    if user_id is None:
        return RedirectResponse(url="/login", status_code=303)
    
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    cursor.execute("update Loans set actual_return_date = ? where id = ? and id_user = ? and actual_return_date is Null", (date.today().isoformat(), loan_id, user_id))

    conn.commit()
    conn.close()


    return RedirectResponse(url="/profile", status_code=303)
    


    
