import re
import sys

from termcolor import cprint


def main():
    CHORD_PATTERN = (
        r'(' +  # Use a capturing group so that re.split() returns the match
            r'\b' +
            r'[A-G]' +  # Any note...
            r'[#b]?' +  # ...possibly with an accidental
            r'(?:7|6|sus2|sus4|m7|maj7|m|dim|aug)?' +  # Chord quality -- there's definitely more than just these
            r'(?:/' +  # Possibly with a slash note
                r'[A-G]' +  # Any note...
                r'[#b]?' +  # ...possibly with an accidental
            r')?' +
            r'\b' +
        r')' +
        ''
    )

    input_file_path = sys.argv[1] if len(sys.argv) > 1 else 'example.txt'
    for line in open(input_file_path).read().splitlines():
        chunks = re.split(CHORD_PATTERN, line)
        for chunk in chunks:
            if re.fullmatch(CHORD_PATTERN, chunk):
                cprint(chunk, 'red', end='')
            else:
                print(chunk, end='')
        print()


if __name__ == '__main__':
    main()
