import Socket from './socket';
import Game from './components/game';

// General Interaction Logic
let close = document.querySelector('.instructions-close');
let instructions_toggle = document.querySelector('.instructions-toggle');
let overlay_toggle = (e) => {
    e.preventDefault();
    document.querySelector('.game').classList.toggle('hide');
    document.querySelector('.overlay').classList.toggle('hide');
};
close.addEventListener('click', overlay_toggle);
instructions_toggle.addEventListener('click', overlay_toggle);

let instructions = document.querySelector('.instructions');
let overlay_ignore = (e) => {
    e.stopPropagation();
};
instructions.addEventListener('click', overlay_ignore);

// Start the game
const socket = Socket(Game);