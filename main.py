from fastapi import FastAPI, Path, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
from db.index import isUserExist, addUser, getUserPassword, get_required_collection, store_password, retrieve_password, drop_user, delete_document
from utils.hash import hash_password, check_password, user_hash_username
from utils.generatePassword import generate_password
from utils.encrypt import encrypt, decrypt
from pydantic import BaseModel

app = FastAPI ()

# static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# template
templates = Jinja2Templates(directory="templates")


#models
class User(BaseModel):
    name: str
    email: str
    password: str

class Store(BaseModel):
    email: str
    masterPassword: str
    password: str
    url: Optional[str] = None
    name: Optional[str] = None

class Retrieve(BaseModel):
    email: str
    masterPassword: str
    url: Optional[str] = None
    name: Optional[str] = None


#Template rendering
@app.get ("/", response_class=HTMLResponse)
async def renderPage (request:Request):
    return templates.TemplateResponse("index.html", {"request":request} )


#Endpoints 
@app.get ("/api/account")
def create_New_Using_Get_Request (*, name: Optional[str] = None, email: Optional[str] = None, password: Optional[str] = None):
    if isUserExist(email):
        return {"Error": "Provided email is already registered"}
        
    else: 
        hashed_password = hash_password (password)
        uid = user_hash_username (email, password)
        addUser ({"name": name, "email": email, "password": hashed_password}, uid)
        return {"Message": "New User created successfully" }

    
@app.post("/api/account")
def create_New_User_Post_Request (user:User):
    if isUserExist(user.email):
        return {"Error": "User already exists"}
    else:
        hashed_password = hash_password (user.password)
        uid = user_hash_username (user.email, user.password)
        addUser ({"name": user.name, "email": user.email, "password": hashed_password})
        return {"Message": "New User created successfully"}

@app.delete ("/api/account")
def delete_an_user_account (user: User):

    if not isUserExist (user.email):
            return {"Error": "Email not found"}
    else:
            hashed_password = getUserPassword (user.email)
            check = check_password (user.password, hashed_password)
            if not check:
                return {"Error": "Invalid Password"}
            else: 
                drop_user (user.email)
                return {"Message": "Account successfully deleted"}

@app.get ("/api/suggestion")
def get_a_password_suggestion (length: Optional[int] = 8):
    return {"Password": generate_password(length)}


@app.post ("/api/store")
def store_a_password (store: Store):

    if not isUserExist(store.email): 
        return {"Error": "Email not found"}
    else:
        hashed_password = getUserPassword (store.email)
        check = check_password (store.masterPassword, hashed_password)
        if not check:
            return {"Error": "Invalid Password"}


    if store.name == None and store.url == None:
        return {"Error": "Please provide an identifier, either name, url or both"}
    else: 
        encrypted = encrypt (store.password)
        store_password (store.email, encrypted, store.url, store.name)
    
    
    return {"Success": "Password stored successfully"}

@app.post ("/api/retrieve")
def retrieve_a_password (retrieve: Retrieve):
       
        if not isUserExist (retrieve.email):
            return {"Error": "Email not found"}
        else:
            hashed_password = getUserPassword (retrieve.email)
            check = check_password (retrieve.masterPassword, hashed_password)
            if not check:
                return {"Error": "Invalid Password"}

        if retrieve.name == None and retrieve.url == None:
            return {"Error": "Please provide an identifier, either name, url or both"}
        else: 
            encrypted = retrieve_password (retrieve.email, retrieve.url, retrieve.name)
            password = decrypt (encrypted)
            return {"Password": password}

@app.delete ("api/password")
def delete_a_password (doc: Retrieve):
        if not isUserExist (doc.email):
            return {"Error": "Email not found"}
        else:
            hashed_password = getUserPassword (doc.email)
            check = check_password (doc.masterPassword, hashed_password)
            if not check:
                return {"Error": "Invalid Password"}

        if doc.name == None and doc.url == None:
            return {"Error": "Please provide an identifier, either name, url or both"}
        else: 
            delete_document (email, doc.url, doc.name)
            return {"Message": "Your password is successfully deleted"}
    


    

    




