<h1 align="center">Binairo Puzzle</h1>

## Introduction
This project consists in solving the Binairo puzzle (see here an [online game](https://www.puzzle-binairo.com)), also called
Takuzu, and described as follows. We have a grid of n x n cells that may contain a white circle or a black circle. The initial
configuration provides some cell values and the rest must be filled with circles according to the following rules:

- Each row and each column must contain the same number of circles of each color, that is, n/2 instances of each case.

- There cannot be more than 2 consecutive circles of the same color in any direction (vertical or horizontal).

- There cannot be two rows or two columns with the same configuration.

An example of initial configuration and the corresponding solution can be seen below. 

<div align="center">
  <img alt="Figure 1" src="img/figure1.jpg"/>
  <img alt="Figure 2" src="img/figure2.jpg"/>
</div>

## Implementation

It will encode the scenario both as a SAT problem and as an ASP program.

This takes an ASCII file <inputfile> with the initial grid where each cell contains a character: '0' (a white circle),
'1' (a black circle) or '.' (an empty cell to be filled). The first line contains an even number n>=2 specifying the number of
rows and columns (we have a square grid). For instance, the example in the picture above would be represented as:

```
6
......
.11.0.
01....
....00
.1....
0..1..
```

This program will generate a DIMACS file and make an external call to *clasp* when it uses SAT or *clingo* when it uses ASP
to get a solution. It will also decode back output and print the complete solution as follows:

```
100110
011001
010011
101100
110010
001101
```

## Execution

By default, it uses ASP and the examples folder contains a set of benchmarks of different sizes (6, 8, 10, 14, 20), where
domX.txt is the input file and solX.txt its corresponding solution.

```
./binairo.py [-h] [-a] [-c input] input

-h            show this help message and exit
-a            use ASP to solve
-c            compare the result with this file
-input        route of the binairo puzzle instance

```
