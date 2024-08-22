import * as fs from 'fs';

const template = fs.readFileSync('template.txt', 'utf8');

const digitWidth = 3;

const whichSegments: Partial<Record<string, number[]>> = {
  '0': [0, 1, 3, 4, 5, 6],
  '1': [3, 6],
  '2': [0, 2, 3, 4, 5],
  '3': [0, 2, 3, 5, 6],
  '4': [1, 2, 3, 6],
  '5': [0, 1, 2, 5, 6],
  '6': [0, 1, 2, 4, 5, 6],
  '7': [0, 3, 6],
  '8': [0, 1, 2, 3, 4, 5, 6],
  '9': [0, 1, 2, 3, 6],
};

type Image = ImageChar[];
interface ImageChar {
  r: number,
  c: number,
  ch: string,
}

function main() {
  showDigits(1234567890);
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

function showDigits(n: number): void {
  const digitChars = Array.from(n.toString());
  const fullImage: Image = [];
  let offset = 0;
  for (let digitImage of digitChars.map(makeDigitImage)) {
    digitImage = shift(digitImage, offset);
    fullImage.push(...digitImage);
    offset += digitWidth;
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

function shift(image: Image, horiontalOffset: number) {
  return image.map(imageChar => ({
    ...imageChar,
    c: imageChar.c + horiontalOffset,
  }));
}

main();
