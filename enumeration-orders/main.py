import position_order
import option_order
import option_order_simplified
import sys


def main(options, length):
    print('Length (N) =', length)
    print(f'Options = {options} (K = {len(options)})')
    print()

    results1 = position_order.main(options, length)
    print('Position order:')
    print(f'  Nodes: {results1.nodes:,}\tResults: {len(results1.results):,}')

    results2 = option_order.main(options, length)
    print()
    print('Option order:')
    print(f'  Nodes: {results2.nodes:,}\tResults: {len(results2.results):,}')

    results3 = option_order_simplified.main(options, length)
    print()
    print('Option order (simplified):')
    print(f'  Nodes: {results3.nodes:,}\tResults: {len(results3.results):,}')

    assert sorted(results1.results) == sorted(results2.results) == sorted(results3.results)


options = None
length = None

if len(sys.argv) == 1:
    options = 'ABCD'
    length = 4
elif len(sys.argv) == 3:
    try:
        options = sys.argv[1]
        length = int(sys.argv[2])
    except ValueError:
        pass

if options and length:
    main(options, length)
else:
    print('''Usage examples:
  python3 main.py        # Run with default options
  python3 main.py ABC 8  # How many strings of length 8 using with allowed characters ABC?''')
