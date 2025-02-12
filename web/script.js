async function loadConsoles() {
    let consoles = await eel.get_consoles()();
    let console_list = document.getElementById('consoles');

    consoles.forEach(console => {
        let button = document.createElement('button');
        button.classList.add('console');
        button.innerText = console;
        console_list.appendChild(button);
    });

}

window.onload = loadConsoles;