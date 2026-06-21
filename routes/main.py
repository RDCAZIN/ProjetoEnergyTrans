from flask import Blueprint, render_template, request, redirect, url_for,flash,session
from models import db
from models.usuarios import Usuario
from models.ponto_coleta import PontoColeta
from models.agendamento import Agendamento
from models.entrega import Entrega


import folium
import json
from geopy.geocoders import Nominatim
from flask import jsonify

main = Blueprint('main', __name__)

# Página inicial (seleção de perfil)
@main.route('/')
def home():
    return render_template("autenticacao/index.html")


# Recebe escolha do perfil (usuario ou coletor)
@main.route("/escolha", methods=["POST"])
def escolha():
    tipo = request.form.get("tipo")
    if tipo in ["usuario", "coletor"]:
        session["tipo_usuario"] = tipo
        return redirect(url_for("main.tem_conta"))

    return redirect(url_for("main.home"))

# Tela "tem conta ou não"
@main.route("/tem_conta")
def tem_conta():
    return render_template("autenticacao/temconta.html")

#Recebe escolha se tem conta ou não
@main.route("/possui_conta", methods=["POST"])
def possui_conta():
    possui = request.form.get("possui_conta")
    if possui == "sim":
        return redirect(url_for('main.login'))
    
    elif possui == "nao":
        return redirect(url_for('main.cadastro'))
    
    return redirect(url_for('main.tem_conta'))


#CADASTRO DE USUARIO NO BANCO DE DADOS
@main.route("/cadastro", methods = ["POST" ,"GET"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome_cadastro")
        email = request.form.get("email_cadastro")
        senha = request.form.get("senha_cadastro")
        confirma_senha = request.form.get("confirma_senha")
        tipo = session.get("tipo_usuario")   
    
        if senha != confirma_senha:
            flash("As senhas estão diferentes")
            return redirect(url_for('main.cadastro'))
        else:
            email_existe = Usuario.query.filter_by(email = email).first()

            if email_existe:
                flash("Esse e-mail ja foi cadastrado, tente outro")
                return redirect(url_for('main.cadastro'))
            else:
                novo_usuario = Usuario(
                    nome = nome,
                    email = email,
                    senha = senha,
                    tipo = tipo
                )

                db.session.add(novo_usuario)
                db.session.commit()
                return redirect(url_for('main.login'))
    return render_template("autenticacao/cadastro.html")

#login, verica se o email ta correto, senha e se o usuario escolheu o perfil certo
@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")
        tipo = session.get("tipo_usuario")
        usuario = Usuario.query.filter_by(email=email).first()
        if not usuario:
            flash("E-mail não encontrado", "erro")
            return redirect(url_for("main.login"))
        if usuario.senha != senha:
            flash("Senha incorreta", "erro")
            return redirect(url_for("main.login"))
        if usuario.tipo != tipo:
            flash("Perfil incorreto", "erro")
            return redirect(url_for("main.login"))
        # login OK
        session["usuario_id"] = usuario.id
        session["usuario_nome"] = usuario.nome
        session["usuario_tipo"] = usuario.tipo
        session.pop("tipo_usuario", None)
        if usuario.tipo == "coletor":
            return redirect(url_for("main.home_coletor"))
        else:
            return redirect(url_for("main.home_usuario"))

    return render_template("autenticacao/login.html")

#Verica se o usuario tem um email, existente para mudar a senha
@main.route("/esqueceu_senha", methods = ["GET", "POST"])
def esqueceu_senha():
    if request.method == "POST":
        email = request.form.get("email")
        email_exite = Usuario.query.filter_by(email = email).first()
        if email_exite:
            session["email"] = email
            return redirect(url_for("main.nova_senha"))
        else:
            flash("Email incorreto!", "erro")
            return redirect(url_for("main.esqueceu_senha"))
    return render_template("autenticacao/esqueci_senha_email.html")

#MUDA A SENHA
@main.route("/nova_senha", methods = ["POST" , "GET"])
def nova_senha():

    if request.method == "POST":
        senha = request.form.get("senha")
        confirma_senha = request.form.get("confirmar_senha")
        email = session.get("email")

        if senha != confirma_senha:
            flash("As senhas são diferentes", "erro")
            return redirect(url_for("main.nova_senha"))
        else:
            usuario = Usuario.query.filter_by(email = email).first()
            usuario.senha = senha
            db.session.commit()
            return redirect(url_for("main.login"))
    return render_template("autenticacao/nova_senha.html")

#---------------
#TELAS DO USUARIO|
#-----------------

@main.route("/home_usuario")
def home_usuario():
    material = request.args.get("material")
    #CRINDO LISTA DE MATERIAS PARA O FILTRO
    materias = [
        "Pilhas",
        "Baterias",
        "Celulares",
        "Painéis"
    ]
    if material:
        pontos = PontoColeta.query.filter(
            PontoColeta.aprovado == True,
            PontoColeta.materiais_aceitos.ilike(f"%{material}%")
        ).all()
    else:
        pontos = PontoColeta.query.filter_by(aprovado = True).all()
    #criando mapa
    control_scale=True
    mapa = folium.Map(location=[-3.1190, -60.0217], zoom_start=13  )
    ##ADICIONANDO OS PONTOS NO MAPA
    for ponto in pontos:
        folium.Marker(
            [ponto.latitude, ponto.longitude],
            tooltip=ponto.nome
        ).add_to(mapa)
    mapa_html = mapa._repr_html_()
    #INFORMAÇOES QUE SERÃO MOSTRADAS
    pontos_json = json.dumps([
        {
            "id": ponto.id,
            "nome": ponto.nome,
            "endereco": ponto.endereco,
            "materiais": ponto.materiais_aceitos,
            "horario": ponto.horario_funcionamento,
            "latitude": ponto.latitude,
            "longitude": ponto.longitude
        }
        for ponto in pontos
    ])
    return render_template("usuario/home_usuario.html",mapa = mapa_html, pontos_json = pontos_json, materias = materias)

@main.route("/buscar_endereco")
def buscar_endereco():
    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")

    geolocator = Nominatim(user_agent="energytrans")
    localizacao = geolocator.reverse(f"{latitude}, {longitude}")

    endereco = localizacao.raw["address"]
    bairro = endereco.get(
        "suburb", 
        "Bairro não encontrado")
    cidade = endereco.get(
        "city",
        endereco.get(
            "town", 
            endereco.get(
                "municipality", 
                "Cidade não encontrada")
                ) )
    return jsonify({
        "bairro": bairro,
        "cidade": cidade
    })


@main.route("/vizualizacao_agendamentos_usuario", methods = ["POST", "GET"])
def vizualizacao_agendamentos_usuario():
    usuario_id = session.get("usuario_id")
    #cancelando/deletando agendamento
    if request.method == "POST":
        agendamento_id = request.form.get("agendamento_id")
        agendamento_cancela = Agendamento.query.get(agendamento_id)
        db.session.delete(agendamento_cancela)
        db.session.commit()
        return redirect(url_for("main.vizualizacao_agendamentos_usuario"))
    
    #mostrando agendametos
    agendamentos = Agendamento.query.filter_by(usuario_id= usuario_id)
    return render_template("usuario/vizualizar_agendamentos.html", agendamentos = agendamentos)
    

@main.route("/historico_usuario")
def historico_usuario():
    return "Historico"

@main.route("/loja_cupons")
def loja_cupons():
    return "Cupons"


#usuario agenda entrega
@main.route("/agendar", methods = ["POST"])
def agendar():
    data_agendada = request.form.get("data_agendada")
    horario = request.form.get("horario")
    ponto_id = request.form.get("ponto_id")
    usuario_id = session.get("usuario_id")
    
    novo_agendamento = Agendamento(
        data_agendada = data_agendada,
        horario = horario,
        ponto_coleta_id = ponto_id,
        usuario_id = usuario_id,
        status = "Pendente"

    )

    db.session.add(novo_agendamento)
    db.session.commit()

    flash("Agendamento realizado com sucesso! ")

    return redirect(url_for("main.home_usuario"))

#-----------------
#TELAS DO COLETOR ||
#-----------------

@main.route("/home_coletor", methods = ["POST", "GET"])
def home_coletor():

    #delete do ponto
    if request.method == "POST":
        ponto_id = request.form.get("ponto_id")
        ponto = PontoColeta.query.get(ponto_id)

        if ponto.agendamentos:
            flash("esse ponto tem agendamentos pendentes !", "erro")
            return redirect(url_for('main.home_coletor'))
        else:
            db.session.delete(ponto)
            db.session.commit()
            return redirect(url_for('main.home_coletor'))
        
    coletor_id = session.get("usuario_id")
    pontos = PontoColeta.query.filter_by(coletor_id = coletor_id).all()
    return render_template ("coletor/home_coletor.html", pontos = pontos)



#o coletor confirma a entrega e gera os pontos
@main.route("/confirmar_entrega", methods = ["POST"])
def confirmar_entrega():
    agendamento_id = request.form.get("agendamento_id")
    peso = float(request.form.get("peso"))
    material = request.form.get("material")
    agendamento = Agendamento.query.get(agendamento_id)
    pontos = round((peso*10),2)

    #atualizar status do agendamento
    agendamento.status = "concluido"
    agendamento.peso_entregue = peso
    agendamento.pontos_gerados = pontos

    #adicionando pontos para usuario
    usuario = agendamento.usuario
    usuario.pontos += pontos

    #atualizando entregas
    nova_entrega = Entrega(
        material = material,
        peso = peso,
        pontos_gerados = pontos,
        data_entrega = agendamento.data_agendada,
        usuario_id=usuario.id,
        ponto_coleta_id= agendamento.ponto_coleta_id
    )
    db.session.add(nova_entrega)
    db.session.commit()
    flash("Entrega confirmada")
    return redirect(url_for("main.home_coletor"))

@main.route("/cadastrar_ponto", methods = ["POST"])
def cadastrar_ponto():
    nome = request.form.get("nome_ponto")
    endereco = request.form.get("endereco_ponto")
    materiais_aceitos = request.form.get("materias_ponto")
    horario_funcionamento = request.form.get("horario_ponto")
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")
    coletor_id = session.get("usuario_id")

    if not latitude or not longitude:
        flash("Localização invalida", "erro")
        return redirect(url_for("main.cadastrar_ponto"))
    else:
        latitude = float(latitude)
        longitude = float(longitude)
            
        novo_ponto = PontoColeta(
            nome = nome,
            endereco = endereco,
             materiais_aceitos = materiais_aceitos,
             horario_funcionamento = horario_funcionamento,
            latitude = latitude,
            longitude = longitude,
            coletor_id = coletor_id
            )

        db.session.add(novo_ponto)
        db.session.commit()
        flash("Cadastro Realizado com sucesso!")
    return redirect(url_for("main.home_coletor"))
    
 


@main.route("/editar_ponto", methods = ["POST"])
def editar_ponto():
    ponto_id = request.form.get("ponto_id")
    nome_ponto = request.form.get("nome_ponto")
    endereco_ponto = request.form.get("endereco_ponto")
    materias_ponto = request.form.get("materias_ponto")
    horario_ponto = request.form.get("horario_ponto")

    ponto = PontoColeta.query.get(ponto_id)

    ponto.nome = nome_ponto
    ponto.edereco = endereco_ponto
    ponto.materiais_aceitos = materias_ponto
    ponto.horario_funcionamento = horario_ponto

    db.session.commit()


    return redirect(url_for("main.home_coletor"))




