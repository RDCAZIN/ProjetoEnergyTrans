from flask import Blueprint, render_template, request, redirect, url_for,flash,session
from models import db
from models.usuarios import Usuario

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
        session["usuario_tipo"] = usuario.tipo

        if usuario.tipo == "coletor":
            return redirect(url_for("main.home_coletor"))
        else:
            return redirect(url_for("main.home_usuario"))

    return render_template("autenticacao/login.html")


@main.route("/home_usuario")
def home_usuario():
    return "HOME USUARIO"

@main.route("/home_coletor")
def home_coletor():
    return "HOME DO COLETOR"

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
            flash("Email incorreto!")
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
            flash("As senhas são diferentes")
            return redirect(url_for("main.nova_senha"))
        else:
            usuario = Usuario.query.filter_by(email = email).first()
            usuario.senha = senha
            db.session.commit()
            return redirect(url_for("main.login"))
    return render_template("autenticacao/nova_senha.html")