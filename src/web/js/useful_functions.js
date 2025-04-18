/* 
Miscellaneous functions that are useful.
Functions: capitalize
*/

// Capitalizes a word for convenience
function capitalize(word) {
    if (word == '3ds') {
        return '3DS';
    }

    if (word == 'ds') {
        return 'DS';
    }

    if (word == 'nes') {
        return 'NES';
    }

    if (word == 'snes') {
        return 'SNES';
    }

    return word.charAt(0).toUpperCase() + word.slice(1);
}