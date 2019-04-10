An automated solver for the [8 Puzzle](https://en.wikipedia.org/wiki/15_puzzle). This program searches for a solution
using A* search algorithm with a Manhattan distance.

Notes:

* The actual A* search algorithm is in `search.py`. The command-line interface is in `main.py`.
`problem.py` contains some boilerplate used to represent the problem in general, while `rules.py` contains the
actual rules of the 8 Puzzle problem and `heuristics.py` contains viable heuristics supplied to the search algorithm.


To get started, run `main.py`:

```
$ python ./eight_puzzle/main.py -h
usage: main.py [-h] [-i ITERATIONS] [-ww WIDTH] [-hh HEIGHT] [-v] [-vv]
               {solve,play}

8 puzzle.

positional arguments:
  {solve,play}

optional arguments:
  -h, --help            show this help message and exit
  -i ITERATIONS, --iterations ITERATIONS
                        Number of iterations to shuffle solution before
                        searching.
  -ww WIDTH, --width WIDTH
                        Width of the board.
  -hh HEIGHT, --height HEIGHT
                        Height of the board.
  -v, --verbose         Be verbose.
  -vv, --debug          Be even more verbose.
```

Example session:

```
$ python ./eight_puzzle/main.py --width 3 --height 3 solve
2 3 4
6 0 1
7 - 5

Searching for solution ..

Found following solution:

LEFT

2 3 4
6 0 1
- 7 5

UP

2 3 4
- 0 1
6 7 5

RIGHT

2 3 4
0 - 1
6 7 5

UP

2 - 4
0 3 1
6 7 5

LEFT

- 2 4
0 3 1
6 7 5

DOWN

0 2 4
- 3 1
6 7 5

RIGHT

0 2 4
3 - 1
6 7 5

RIGHT

0 2 4
3 1 -
6 7 5

UP

0 2 -
3 1 4
6 7 5

LEFT

0 - 2
3 1 4
6 7 5

DOWN

0 1 2
3 - 4
6 7 5

RIGHT

0 1 2
3 4 -
6 7 5

DOWN

0 1 2
3 4 5
6 7 -
```
