from flask import Flask, render_template, request, session
from werkzeug.utils import secure_filename
from flask_mail import Mail,  Message
from formularios import formUsuario, formProducto, formCantidad
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

FOLDER_IMAGENES = "static/img/"
EXT_VALIDAS = ["jpeg", "jpg", "png"]

@app.route("/", methods=["POST", "GET"])
def login():
    session.pop("usuario", None)
    session.pop("administrador", None)
    form = formUsuario()
    return render_template("login.html", form=form)

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
                if username == "admin":
                    session["administrador"] = username
                else:
                    session["usuario"] = username
                with sqlite3.connect("proyectoDB.db") as con:
                    con.row_factory = sqlite3.Row
                    cur = con.cursor()
                    cur.execute("SELECT * FROM productos")
                    row = cur.fetchall()
                    return render_template("inicioUsuario.html", form=form, row=row)
        eg.msgbox(msg='Usuario o contraseña inválidos!',
                title='Error!!', 
                ok_button='Aceptar')
        return render_template("login.html")
    else:
        if "administrador" in session:
            with sqlite3.connect("proyectoDB.db") as con:
                    con.row_factory = sqlite3.Row
                    cur = con.cursor()
                    cur.execute("SELECT * FROM productos")
                    row = cur.fetchall()
            return render_template("inicioUsuario.html", row=row)
        elif "usuario" in session:
            with sqlite3.connect("proyectoDB.db") as con:
                    con.row_factory = sqlite3.Row
                    cur = con.cursor()
                    cur.execute("SELECT * FROM productos")
                    row = cur.fetchall()
            return render_template("inicioUsuario.html", row=row)
        else:
            eg.msgbox(msg='Debe iniciar sesión para ingresar',
            title='Error', 
            ok_button='Aceptar')
            return render_template("login.html")

@app.route("/crearProducto")
def crearProducto():
    if "administrador" in session:
        return render_template("crearProducto.html")
    else:
        eg.msgbox(msg='Solo el administrador puede crear nuevos productos',
        title='Error', 
        ok_button='Aceptar')
    return render_template("inicioUsuario.html")

@app.route("/producto/crear", methods=["POST"])
def producto_crear():
    ref = request.form["referencia"]
    nombre = request.form["nombre"]
    cantidad = request.form["cantidad"]
    imagen = request.files["imagen"]
    ext = imagen.filename.rsplit(".", 1)[1]
    if ext in EXT_VALIDAS:
        with sqlite3.connect("proyectoDB.db") as con:
            ruta = secure_filename(imagen.filename)
            imagen.save(FOLDER_IMAGENES+ruta)
            cur = con.cursor()
            cur.execute("INSERT INTO productos (referencia, nombre, cantidad, imagen) VALUES (?,?,?,?)",
                        (ref, nombre, cantidad, ruta))
            con.commit()
            eg.msgbox(msg='Producto creado satisfactoriamente',
                title='Atención', 
                ok_button='Aceptar')
            return render_template("crearProducto.html")
        eg.msgbox(msg='Producto NO pudo ser creado',
            title='Error', 
            ok_button='Aceptar')
        return render_template("crearProducto.html")
    else:
        eg.msgbox(msg='Extensión de la imagen no es válida',
            title='Error', 
            ok_button='Aceptar')
        return render_template("crearProducto.html")

@app.route("/nuevoUsuario")
def nuevoUsuario():
    if "administrador" in session:
        return render_template("nuevoUsuario.html")
    else:
        eg.msgbox(msg='Solo el administrador puede crear nuevos usuarios',
        title='Error', 
        ok_button='Aceptar')
    return render_template("inicioUsuario.html")

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
    eg.msgbox(msg='Usuario NO pudo ser creado',
        title='Error', 
        ok_button='Aceptar')
    return render_template("nuevoUsuario.html")

@app.route("/actualizarInventario/<referencia>")
def actualizarInventario(referencia):
    with sqlite3.connect("proyectoDB.db") as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM productos WHERE referencia = ?", [referencia])
        row = cur.fetchone() 
    return render_template("actualizarInventario.html", row=row)

@app.route("/actualizarCantidad/<referencia>", methods=["POST"])
def actualizarCantidad(referencia):
    cant = request.form["cantidad"]
    with sqlite3.connect("proyectoDB.db") as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("UPDATE productos SET cantidad = ? WHERE referencia = ?", [cant, referencia])
        eg.msgbox(msg='Inventario actualizado satisfactoriamente',
            title='Atención', 
            ok_button='Aceptar')
        return render_template("inicioUsuario.html")

@app.route("/eliminarProducto/<referencia>")
def eliminarProducto(referencia):
    if "administrador" in session:
        with sqlite3.connect("proyectoDB.db") as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("DELETE FROM productos WHERE referencia = ?", [referencia])
            eg.msgbox(msg='Producto elimando',
                title='Atención', 
                ok_button='Aceptar')
            return render_template("inicioUsuario.html")
    else:
        eg.msgbox(msg='Solo el administrador puede eliminar productos',
        title='Error', 
        ok_button='Aceptar')
        return render_template("actualizarInventario.html")

@app.route("/actualizarProducto/<referencia>")
def actualizarProducto(referencia):
    if "administrador" in session:
        with sqlite3.connect("proyectoDB.db") as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM productos WHERE referencia = ?", [referencia])
            row = cur.fetchone() 
        return render_template("actualizarProducto.html", row=row)
    else:
        eg.msgbox(msg='Solo el administrador puede actualizar los datos del producto',
            title='Error', 
            ok_button='Aceptar')
        return render_template("actualizarProducto.html")

@app.route("/guardarCambio/<referencia>", methods=["POST","GET"])
def guardarCambio(referencia):
    if (request.method == "POST"):
        nombre = request.form["nombre"]
        imagen = request.files["imagen"]
        ext = imagen.filename.rsplit(".", 1)[1]
        if ext in EXT_VALIDAS:
            with sqlite3.connect("proyectoDB.db") as con:
                ruta = secure_filename(imagen.filename)
                imagen.save(FOLDER_IMAGENES+ruta)
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                cur.execute("UPDATE productos SET nombre = ?, imagen = ? WHERE referencia = ?", [nombre, ruta, referencia])
                eg.msgbox(msg='Producto Actualizado',
                    title='Atención', 
                    ok_button='Aceptar')
                return render_template("actualizarProducto.html")
        else:
            eg.msgbox(msg='Extensión de la imagen no es válida',
                title='Error', 
                ok_button='Aceptar')
            return render_template("actualizarProducto.html")
    else:
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