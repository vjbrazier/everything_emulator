/*
Manages functions related to the game buttons.
Functions: 
*/
const games = document.getElementById('games');

async function loadGames() {
    let game_data = await eel.get_game_data()();

    for (let key in game_data) {
        let rom = game_data[key]

        let game_name    = rom['display-name'];
        let console_name = rom['console'];
        let cover_image  = rom['js-cover-image'];
        let hover_image  = rom['js-hover-image'];
        
        let game_div     = document.createElement('div');
        let game_button  = document.createElement('button');
        let game_text    = document.createElement('h3');
        let game_console = document.createElement('h3');
        let cover_img    = document.createElement('img');
        let hover_img    = document.createElement('img');

        game_button.id = rom;

        game_div.classList.add('game-div');
        game_button.classList.add('game-button');
        game_text.classList.add('game-text');
        game_console.classList.add('game-console');
        cover_img.classList.add('game-img', 'cover');
        hover_img.classList.add('game-img', 'hover');
        
        cover_img.src = cover_image;
        hover_img.src = hover_image;

        game_text.innerText = game_name;
        game_console.innerText = capitalize(console_name.replaceAll('-', ' '));
        
        game_button.appendChild(cover_img);
        game_button.appendChild(hover_img);
        game_div.appendChild(game_button);
        game_div.appendChild(game_console);
        game_div.appendChild(game_text);
        games.appendChild(game_div);
    }
}