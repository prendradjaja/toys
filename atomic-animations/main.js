import { Tween, Easing, update } from './tween.esm.js';

const $ = s => document.querySelector(s);

let position = { x: 100, y: 100 };
let lastTween;

function main() {
  updatePosition(position);

  function animate(time) {
    requestAnimationFrame(animate);
    update(time);
  }
  requestAnimationFrame(animate);

  document.addEventListener('keydown', (e) => {
    if (lastTween) {
      // If the most recent tween is still in progress, we want to skip to the
      // end.

      // (Actually, this only should happen if the key pressed is one of
      // the keys handled below. As is, pressing any other key will also skip
      // to the end. TODO Don't skip to the end for other keys)
      lastTween.stop();
      updatePosition(position);
    }

    const oldPosition = {...position};

    if (e.key === 'j' || e.key === 'ArrowDown') {
      position.y += 100;
    } else if (e.key === 'k' || e.key === 'ArrowUp') {
      position.y -= 100;
    } else if (e.key === 'h' || e.key === 'ArrowLeft') {
      position.x -= 100;
    } else if (e.key === 'l' || e.key === 'ArrowRight') {
      position.x += 100;
    } else {
      return;
    }

    lastTween = new Tween({...oldPosition})
      .to(position, 250)
      .easing(Easing.Quadratic.Out)
      .onUpdate((livePosition) => {
        updatePosition(livePosition);
      })
      .start();
  });
}

function updatePosition(position) {
  $('#box').style.left = `${position.x}px`;
  $('#box').style.top = `${position.y}px`;
}

main();
