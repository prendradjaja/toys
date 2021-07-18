## Set game simulation

Plays a random game of [Set][set], displaying the state of the game after each
turn and the leftover cards (if any) at the end of the game.

Example output:

```
$ python3 main.py
Deck	Board	Matched
69	12	0*3=0
69	9	1*3=3
68	7	2*3=6
66	6	3*3=9
61	8	4*3=12
59	7	5*3=15
55	8	6*3=18
49	11	7*3=21
46	11	8*3=24
45	9	9*3=27
43	8	10*3=30
42	6	11*3=33
41	4	12*3=36
37	5	13*3=39
36	3	14*3=42
32	4	15*3=45
26	7	16*3=48
22	8	17*3=51
19	8	18*3=54
17	7	19*3=57
11	10	20*3=60
10	8	21*3=63
9	6	22*3=66
8	4	23*3=69
3	6	24*3=72
2	4	25*3=75
0	6	25*3=75

Leftover cards:
1,	oval,	open,	purple
3,	squig,	open,	purple
3,	oval,	open,	green
1,	squig,	solid,	green
3,	diam,	open,	green
1,	diam,	stripe,	purple
```

[set]: https://en.wikipedia.org/wiki/Set_(card_game)
