/**Colocar fecha */
var d = new Date();
function days() {
    var day = d.getDay();
    switch (day) {
        case 0:
            return "Domingo";
        case 1:
            return "Lunes";
        case 2:
            return "Martes";
        case 3:
            return "Miercoles";
        case 4:
            return "Jueves";
        case 5:
            return "Viernes";
        case 6:
            return "Sabado";
        default:
            break;
    }
}
function months() {
    var mon = d.getMonth();
    switch (mon) {
        case 0:
            return "Enero";
        case 1:
            return "Febrero";
        case 2:
            return "Marzo";
        case 3:
            return "Abril";
        case 4:
            return "Mayo";
        case 5:
            return "Junio";
        case 6:
            return "Julio";
        case 7:
            return "Agosto";
        case 8:
            return "Septiembre";
        case 9:
            return "Octubre";
        case 10:
            return "Noviembre";
        case 11:
            return "Diciembre";
        default:
            break;
    }
}


function fecha() {
    document.write(
        days(),
        ", " + d.getDate(),
        " de " + months(),
        " de " + d.getFullYear()
    );
}