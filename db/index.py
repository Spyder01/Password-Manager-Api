import pymongo
import urllib as url

myclient = pymongo.MongoClient ("mongodb+srv://Suhan_Ubuntu:"+url.parse.quote("owmshitkintk@123")+"@cluster0.v4vzz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = myclient["PasswordManager"]

Users = db["Users"]



def createCollection (name):
    return db[name]


def collectionExists (name):
    Collections = db.list_collection_names ()
    if name in Collections:
        return True
    else: return False


def isUserExist (email):
    x = Users.find()
    for y in x:
     try:
        #print (y["email"])
        if y["email"] == email:
            return True
     except: print("Error")
    return False

def createUserCollection (x_key):
    newUser = db[x_key]
    return newUser

def addUser (entry):
    print (entry)
    confirm = Users.insert_one(entry)
    return createUserCollection (entry["email"])

def getUserPassword (email):
    x = Users.find ()
    for y in x:
        try: 
            if y["email"] == email:
                return y["password"]
        except: return "Error"
    return "Error"

def get_required_collection (check_hash, key):
    collections = db.list_collection_names ()
    for x in collections:
     if x!="Users":
        print(x, key)
        if check_hash (key, x):
            return db[x]


def store_password (email, password, url, name): 

    collection = db[email]
    confirm = collection.insert_one ({
        "url": url,
        "password": password,
        "name": name
    })




def retrieve_password (email, url, name):

    collection = db[email]
    x = collection.find ()

    for y in x:
        try: 
            if y["name"] == name and y["url"] == url:
                return y["password"]
        except: return "Error"
    
    return "Error"


def drop_user (email):

    collection = db [email]
    collection.drop ()
    Users.delete_one ({"email": email})

def delete_document (email, url, name):
    collection = db [email]
    my_query = {"name": name, "url": url}
    collection.delete_one (my_query)
