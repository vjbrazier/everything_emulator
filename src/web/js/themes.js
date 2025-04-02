document.addEventListener('DOMContentLoaded', function() {
    //Grab the webpage, and sets the theme from local storage, or just defaults to light
    const webpage = document.getElementById('webpage');
    webpage.setAttribute('data-theme', localStorage.getItem('theme') || 'light');

    const themes = document.getElementsByClassName('theme-button');

    //Allows the toggling of the theme button by clicking.
    const toggleThemes = document.getElementById('toggle-themes-button');
    toggleThemes.addEventListener('click', function() {
        for (let i = 0; i < themes.length; i++) {
            themes[i].classList.toggle('visible');
        }
        // themeButtons.classList.toggle('visible');
    });


    //Adds an event listener to each button that uses the text of the button to set the theme
    for (let i = 0; i < themes.length; i++) {
        themes[i].addEventListener('click', function(event) {
            var targetTheme = themes[i].getAttribute('data-theme-button');
            webpage.setAttribute('data-theme', targetTheme);
            localStorage.setItem('theme', targetTheme);
        });
    };
});