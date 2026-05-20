from models import db

class Entrega(db.Model):

    __tablename__ = "entregas"

    id = db.Column(db.Integer,primary_key=True)

    material = db.Column(db.String(50),nullable=False)

    peso = db.Column(db.Float,nullable=False)

    pontos_gerados = db.Column(
        db.Float,
        nullable=False
    )

    data_entrega = db.Column(
        db.String(20),
        nullable=False
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id")
    )

    ponto_coleta_id = db.Column(
        db.Integer,
        db.ForeignKey("pontos_coleta.id")
    )