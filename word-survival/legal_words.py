legal_words = set()

for line in open('./sowpods.txt'):
    line = line.strip()
    if line.startswith('#') or line == '':
        continue
    legal_words.add(line)
