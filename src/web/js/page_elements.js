/*
Handles various UI elements
Elements: console scroller, search bar
*/

// Variables/Site Elements
let consoles        = document.getElementById('consoles');
let consoles_margin = parseInt(window.getComputedStyle(consoles).marginLeft);
let console_pos, console_pos_initial, console_pos_limit;

// Calculates the size of the screen and adjusts the "start point" of the console scroller
function calculate_consoles_per_scroll() {
    let window_width = window.innerWidth - 120; // The arrows are 60px wide
    let count = 0;

    // Increments until the screen is "empty"
    while (window_width - 450 > 0) {
        count++;
        window_width -= 450;
    }

    //This is used to figure out how much the position changed by on resize
    let original_pos = console_pos_initial - count;

    console_pos_initial = count;

    //If console_pos hasn't been set yet (first load) it defaults it
    if (!console_pos) {
        console_pos = count;
    } else {
        console_pos = (console_pos - original_pos);
    }
}

// Adjusts the scroller when the screen is resized
window.addEventListener('resize', () => {
    calculate_consoles_per_scroll();

    // Debugging
    document.getElementById('ratio').innerText = window.innerWidth + ' x ' + window.innerHeight;
});

// Shifts the margin positive to make it scroll left, adjusts position
document.getElementById('console-left').addEventListener('click', () => {
    if (console_pos != console_pos_initial) {
        console_pos--;
        consoles_margin += 450;
        consoles.style.marginLeft = consoles_margin + 'px';
    }
})

// Shifts the margin negative to make it scroll right, adjusts position
document.getElementById('console-right').addEventListener('click', () => {
    if (console_pos != console_pos_limit) {
        console_pos++;
        consoles_margin -= 450;
        consoles.style.marginLeft = consoles_margin + 'px';
    }
})