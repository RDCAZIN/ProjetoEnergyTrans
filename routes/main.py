from flask import Blueprint, render_template, request, redirect, url_for

main = Blueprint('main', __name__)

# Página inicial (seleção de perfil)
@main.route('/')
def home():
    return render_template("autenticacao/index.html")


# Recebe escolha do perfil (usuario ou coletor)
@main.route("/escolha", methods=["POST"])
def escolha():
    tipo = request.form.get("tipo")

    if tipo == "usuario":
        return redirect(url_for('main.tem_conta'))

    elif tipo == "coletor":
        return redirect(url_for('main.tem_conta'))

    # fallback (se não vier nada válido)
    return redirect(url_for('main.home'))


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

@main.route("/cadastro")
def cadastro():
    return render_template("autenticacao/cadastro.html")


@main.route("/login")
def login():
    return render_template("autenticacao/login.html")