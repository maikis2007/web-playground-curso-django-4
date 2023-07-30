function show(e) {
    var source = e.target.result;
    var avatar = document.getElementById('img_avatar');

    avatar.src = source;
}

function process(e) {
    var image = e.target.files[0];
    var reader = new FileReader();

    reader.readAsDataURL(image);
    reader.addEventListener('load', show, false);
    document.getElementById('volver_avatar').classList.remove('d-none');
}

document.getElementById('select_avatar').addEventListener('change', process, false);
