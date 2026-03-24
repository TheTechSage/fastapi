from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["testdb"]
users = db["users"]

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    users_data = users.find().limit(2)

    # print(users_data)

    usrdata = []
    for user in users_data:
        usrdata.append(user)

    print(usrdata)
    

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"users": usrdata}
    )

@app.get("/about", response_class=HTMLResponse)
async def read_about(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="about.html"
    )

@app.get("/contact", response_class=HTMLResponse)
async def read_about(request: Request):

    arr = []

    if arr:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return templates.TemplateResponse(
        request=request,
        name="contact.html"
    )


