from collections import namedtuple


stroke_counts = {}


def main():
    Line = namedtuple('Line', 'text hl_shorts hl_longs')

    lines = [
        Line('OK and finally I really like,',                   25, 13),
        Line('besides the open world exploring',                30, 17),
        Line('(which I\'ve done SO little of overall,',         29, 17),
        Line('while still trying to follow storyline things),', 40, 22),
    ]

    print('en\thl\ttext')
    for line in lines:
        hl_count = combine(line.hl_shorts, line.hl_longs)
        print(count_ascii(line.text), hl_count, line.text, sep='\t')


def count_ascii(s):
    if not stroke_counts:
        populate_stroke_counts()
    result = 0
    for ch in s:
        assert ch in stroke_counts, f'{ch} is not in ascii-stroke-counts.tsv'
        result += stroke_counts[ch]
    return result


def populate_stroke_counts():
    for line in open('ascii-stroke-counts.tsv'):
        line = line.rstrip('\n')
        ch, shorts, longs = line.split('\t')
        shorts = int(shorts)
        longs = int(longs)
        stroke_counts[ch] = combine(shorts, longs)


def combine(shorts, longs):
    return (shorts * 1.0) + (longs * 1.5)


if __name__ == '__main__':
    main()
