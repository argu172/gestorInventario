from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

class formUsuario(FlaskForm ):
    usuario = StringField( 'usuario', validators=[DataRequired( message='No dejar vacío, completar')])
    password = PasswordField('password', validators=[DataRequired(message='No dejar vacio, completar')])
    email = EmailField('email', validators=[DataRequired(message='No dejar vacio, completar')])

class formProducto(FlaskForm):
    ref = IntegerField('referencia', validators=[DataRequired(message='No dejar vacío, completar')])
    nombre = StringField('nombre', validators=[DataRequired(message='No dejar vacío, completar')])
    cantidad = IntegerField('cantidad', validators=[DataRequired(message='No dejar vacío, completar')])
    imagen = FileField('imagen', validators=[DataRequired(message='No dejar vacío, completar')])

class formCantidad(FlaskForm):
    cant = IntegerField('cantidad', validators=[DataRequired(message='No dejar vacío, completar')])