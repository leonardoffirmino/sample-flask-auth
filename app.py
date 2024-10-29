from flask import Flask, jsonify, request
from models.user import User
from database import db
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///database.db'


login_manager = LoginManager()
db.init_app(app)
# Session < Conexão ativa do banco de dados
login_manager.init_app(app)

#View de login para autenticação 
@app.route("/login", methods=["POST"])
def login():
  data = request.json
  username = data.get("username")
  password = data.get("password")

  if username and password:
    #Login
    pass
  
  return jsonify({"message":"Credentials invalid!"}),400


@app.route("/hello-world",methods=["GET"])
def hello_world():
  return "Deu bom :)"

if __name__ == "__main__":
  app.run(debug=True)