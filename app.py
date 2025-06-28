from flask import Flask, request, jsonify
from Common.db import db 
from models.user import User
from routes.auth.signUp import handle_signUp
from routes.auth.login import handle_login
#--- LISTS ---
from routes.Lists.fetchListsWithUserId import fetchListsWithUserId
from routes.Lists.createListsWithUserId import createListsWithUserId
from routes.Lists.editListsWithListId import editListsWithListId
from routes.Lists.deleteListsWithListId import deleteListsWithListId
from routes.Lists.searchListsWithZKeyWord import searchListsWithZKeyWord
#--- ToDos ---
from routes.ToDos.createToDosWithListId import createToDosWithListId
from routes.ToDos.fetchToDosWithListId import fetchToDosWithListId
from routes.ToDos.editToDosWithToDoId import editToDosWithToDoId
from routes.ToDos.deleteToDosWithToDoId import deleteToDosWithToDoId
from routes.ToDos.searchToDosWithZKeyWord import searchToDosWithZKeyWord

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()

#-----------------------------------------------------------------------------------

@app.route("/search_todos", methods=["GET"])
def search_todos():
    return searchToDosWithZKeyWord()

@app.route("/delete_todos",methods=["DELETE"])
def delete_todos():
    return deleteToDosWithToDoId()

@app.route("/edit_todos", methods=["PUT"])
def edit_todos():
    return editToDosWithToDoId()

@app.route("/fetch_todos", methods=["GET"])
def fetch_todos():
    return fetchToDosWithListId()
    
@app.route("/create_todos", methods=["POST"])
def create_todos():
    return createToDosWithListId()
    
#-----------------------------------------------------------------------------------

@app.route("/search_lists", methods=['GET'])
def search_lists():
    return searchListsWithZKeyWord()
    
@app.route("/delete_lists", methods=["DELETE"])
def delete_lists():
    return deleteListsWithListId()
    
@app.route("/edit_lists", methods=["PUT"])
def edit_lists():
    return editListsWithListId()
    
@app.route("/create_lists", methods=["POST"])
def create_lists():
    return createListsWithUserId()
    
@app.route("/fetch-lists", methods=["GET"])
def fetch_lists():
    return fetchListsWithUserId()
#-------------------------------------------------------------------------------------

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    response, status = handle_signUp(data)
    return jsonify(response), status

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    response, status = handle_login(data)
    return jsonify(response), status

#--------------------------------------------------------------------------------------

@app.route("/")
def home():
    return "HELLO FLASK !"

if __name__ == "__main__":
    app.run(debug=True)
