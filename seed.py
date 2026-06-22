from app import app
from models import db

from models.usuarios import Usuario
from models.ponto_coleta import PontoColeta
from models.agendamento import Agendamento

with app.app_context():

    # APAGA TODOS OS DADOS
    db.drop_all()

    # RECRIA AS TABELAS
    db.create_all()

    print("Banco recriado!")

    # =========================
    # USUÁRIOS
    # =========================

    usuario1 = Usuario(
        nome="Ronald",
        email="ronald@email.com",
        senha="123",
        tipo="usuario",
        pontos=120
    )

    usuario2 = Usuario(
        nome="Maria",
        email="maria@email.com",
        senha="123",
        tipo="usuario",
        pontos=80
    )

    coletor1 = Usuario(
        nome="Eco Coleta",
        email="eco@email.com",
        senha="123",
        tipo="coletor",
        pontos=0
    )

    db.session.add_all([
        usuario1,
        usuario2,
        coletor1
    ])

    db.session.commit()

    print("Usuários criados!")

    # =========================
    # PONTOS DE COLETA
    # =========================

    ponto1 = PontoColeta(
        nome="EcoPoint Centro",
        endereco="Av. Central, 100",
        materiais_aceitos="Pilhas, Baterias, Celulares",
        horario_funcionamento="08:00 às 18:00",
        latitude="-3.1190",
        longitude="-60.0217",
        aprovado=True,
        coletor_id=coletor1.id
    )

    ponto2 = PontoColeta(
        nome="Green Reciclagem",
        endereco="Rua Verde, 250",
        materiais_aceitos="Notebooks, Cabos, Eletrônicos",
        horario_funcionamento="09:00 às 17:00",
        latitude="-3.1000",
        longitude="-60.0250",
        aprovado=True,
        coletor_id=coletor1.id
    )

    ponto3 = PontoColeta(
        nome="Ponto Sustentável",
        endereco="Av. Brasil, 500",
        materiais_aceitos="Baterias, Fontes, Monitores",
        horario_funcionamento="07:00 às 16:00",
        latitude="-3.1300",
        longitude="-60.0150",
        aprovado=True,
        coletor_id=coletor1.id
    )

    ponto4 = PontoColeta(
        nome="EcoPoint Jorge Teixeira",
        endereco="Av. Itaúba, Jorge Teixeira",
        materiais_aceitos="Pilhas, Baterias, Celulares, Cabos",
        horario_funcionamento="08:00 às 18:00",
        latitude="-3.0440",
        longitude="-59.9440",
        aprovado=True,
        coletor_id=coletor1.id
    )

    ponto5 = PontoColeta(
        nome="Recicla Cidade Nova",
        endereco="Av. Noel Nutels, Cidade Nova",
        materiais_aceitos="Notebooks, Monitores, Impressoras",
        horario_funcionamento="08:00 às 17:00",
        latitude="-3.0180",
        longitude="-60.0150",
        aprovado=True,
        coletor_id=coletor1.id
    )

    ponto6 = PontoColeta(
        nome="Ponto Verde Ponta Negra",
        endereco="Av. Coronel Teixeira, Ponta Negra",
        materiais_aceitos="Baterias, Fontes, Equipamentos Eletrônicos",
        horario_funcionamento="09:00 às 18:00",
        latitude="-3.0620",
        longitude="-60.1030",
        aprovado=True,
        coletor_id=coletor1.id
    )

    db.session.add_all([
        ponto1,
        ponto2,
        ponto3,
        ponto4,
        ponto5,
        ponto6
    ])

    db.session.commit()

    print("Pontos de coleta criados!")

    # =========================
    # AGENDAMENTOS
    # =========================

    agendamento1 = Agendamento(
        data_agendada="20/05/2026",
        horario="14:00",
        status="pendente",
        usuario_id=usuario1.id,
        ponto_coleta_id=ponto1.id
    )

    agendamento2 = Agendamento(
        data_agendada="22/05/2026",
        horario="10:30",
        status="pendente",
        usuario_id=usuario2.id,
        ponto_coleta_id=ponto2.id
    )

    db.session.add_all([
        agendamento1,
        agendamento2
    ])

    db.session.commit()

    print("Agendamentos criados!")

    print("SEED FINALIZADA!")