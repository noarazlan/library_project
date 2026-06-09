from fastapi import FastAPI
from routers import users, books, loans
import uvicorn

app = FastAPI()
app.include_router(users.router)
app.include_router(books.router)
app.include_router(loans.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)