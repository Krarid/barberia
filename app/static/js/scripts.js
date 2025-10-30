/********* Add modal *********/
const addIcon = document.getElementById('addIcon');
const addModal = document.getElementById('addModal');
const backgroundModal = document.getElementById('backgroundModal');

if(addIcon) {
    addIcon.addEventListener('click', async function (event) {
        backgroundModal.style.display = 'block';
    });
}

if(backgroundModal) {
    backgroundModal.addEventListener('click', async function (event) {
        if (!addModal.contains(event.target)) {
            backgroundModal.style.display = 'none';
            return;
        }
    });
}