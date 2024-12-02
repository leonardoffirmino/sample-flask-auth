from flask import Flask, jsonify, request
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required


app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///database.db'


login_manager = LoginManager()
db.init_app(app)
# Session < Conexão ativa do banco de dados
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)
  
#View de login para autenticação 
@app.route("/login", methods=["POST"])
def login():
  data = request.json
  username = data.get("username")
  password = data.get("password")

  if username and password:
    #Login
    user = User.query.filter_by(username=username).first()

    if user and user.password == password:
      # Autenticado com sucesso
      login_user(user)
      print(current_user.is_authenticated)
      return jsonify({"message":"Autenticação realizada com sucesso"})

    return jsonify({"message":"Falha de autenticação!!"})
  
  return jsonify({"message":"Credentials invalid!"}),400

@app.route("/logout", methods=["GET"])
@login_required
def logout():
  logout_user()
  return jsonify({"message": "Logout realizado com sucesso"})

@app.route("/user",methods=['POST'])
def create_user():
  data = request.json
  username = data.get("username")
  password = data.get("password")

  if username and password:
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Usuário cadastrado com sucesso."})

  return jsonify({"message": "Dados invalidos!"}),400

@app.route("/user/<int:id_user>", methods=["GET"])
@login_required
def read_user(id_user):
  user = User.query.get(id_user)

  if user:
    return {"username": user.username}
  
  return jsonify({"message":"Usuário não encontrado!"}),404


@app.route("/user/<int:id_user>", methods=["PUT"])
@login_required
def update_user(id_user):
  user = User.query.get(id_user)
  data = request.json

  #Update de password lembrando que sempre e indicado alterar somente senhas do que user!
  if user and data.get("password"):
    user.password = data.get("password")
    db.session.commit()
    return jsonify({"message": f"Usuário {user.username} atualizado com sucesso"})

  return jsonify({"message":"Usuário não encontrado!"}),404


@app.route("/user/<int:id_user>", methods=["DELETE"])
@login_required
def delete_user(id_user):
  user = User.query.get(id_user)

  if user:
    return jsonify({"message",f"Usuário deletado com sucesso -- {user.username}"})

  return jsonify({"message":"Usuário não encontrado!"}),404


@app.route("/hello-world",methods=["GET"])
def hello_world():
  return "Application is running!"

if __name__ == "__main__":
  app.run(debug=True)