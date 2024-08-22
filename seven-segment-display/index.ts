import * as fs from 'fs';

const template = fs.readFileSync('template.txt', 'utf8');

const digitHeight = 3;

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

type DigitImage = string[];

function main() {
  showDigits(1234567890);
}

function makeDigitImage(n: string): DigitImage {
  const segments = whichSegments[n];
  if (segments === undefined) {
    throw new Error(`Invalid digit: ${n}`);
  }
  const result: DigitImage = [];
  let i = 0;
  let row = '';
  for (const ch of template) {
    if (ch === '\n') {
      result.push(row);
      row = '';
    } else if (ch === ' ') {
      row += ch;
    } else {
      if (segments.includes(i)) {
        row += ch;
      } else {
        row += ' ';
      }
      i++;
    }
  }
  return result;
}

function showDigits(n: number): void {
  const digitChars = Array.from(n.toString());
  const digitImages = digitChars.map(makeDigitImage);
  for (let i = 0; i < digitHeight; i++) {
    let line = '';
    for (const image of digitImages) {
      line += image[i];
    }
    console.log(line);
  }
}

main();
