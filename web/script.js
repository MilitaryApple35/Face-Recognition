let listName, fecha, hora, dateTime;
async function pasar_lista() {
    document.getElementById("loading-screen").style.display = "block";
    await eel.tomar_lista()(function(result) {
        if (result!=null && result[0] !== null) {
            listName = result[0];
            fecha = result[1];
            hora = result[2];
            dateTime = result[3];
            document.getElementById("confirmation-screen").style.display = "block";
            document.getElementById("list-name").innerText = listName;
            document.getElementById("date").innerText = fecha;
            document.getElementById("time").innerText = hora;
        } else {
            alert("Ha ocurrido un error");
        }
    });
    document.getElementById("loading-screen").style.display = "none";
}

function confirmation() {
    eel.confirmar_lista(listName, dateTime);
    document.getElementById("confirmation-screen").style.display = "none";
}

function cancelList() {
    document.getElementById("confirmation-screen").style.display = "none";
}

async function cargar_lista() {
    try {
        const data = await eel.get_data()();
        const tableBody = document.getElementById('table-body');
        data.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${item.nombre}</td>
                <td>${item.hora}</td>
                <td>${item.fecha}</td>
            `;
            tableBody.appendChild(row);
        });
        document.getElementById('table-screen').style.display = 'block';
    } catch (error) {
        console.error('Error:', error);
    }
}

function take_photo() {
    document.getElementById('camera-screen').style.display = 'block';
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function(stream) {
            // Muestra el video en el elemento de video
            document.getElementById('video').srcObject = stream;
            document.getElementById('snap').addEventListener('click', function() {
                var canvas = document.getElementById('canvas');
                var context = canvas.getContext('2d');
                // Dibuja la imagen actual del video en el canvas
                context.drawImage(document.getElementById('video'), 0, 0, 640, 480);
                nombre= document.getElementById('input-nombre').value;
                // Convierte la imagen del canvas a base64
                var data = canvas.toDataURL(`${nombre}.png`);
                // Envía la imagen a Python
                eel.process_image(data, nombre);
                document.getElementById('camera-screen').style.display = 'none';
                stream.getTracks().forEach(track => track.stop());
            });
        })
        .catch(function(err) {
            console.log("Error: " + err);
        });
    
}


function hide_table() {
    document.getElementById('table-screen').style.display = 'none';
}

function salir() {
    eel.close_callback();
}