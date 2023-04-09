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

const searchFocus = document.getElementById('search-focus');
const keys = [
    { keyCode: 'AltLeft', isTriggered: false },
    { keyCode: 'ControlLeft', isTriggered: false },
];

window.addEventListener('keydown', (e) => {
    keys.forEach((obj) => {
        if (obj.keyCode === e.code) {
            obj.isTriggered = true;
        }
    });

    const shortcutTriggered = keys.filter((obj) => obj.isTriggered).length === keys.length;

    if (shortcutTriggered) {
        searchFocus.focus();
    }
});

window.addEventListener('keyup', (e) => {
    keys.forEach((obj) => {
        if (obj.keyCode === e.code) {
            obj.isTriggered = false;
        }
    });
});


async function Resumen() {
    let txtlink, traduccion = 1;
    txtlink = document.getElementById("txtlink").value;

    if (txtlink) {
        var info = new FormData();
        info.append('link', txtlink)
        info.append('traduccion', traduccion)

        let fetchData = {
            method: 'POST',
            body: info,
            headers: new Headers()
        }
        
        let data = await fetch('http://127.0.0.1:5000/api_resumen', fetchData)
        .then(res => res.json())
        .then(data => {
            var inputResumen = document.getElementById("idresumen");
            var inputTraducido = document.getElementById("idtraduccion");

            inputResumen.value = data['original']
            inputTraducido.value = data['traducido']
        })
    } else {
        alert('Campos Incompletos')
    }
}
