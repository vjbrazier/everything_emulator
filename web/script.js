async function loadConsoles() {
    let consoles = await eel.get_consoles()();
    let console_list = document.getElementById('consoles');

    for (let i = 0; i < consoles.length; i++) {
        let button = document.createElement('button');
        button.classList.add('console');

        if (i == 0) {
            button.classList.add('carosel-0');
        } else if (i == 1) {
            button.classList.add('carosel-1');
        } else if (i == 2) {
            button.classList.add('carosel-2');
        } else if (i == 3) {
            button.classList.add('carosel-3');
        } else if (i == 4) {
            button.classList.add('carosel-4');
        }

        button.id = consoles[i].toLowerCase();
        button.innerText = consoles[i];
        console_list.appendChild(button);
    }

}



window.onload = loadConsoles;