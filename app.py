from flask import Flask
from routes.main import main
from models import db  

app = Flask(__name__)

#configuração do banco
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'sua_chave_secreta'

db.init_app(app)

#importando os models
from models.usuarios import Usuario

with app.app_context():
    db.create_all()

# registrando o blueprint
app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)