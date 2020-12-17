from flask import Flask, render_template, request, session
from flask_mail import Mail,  Message
from formularios import formUsuario
import os
import sqlite3
from markupsafe import escape
import hashlib
from flask_session import Session
import easygui as eg

app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config.update(dict(
       DEBUG = True,
       MAIL_SERVER = 'smtp.gmail.com',
       MAIL_PORT = 587,
       MAIL_USE_TLS = True,
       MAIL_USE_SSL = False,
       MAIL_USERNAME = 'noResponderMisionTicD@gmail.com',
       MAIL_PASSWORD = 'm1s10nt1c'
))
app.config.from_object(__name__)
Session(app)

app.secret_key = os.urandom(24)

mail = Mail(app)

@app.route("/", methods=["POST", "GET"])
def login():
    return render_template("login.html")

@app.route("/forgot", methods=["POST", "GET"])
def forgot():
    return render_template("forgot.html")

@app.route("/inicioUsuario", methods=["POST", "GET"])
def inicioUsuario():
    if (request.method == "POST"):
        form = formUsuario()
        username = request.form["usuario"]
        password = request.form["password"]
        h = hashlib.sha256(password.encode())
        pwd = h.hexdigest()
        with sqlite3.connect("proyectoDB.db") as con:
            cur = con.cursor()
            cur.execute(
                "SELECT * FROM usuarios WHERE nombre = ? AND clave = ?", [username, pwd])
            if cur.fetchone():
                session["usuario"] = username
                return render_template("inicioUsuario.html", form=form)
        eg.msgbox(msg='Usuario o contraseña inválidos!',
                title='Error!!', 
                ok_button='Aceptar')
        return render_template("login.html")
    else:
        return render_template("inicioUsuario.html")

@app.route("/crearProducto")
def crearProducto():
    return render_template("crearProducto.html")

@app.route("/nuevoUsuario")
def nuevoUsuario():
    return render_template("nuevoUsuario.html")

@app.route("/usuario/crear", methods=["POST"])
def usuario_crear():
    user = escape(request.form["usuario"])
    password = escape(request.form["password"])
    email = escape(request.form["email"])
    h = hashlib.sha256(password.encode())
    pwd = h.hexdigest()
    with sqlite3.connect("proyectoDB.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO usuarios (nombre, clave, correo) VALUES (?,?,?)",
                    (user, pwd, email))
        con.commit()
        eg.msgbox(msg='Usuario creado satisfactoriamente',
            title='Atención', 
            ok_button='Aceptar')
        return render_template("nuevoUsuario.html")
    eg.msgbox(msg='Usuario NO creado',
        title='Error', 
        ok_button='Aceptar')
    return render_template("nuevoUsuario.html")

@app.route("/actualizarInventario")
def actualizarInventario():
    return render_template("actualizarInventario.html")

@app.route("/actualizarProducto")
def actualizarProducto():
    return render_template("actualizarProducto.html")

@app.route("/enviarCorreo", methods=["POST", "GET"])
def enviarCorreo():
    if(request.method=="POST"):
        email1 = request.form["email"]
        email2 = request.form["email2"]
        if(email1==email2):
            msg = Message('Recuperar contraseña', sender='noResponderMisionTicD@gmail.com', recipients=[email1])
            msg.body="Para crear su nueva contraseña, ingrese al siguiente link: http://127.0.0.1:5000/newPassword"
            mail.send(msg)
            return ("Correo enviado a "+email1)
        else:
            return render_template("forgot.html")
    else:
        return render_template("forgot.html")

@app.route("/newPassword", methods=["POST", "GET"])
def newPassword():
    return render_template("newPassword.html") 