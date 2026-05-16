from models import db
from datetime import datetime

class Agendamento(db.Model):
    __tablename__ = "agendamentos"

    id = db.Column(db.Integer, primary_key=True)

    data_agendada = db.Column(db.String(20), nullable=False)

    horario = db.Column(db.String(20), nullable=False)

    status = db.Column(
        db.String(20),
        default="pendente"
    )

    criado_em = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    ponto_coleta_id = db.Column(
        db.Integer,
        db.ForeignKey("pontos_coleta.id"),
        nullable=False
    )

    def __repr__(self):
        return f"<Agendamento {self.id}>"