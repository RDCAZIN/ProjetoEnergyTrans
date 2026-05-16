from models import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # "usuario" ou "coletor"
    pontos = db.Column(db.Integer, default = 0)
    def __repr__(self):
        return f"<Usuario id={self.id} email={self.email} tipo={self.tipo}>"