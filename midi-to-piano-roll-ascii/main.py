import mido
from termcolor import cprint

INPUT_FILE = './for_elise_by_beethoven.mid'
INPUT_FILE = './alla-turca.mid'

def main():
    messages = mido.MidiFile(INPUT_FILE)
    messages = [msg for msg in messages if msg.type in ['note_on', 'note_off']][:30]

    # TODO-NEXT: Read time data
    # Maybe take mido's parsed messages and do this in JS, actually? Then, I probably can:
    # - More easily make a MIDI player to check I'm interpreting this all correctly
    # - Not be limited by the resolution of ASCII art
    # - Then later I can figure out how to do the ASCII art problem (i.e. low vertical resolution), if I want

    for msg in messages:
        if msg.type == 'note_on':
            # print(msg)
            note = to_piano_roll_index(msg.note)
            draw_row([note])
        elif msg.type == 'note_off':
            pass
            # cprint(msg, 'blue')
        else:
            1/0

    print('''
 .  . .  . . .  . .  . . .  . .  . . .  . .  . . .  . .  . . .  . .  . . .  . .  . . .
A BC D EF G A BC D EF G A BC D EF G A BC D EF G A BC D EF G A BC D EF G A BC D EF G A BC
                                       ^ middle C
    '''.strip())

def pipe(x, fns):
    for fn in fns:
        x = fn(x)
    return x


def to_piano_roll_index(midi_note_number):
    return midi_note_number - 21

def draw_row(notes):
    row = [' '] * 88
    for note in notes:
        row[note] = '#'
    print(''.join(row).rstrip())


main()
