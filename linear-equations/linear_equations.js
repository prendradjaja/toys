/**
 * m: slope
 * b: y-intercept
 */
function makeLinearEquation(m, b) {
  const f = x => m * x + b;
  Object.defineProperties(f, {
    m: { value: m },
    b: { value: b },
  });
  return f;
}

function makeLinearEquationFromPoints(p1, p2) {
  const [x1, y1] = p1;
  const [x2, y2] = p2;
  const m = (y2 - y1) / (x2 - x1);
  const b = y1 - m * x1;
  return makeLinearEquation(m, b)
}

const line = makeLinearEquationFromPoints([1, 2], [3, 3]);
console.log(line, line.m, line.b);
console.log(line(0));
console.log(line(5));
