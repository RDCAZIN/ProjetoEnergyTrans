from models import db

class PontoColeta(db.Model):
    __tablename__ = 'pontos_coleta'

    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), nullable = False)
    endereco = db.Column(db.String(200), nullable = False)
    materiais_aceitos = db.Column(db.String(300),nullable = False )
    horario_funcionamento = db.Column(db.String(100))
    latitude = db.Column(db.String(50))
    longitude = db.Column(db.String(50))
    aprovado = db.Column(db.Boolean, default=True)
    coletor_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id")
    )

    def __repr__(self):
        return f"<PontoColeta {self.nome}>"
    