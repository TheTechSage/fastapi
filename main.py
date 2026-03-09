from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["testdb"]
users = db["users"]


#  fdfdsaftrdsfsdfsd
# users.insert_one({"name": "John Doe", "email": "john.doe@example.com"})


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
    return templates.TemplateResponse(
        request=request,
        name="contact.html"
    )


# data = collection.find().limit(10)
# for item in data:
#     print(item)


#  jinja2 


# router 
# apiRouter = APIRouter()

# port => 8000 to run the the other server
# use this command => uvicorn main:app --port=1000 --reload