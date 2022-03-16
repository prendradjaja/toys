const fs = require('fs');
const PNG = require('pngjs').PNG;

const incolor1 = [241, 194, 50]; // yellow
const incolor2 = [11, 83, 148]; // blue

const outcolor1 = [255, 0, 144];
const outcolor2 = [122, 233, 255];

function main() {
  if (process.argv.length < 4) {
    console.log('Usage: node index.js INPUT_PATH OUTPUT_PATH');
    return;
  }

  const [inputPath, outputPath] = process.argv.slice(2);

  fs.createReadStream(inputPath)
    .pipe(
      new PNG()
    )
      .on("parsed", function () {
        for (var y = 0; y < this.height; y++) {
          for (var x = 0; x < this.width; x++) {
            var idx = (this.width * y + x) << 2;

            // Read color
            const originalColor = this.data.slice(idx, idx + 3);

            // Compute new color
            const weight1 = distance(originalColor, incolor2);
            const weight2 = distance(originalColor, incolor1);
            let newColor = vectorWeightedAverage(outcolor1, outcolor2, weight1, weight2);
            newColor = toValidValues(newColor);

            // Write new color
            this.data[idx] = newColor[0];
            this.data[idx + 1] = newColor[1];
            this.data[idx + 2] = newColor[2];
          }
        }

        this.pack().pipe(fs.createWriteStream(outputPath));
      });
}

function distance(p1, p2) {
  const [x1, y1, z1] = p1;
  const [x2, y2, z2] = p2;
  const dx = x1 - x2;
  const dy = y1 - y2;
  const dz = z1 - z2;
  return Math.sqrt(dx*dx + dy*dy + dz*dz);
}

function scalarWeightedAverage(x1, x2, w1, w2) {
  return (x1*w1 + x2*w2)/(w1 + w2);
}

function vectorWeightedAverage(v1, v2, w1, w2) {
  return [
    scalarWeightedAverage(v1[0], v2[0], w1, w2),
    scalarWeightedAverage(v1[1], v2[1], w1, w2),
    scalarWeightedAverage(v1[2], v2[2], w1, w2),
  ];
}

function toValidValues(color) {
  return (color
    .map(x => clamp(x, 0, 255))
    .map(x => Math.floor(x))
  );
}

function clamp(x, lo, hi) {
  if (x > hi) {
    return hi;
  } else if (x < lo) {
    return lo;
  } else {
    return x;
  }
}

main();
