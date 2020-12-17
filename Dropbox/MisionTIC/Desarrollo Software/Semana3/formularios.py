from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

class formUsuario( FlaskForm ):
    usuario = StringField( 'usuario', validators=[DataRequired( message='No dejar vacío, completar')])
    password = PasswordField('password', validators=[DataRequired(message='No dejar vacio, completar')])
    email = EmailField('email', validators=[DataRequired(message='No dejar vacio, completar')])
    guardar = SubmitField( 'Guardar', render_kw={"onclick":"ususarioSave()"} )