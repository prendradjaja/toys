import * as fs from 'fs';

const template = fs.readFileSync('template-seven-slashes.txt', 'utf8');

const verticalOffsetPerDigit = -2;
const horizontalOffsetPerDigit = 2;

const whichSegments: Partial<Record<string, number[]>> = {
  '0': [0, 2, 1, 5, 6, 4],
  '1': [1, 4],
  '2': [0, 3, 1, 5, 6],
  '3': [0, 3, 1, 6, 4],
  '4': [2, 3, 1, 4],
  '5': [0, 2, 3, 6, 4],
  '6': [0, 2, 3, 5, 6, 4],
  '7': [0, 1, 4],
  '8': [0, 2, 3, 1, 5, 6, 4],
  '9': [0, 2, 3, 1, 4]
};

type Image = ImageChar[];
interface ImageChar {
  r: number,
  c: number,
  ch: string,
}

function main() {
  showDigits('1234567890');
  showDigits('314159265');
}

function makeDigitImage(n: string): Image {
  const segments = whichSegments[n];
  if (segments === undefined) {
    throw new Error(`Invalid digit: ${n}`);
  }
  const result: Image = [];
  let r = 0;
  let c = 0;
  let row = '';
  let i = 0;
  for (const ch of template) {
    if (ch === '\n') {
      r++;
      c = 0;
    } else if (ch === ' ') {
      c++;
    } else {
      if (segments.includes(i)) {
        result.push({ r, c, ch });
      }
      c++;
      i++;
    }
  }
  return result;
}

function showDigits(s: string): void {
  const fullImage: Image = [];
  let i = 0;
  for (let digitImage of Array.from(s).map(makeDigitImage)) {
    digitImage = shift(digitImage, verticalOffsetPerDigit * i, horizontalOffsetPerDigit * i);
    fullImage.push(...digitImage);
    i++;
  }

  let rmin = Infinity;
  let rmax = -Infinity;
  let cmin = Infinity;
  let cmax = -Infinity;
  for (const imageChar of fullImage) {
    rmin = Math.min(rmin, imageChar.r);
    rmax = Math.max(rmax, imageChar.r);
    cmin = Math.min(cmin, imageChar.c);
    cmax = Math.max(cmax, imageChar.c);
  }

  for (let r = rmin; r <= rmax; r++) {
    let line = '';
    for (let c = cmin; c <= cmax; c++) {
      const imageChar = fullImage.find(each => each.r === r && each.c === c);
      if (imageChar === undefined) {
        line += ' ';
      } else {
        line += imageChar.ch;
      }
    }
    console.log(line);
  }
}

function shift(image: Image, verticalOffset: number, horiontalOffset: number) {
  return image.map(imageChar => ({
    ...imageChar,
    r: imageChar.r + verticalOffset,
    c: imageChar.c + horiontalOffset,
  }));
}

main();
