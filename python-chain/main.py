from chain import *


print(
    ['a', 'b', 'cde']
    | map_(dot('upper'))  # shorthand for `| map_(lambda x: x.upper())`
    | map_(lambda x: x + '!')
    | join(' ')
)

print(
    1
    | F(lambda x: x + 1)
    | F(lambda x: x * 2)
)
