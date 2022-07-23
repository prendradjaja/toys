import { Tween, Easing, update } from './tween.esm.js';

const $ = s => document.querySelector(s);

let livePosition = { x: 100, y: 100 };
let lastTween;

function main() {
  updatePosition(livePosition);

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
    }


    const move = { x: 0, y: 0 };

    if (e.key === 'j' || e.key === 'ArrowDown') {
      move.y = 100;
    } else if (e.key === 'k' || e.key === 'ArrowUp') {
      move.y = -100;
    } else if (e.key === 'h' || e.key === 'ArrowLeft') {
      move.x = -100;
    } else if (e.key === 'l' || e.key === 'ArrowRight') {
      move.x = 100;
    } else {
      return;
    }

    let lastProgress = 0;

    function onProgress({ progress }) {
      const progressDelta = progress - lastProgress;
      lastProgress = progress;
      livePosition = linearCombination(livePosition, 1, move, progressDelta);
      updatePosition(livePosition);
    }

    lastTween = new Tween({ progress: 0 })
      .to({ progress: 1 }, 250)
      .easing(Easing.Quadratic.Out)
      .onUpdate(({ progress }) => onProgress({ progress }))
      .onComplete(() => onProgress({ progress: 1 }))
      .onStop(() => onProgress({ progress: 1 }))
      .start();
  });
}

function updatePosition(position) {
  $('#box').style.left = `${position.x}px`;
  $('#box').style.top = `${position.y}px`;
}

function addVectors(v1, v2) {
  return {
    x: v1.x + v2.x,
    y: v1.y + v2.y,
  };
}

function scaleVector(v, scalar) {
  return {
    x: v.x * scalar,
    y: v.y * scalar,
  };
}

function linearCombination(v1, w1, v2, w2) {
  return addVectors(
    scaleVector(v1, w1),
    scaleVector(v2, w2)
  );
}

main();
