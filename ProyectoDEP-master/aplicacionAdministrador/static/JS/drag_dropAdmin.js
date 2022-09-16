console.log('Hola Mundo desdeadmin');

const archivos = document.getElementById('archivo-dictamen');
const prev = document.getElementById('preview');
 
const boton = document.getElementById('boton');
const input = document.getElementById('archivo-dictamen');

boton.addEventListener('click', () => {
   input.click();
});     

// boton.addEventListener('click', e =>{
//     console.log('Click');
//     input.click();
//     // showFiles(archivos.files);
// });

// button.addEventListener('click', e =>{
//     e.preventDefault();
//     input.click();
//     showFiles(archivos.files);
// });


input.addEventListener('change', e => {
    e.preventDefault();
    showFiles(files);
});




const showFiles = (files) =>{
    cont = 0;
    if(files.length === undefined){
        processFile(files);
    } else{
        for(const file of files){
            processFile(file, cont);
            cont++;
        }
    }
    purgarArchivos();
};

const processFile = (file, indice) => {
    const docType = file.type;
    const validExtensions = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png', 'image/PNG'];
    if(docType == 'application/pdf') icon = '<i class="far fa-file-pdf fa-1x"></i>';
    else icon = '<i class="far fa-file-image fa-1x"></i>';

    if(validExtensions.includes(docType)){
        const fileReader = new FileReader();
        fileReader.addEventListener('load', e => {
            const fileUrl = fileReader.result;
            const archivo = `
            <div id="${indice}" class="container">
    <div class="row">
    
        <span style="background-color: #ece8ff; border-radius: 30px; padding: .3rem; 
        margin-bottom: .2rem; padding-left: 1rem;">${file.name} ${icon} 
        <button onclick="eliminarArchivo(${indice})" class="btn btn-warning" type="button" style="width: auto; border-radius: 15px; height: auto; margin-top: .05rem; margin-bottom: .05rem;">
            <svg aria-hidden="true" focusable="false" data-prefix="fas" data-icon="trash-can" class="svg-inline--fa fa-trash-can" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" height="1rem" width="1rem">
                <path fill="currentColor" d="M32 464C32 490.5 53.5 512 80 512h288c26.5 0 48-21.5 48-48V128H32V464zM304 208C304 199.1 311.1 192 320 192s16 7.125 16 16v224c0 8.875-7.125 16-16 16s-16-7.125-16-16V208zM208 208C208 199.1 215.1 192 224 192s16 7.125 16 16v224c0 8.875-7.125 16-16 16s-16-7.125-16-16V208zM112 208C112 199.1 119.1 192 128 192s16 7.125 16 16v224C144 440.9 136.9 448 128 448s-16-7.125-16-16V208zM432 32H320l-11.58-23.16c-2.709-5.42-8.25-8.844-14.31-8.844H153.9c-6.061 0-11.6 3.424-14.31 8.844L128 32H16c-8.836 0-16 7.162-16 16V80c0 8.836 7.164 16 16 16h416c8.838 0 16-7.164 16-16V48C448 39.16 440.8 32 432 32z">
                </path>
            </svg> Eliminar
        </button>
        </span>
    </div> 
</div>
            `;
            const html = document.querySelector('#preview').innerHTML;
            document.querySelector('#preview').innerHTML = archivo + html;
        });
        fileReader.readAsDataURL(file);
    } else{
        alert(file.name + ", No es un archivo permitido, ingresa solamente pdfs o imágenes");
        quitar.push(indice);
    }
};

const reiniciarPreview = () => {
    while(prev.firstChild){
        prev.removeChild(prev.firstChild);
    }
};

const eliminarArchivo = (indice) => {
    const nodo = document.getElementById(indice);
    prev.removeChild(nodo);

    const dt = new DataTransfer();
    for(let i = 0; i < archivos.files.length; i++){
        const file = archivos.files[i];
        if (indice !== i) dt.items.add(file)
    }
    archivos.files = dt.files

};

const purgarArchivos = () => {

    const dt = new DataTransfer();
    for(let i = 0; i < archivos.files.length; i++){
        const file = archivos.files[i];
        if (archivos.files[i].name.endsWith('.pdf') ||
            archivos.files[i].name.endsWith('.jpeg') || 
            archivos.files[i].name.endsWith('.jpg') || 
            archivos.files[i].name.endsWith('.png') ||
            archivos.files[i].name.endsWith('.PNG')) dt.items.add(file)
    }
    archivos.files = dt.files
};



archivos.onchange = (e) =>{
    console.log('Agregó archivos');
    reiniciarPreview();
    showFiles(archivos.files);
}
