function usuarioSave() {
    let doc = $("#documento").val();
    let nom = $("#nombre").val();
    let cic = $("#ciclo").val();
    let estado = $("#estado").val();
    let sexo = $("#sexo").val();
    $.ajax({
        type: "POST",
        url: "/estudiante/save",
        data: {
            documento: doc,
            nombre: nom,
            ciclo: cic,
            sexo: sexo,
            estado: estado
        },
        dataType: "JSON",
    }).done(function (datos) {
        alert(datos["msj"])
    }).fail(function (e) {
        //Si ocurre un error
        console.log(e);
    }).always(function () {

    });
}