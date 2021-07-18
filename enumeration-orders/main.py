import position_order
import option_order
import option_order_simplified


options = 'ABCD'
length = 4


results1 = position_order.main(options, length)
print('Position order:')
print(f'  Nodes: {results1.nodes}\tResults: {len(results1.results)}')

results2 = option_order.main(options, length)
print()
print('Option order:')
print(f'  Nodes: {results2.nodes}\tResults: {len(results2.results)}')

results3 = option_order_simplified.main(options, length)
print()
print('Option order (simplified):')
print(f'  Nodes: {results3.nodes}\tResults: {len(results3.results)}')

assert sorted(results1.results) == sorted(results2.results) == sorted(results3.results)
