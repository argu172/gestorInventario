function mostrar() {
    var tipo = document.getElementById("password");
    if(tipo.type == "password"){
        tipo.type = "text";
    }else{
        tipo.type = "password";
    }
}

function validarExtension() {
    let archivo = document.getElementById('imagen').value,
        extension = archivo.substring(archivo.lastIndexOf('.'),archivo.length);
    if(document.getElementById('imagen').getAttribute('accept').split(',').indexOf(extension) < 0) {
      alert('Archivo inválido. La extensión ' + extension+' no es una imagen');
    }
}

function iguales() {
    let email1 = document.getElementById('email').value, 
        email2 = document.getElementById('email2').value;
    if (email1 != email2){
        alert('Los correos no coinciden');
    } else{
        alert('Correo enviado a '+email1);
    }
}

function validar_clave(){
    let passw1 = document.getElementById('newpass1').value;
    let passw2 = document.getElementById('newpass2').value;
    if(passw1 == passw2){
        var mayuscula = false;
        var minuscula = false;
        var numero = false;
        for(var i = 0;i<passw1.length;i++){
            if(passw1.charCodeAt(i) >= 65 && passw1.charCodeAt(i) <= 90){
                mayuscula = true;
            }
            else if(passw1.charCodeAt(i) >= 97 && passw1.charCodeAt(i) <= 122){
                minuscula = true;
            }
            else if(passw1.charCodeAt(i) >= 48 && passw1.charCodeAt(i) <= 57){
                numero = true;
            }
        }
        if(mayuscula == true && minuscula == true && numero == true){
            cumple = true;
        }else{
            cumple = false;
        }
        if(cumple){
            alert('Contraseña cambiada con éxito');
            return true;
        }else{
            alert('La contraseña ingresada no cumple con los requisitos de seguridad');
            return false;
        }
    }else{
        alert('Las contraseñas no coinciden');
        return false;
    }
}