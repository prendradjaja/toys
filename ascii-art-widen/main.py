import fileinput


for line in fileinput.input():
    line = line.rstrip('\n')
    print(''.join(a + b for a, b in zip(line, ' ' * len(line))))
