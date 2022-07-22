import { Tween, Easing, update } from './tween.esm.js';


const $ = s => document.querySelector(s);

let position = { x: 100, y: 100 };
let activeTween;

function main() {
  updatePosition(position);

  function animate(time) {
    requestAnimationFrame(animate);
    update(time);
  }
  requestAnimationFrame(animate);

  document.addEventListener('keydown', (e) => {
    if (activeTween) {
      activeTween.stop();
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

    activeTween = new Tween({...oldPosition})
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
