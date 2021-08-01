import fileinput


for line in fileinput.input():
    line = line.rstrip('\n')
    print(' '.join(line))
