from fastapi import APIRouter, Request , Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import sqlite3



router = APIRouter()
templates = Jinja2Templates(directory= "templates")


@router.get("/")
def home_page(request:Request):
    return templates.TemplateResponse(request, "index.html")
   

@router.get("/login")
def log_in(request:Request):
    return templates.TemplateResponse(request, "log_in.html")

@router.get("/add-user")
def add_user(request:Request):
    return templates.TemplateResponse(request, "register.html")

@router.post("/login")
def log_in(request:Request, 
           username:str = Form(), 
           password:str = Form()):
    
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("""select * 
                   from Users 
                   where username = ?
                   and password = ?""",
                    (username,password))
    
    user = cursor.fetchone()

    conn.close()

    if user:
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(key="id_user", value = user[0])
        return response

    return templates.TemplateResponse(request, "index.html" , {"Message":"Wrong Username or Password"})


@router.post("/add-user")
def add_user(request:Request,
             user_id:int = Form(),
            full_name:str = Form(),
            email:str = Form(),
            username:str = Form(),
            password:str = Form()):
    
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    cursor.execute("""select * 
                   from Users
                   where username = ?
                   or email = ?
                   """, (username, email))
    
    user_valid = cursor.fetchall()

    if user_valid:
        conn.close()
        return templates.TemplateResponse(request, "register.html" ,{"Message": "This username or email already exist"})
    
    cursor.execute("insert into Users (id_user, username, email, password, full_name) values(?,?,?,?,?)", (user_id, username,email,password,full_name))
    conn.commit()
    conn.close()
    return templates.TemplateResponse(request, "index.html", {"Message": f"{username} was successfully added"})
    
    
@router.get("/profile")
def get_profile(request:Request):

    user_id = request.cookies.get("id_user")
    
    if user_id is None:
        return RedirectResponse(url="/", status_code=303)
    
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    cursor.execute(""" select full_name, username, email
                        from Users
                        where id_user = ?
                        """, (user_id,))
    
    user = cursor.fetchone()

    if user is None:
        return templates.TemplateResponse(request, "index.html", {"Message": "User not found"})
    
    cursor.execute(""" select b.title, 
                              b.author,
                              b.summary,
                              b.category,
                              b.price,
                              l.borrow_date,
                              l.actual_return_date
                        from Loans as l
                        inner join Books as b
                        on b.id = l.book_id
                        where l.id_user = ? """ ,(user_id,))
    books = cursor.fetchall()
    conn.close()

    return templates.TemplateResponse(request, "profile.html" , 
                                      {
                                        "full_name": user[0],
                                         "username": user[1],
                                          "email" : user[2],
                                           "books": books })