var canvas = document.getElementById('my-canvas');
var ctx = canvas.getContext('2d');

ctx.lineWidth = 3;

const size = 200;

const colors = [];
for (let i = 0; i < 25; i++) {
  colors.push(`hsl(${i / 25 * 360}, 100%, 50%)`);
}

function star(n, k, cx, cy) {
  // To fix: Use a polygon to fix the issue with the top spoke (obvious on
  // star(15,7) but more subtle on the other stars)
  if (!cx) {
    ([cx, cy] = centers.shift());
  }
  const r = size * 0.4;
  const points = [];
  for (let i = 0; i < n; i++) {
    const theta = 2 * Math.PI * i / n - 0.5 * Math.PI;
    const x = r * Math.cos(theta) + cx;
    const y = r * Math.sin(theta) + cy;
    points.push([x, y]);
  }

  ctx.beginPath();
  ctx.strokeStyle = colors.shift();
  for (let j = 0; j < n; j++) {
    const i = (j * k) % n;
    ctx.lineTo(...points[i]);
  }
  ctx.lineTo(...points[0]);
  ctx.stroke();
}

function dot(cx, cy) {
  console.log(cx, cy);
  ctx.beginPath();
  ctx.arc(cx, cy, 5, 0, 2 * Math.PI);
  ctx.fill();
}

const centers = [];

let n = 3;
for (let cy = size; cy < 15 * size; cy += size) {
  for (let cx = size; cx < 6 * size; cx += size) {
    centers.push([cx - size * 0.5, cy - size * 0.5]);
  }
}

star(5,2)
star(7,2)
star(7,3)
star(8,3)
star(9,2)

star(9,4)
star(10,3)
star(11,2)
star(11,3)
star(11,4)

star(11,5)
star(12,5)
star(13,2)
star(13,3)
star(13,4)

star(13,5)
star(13,6)
star(14,3)
star(14,5)
star(15,2)

star(15,4)
star(15,7)
star(16,3)
star(16,5)
star(16,7)
