const cover = document.getElementById('cover');
const cover_preview = document.getElementById('cover-preview');
const hover = document.getElementById('hover');
const hover_preview = document.getElementById('hover-preview');

cover.addEventListener('change', (e) => {
    const file = e.target.files[0];
    
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            cover_preview.src = e.target.result;
        }
        reader.readAsDataURL(file);
    } else {
        cover_preview.src = "";
    }
})

hover.addEventListener('change', (e) => {
    const file = e.target.files[0];
    
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            hover_preview.src = e.target.result;
        }
        reader.readAsDataURL(file);
    } else {
        hover_preview.src = "https://placehold.co/300x300";
    }
})

window.onload = () => { 
    window.resizeTo(900, 1000);
    window.moveTo(1500, 0);
}