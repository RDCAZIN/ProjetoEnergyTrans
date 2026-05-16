from models import db
from datetime import datetime

class Entrega(db.Model):
    __tablename__ = "entregas"

    id = db.Column(db.Integer, primary_key=True)

    material = db.Column(db.String(100), nullable=False)

    quantidade = db.Column(db.Float, nullable=False)

    pontos_gerados = db.Column(db.Integer, default=0)

    data_confirmacao = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    agendamento_id = db.Column(
        db.Integer,
        db.ForeignKey("agendamentos.id"),
        nullable=False
    )

    def __repr__(self):
        return f"<Entrega {self.id}>"