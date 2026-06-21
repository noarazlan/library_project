from fastapi import FastAPI
from routers import users, books, loans
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

app.mount("/static/css", StaticFiles(directory="C:/Users/salom/OneDrive/שולחן העבודה/cyberpro/midle_project/library_project/templates/css"), name="static_css")

app.include_router(users.router)
app.include_router(books.router)
app.include_router(loans.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)