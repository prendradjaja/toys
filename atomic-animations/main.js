const $ = s => document.querySelector(s);

let position = { x: 100, y: 100 };

function main() {
  updatePosition();

  document.addEventListener('keydown', (e) => {
    if (e.key === 'j' || e.key === 'ArrowDown') {
      position.y += 100;
    } else if (e.key === 'k' || e.key === 'ArrowUp') {
      position.y -= 100;
    } else if (e.key === 'h' || e.key === 'ArrowLeft') {
      position.x -= 100;
    } else if (e.key === 'l' || e.key === 'ArrowRight') {
      position.x += 100;
    } else {
      // Do nothing
    }
    updatePosition();
  });
}

function updatePosition() {
  $('#box').style.left = `${position.x}px`;
  $('#box').style.top = `${position.y}px`;
}

main();
