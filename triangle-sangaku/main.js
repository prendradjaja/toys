const scaleFactor = 60;

const canvas = document.querySelector('canvas');
const ctx = canvas.getContext('2d');

ctx.translate(canvas.width * 0.2, canvas.height * 0.8);

ctx.scale(scaleFactor, -scaleFactor);

// x- and y-axes
{
  ctx.lineWidth = 2 / scaleFactor;

  ctx.strokeStyle = '#cccccc'
  ctx.beginPath()
  ctx.moveTo(0, -20)
  ctx.lineTo(0, 20)
  ctx.stroke()

  ctx.beginPath()
  ctx.moveTo(-20, 0)
  ctx.lineTo(20, 0)
  ctx.stroke()
}

// Triangle
ctx.lineWidth = 4 / scaleFactor;
ctx.strokeStyle = '#000000'
ctx.beginPath()
ctx.moveTo(0, 0)
ctx.lineTo(4, 0)
ctx.lineTo(0, 3)
ctx.closePath()
ctx.stroke()

// Circles
{
  const r = 5/7;

  ctx.lineWidth = 4 / scaleFactor;
  ctx.strokeStyle = '#000000'
  ctx.beginPath()
  ctx.arc(
    r, 11/5*r,
    r, // radius
    0, Math.PI * 2 // start and end angle
  );
  ctx.stroke()

  ctx.lineWidth = 4 / scaleFactor;
  ctx.strokeStyle = '#000000'
  ctx.beginPath()
  ctx.arc(
    13/5*r, r,
    r, // radius
    0, Math.PI * 2 // start and end angle
  );
  ctx.stroke()
}
