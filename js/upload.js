const url = 'process.py';
const form = document.querySelector('form');

form.addEventListener('submit', e => {
    e.preventDefault();
    const files = document.querySelector('[type=file]').files;
    const formData = new FormData();

    for (let x = 0; x < files.length; x++) {
        let file = files[x];
        formData.append('files[]', file);
    }

    fetch(url, {
        method: 'POST',
        body: formData
    }).then(response => {
        console.log(response);
    });
});
