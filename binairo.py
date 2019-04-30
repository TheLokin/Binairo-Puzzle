#!/usr/bin/python3
# -*- coding: utf-8 -*-

from itertools import combinations, product
from argparse import ArgumentParser
import numpy
import sys
import os

class SatSolver:
    def __init__(self, input_file):
        self.__size = 0
        self.__clauses = []
        if os.path.exists('tmp.cnf'):
            os.remove('tmp.cnf')
        try:
            # Parsear el fichero de entrada para obtener las cláusulas iniciales
            with open(input_file) as input:
                try:
                    self.__size = int(input.readline())
                    if self.__size % 2 != 0:
                        print('Could not solve a puzzle of size:', self.__size)
                        self.__size = 0
                        return
                    
                    position = 0
                    for line in input:
                        for char in line:
                            if char == '.':
                                position += 1
                            elif char == '0':
                                position += 1
                                self.__clauses.append(str(-position)+' 0\n')
                            elif char == '1':
                                position += 1
                                self.__clauses.append(str(position)+' 0\n')
                    if position != self.__size*self.__size:
                        print('File contain wrong arguments')
                        self.__size = 0
                        return
                except:
                    print('File contain wrong arguments')
                    self.__size = 0
                    return
        except FileNotFoundError:
            print('File not found:', input_file)
            self.__size = 0
            return
        
        self.__solve_rows()
        self.__solve_columns()

        # Escribe las cláusulas en un fichero para el clasp
        with open('tmp.cnf', 'w+') as output:
            output.write('p cnf '+ str(self.__size*self.__size)+' '+ str(len(self.__clauses))+'\n')
            for operation in self.__clauses:
                output.write(operation)

        # Llamada a clasp
        os.system('clasp --verbose=0 tmp.cnf > solution.cnf')
        os.remove('tmp.cnf')

        # Construye el puzzle con la solución obtenida de clasp
        output_file = 'sol'+str(self.__size).zfill(2)+'.txt'
        if os.path.exists(output_file):
            os.remove(output_file)
        with open('solution.cnf') as input:
            with open(output_file, 'w+') as output:
                position = 0
                for line in input:
                    for word in line.split(' '):
                        try:
                            number = int(word)
                            if number != 0:
                                if number > 0:
                                    output.write('1')
                                else:
                                    output.write('0')
                                if (position % self.__size == self.__size-1):
                                    output.write('\n')
                                position += 1
                        except:
                            continue
        os.remove('solution.cnf')
        if (position == 0):
            os.remove(output_file)
            print('The puzzle has not solution')
            self.__size = 0
        else:
            print('Solution written in:', output_file)
        
    def __get_position(self, x, y):
        return x+y*self.__size+1

    # Cláusulas para las filas
    def __solve_rows(self):
        for y in range(0, self.__size):
            row = []

            # Cláusulas para no tener más de dos '1' o '0' consecutivos en una fila
            for x in range(0, self.__size-2):
                position1 = self.__get_position(x, y)
                position2 = self.__get_position(x+1, y)
                position3 = self.__get_position(x+2, y)
                self.__clauses.append(str(position1)+' '+str(position2)+' '+str(position3)+' 0\n')
                self.__clauses.append(str(-position1)+' '+str(-position2)+' '+str(-position3)+' 0\n')
                row.append(position1)
            
            row.append(self.__get_position(x+1, y))
            row.append(self.__get_position(x+2, y))
            
            # Cláusulas para balancear las filas
            for positions in combinations(row, int(self.__size/2+1)):
                clause1 = ''
                clause2 = ''
                for position in positions:
                    clause1 += str(position)+' '
                    clause2 += str(-position)+' '
                self.__clauses.append(clause1+'0\n')
                self.__clauses.append(clause2+'0\n')

            # Cláusulas para no repetir filas
            for positions in list(product(*((x, -x) for x in row))):
                sign = []
                clause1 = ''
                c0 = 0
                c1 = 0
                append = True
                aux0 = 0
                c0 = 0
                aux1 = 0
                c1 = 0
                for position in positions:
                    if position < 0:
                        c0 += 1
                        if c0 > self.__size/2 or aux1 >= 3:
                            append = False
                            break
                        else:
                            aux1 = 0
                            aux0 += 1
                    else:
                        c1 += 1
                        if c1 > self.__size/2 or aux0 >= 3:
                            append = False
                            break
                        else:
                            aux0 = 0
                            aux1 += 1
                    sign.append(numpy.sign(-position))
                    clause1 += str(-position)+' '
                if append:
                    for k in range(y+1, self.__size):
                        clause2 = ''
                        for x in range(0, self.__size):
                            clause2 += str(sign[x]*self.__get_position(x, k))+' '
                        self.__clauses.append(clause1+clause2+'0\n')
    
    # Cláusulas para las columnas
    def __solve_columns(self):
        for x in range(0, self.__size):
            column = []
            
            # Cláusulas para no tener más de dos '1' o '0' consecutivos en una columna
            for y in range(0, self.__size-2):
                position1 = self.__get_position(x, y)
                position2 = self.__get_position(x, y+1)
                position3 = self.__get_position(x, y+2)
                self.__clauses.append(str(position1)+' '+str(position2)+' '+str(position3)+' 0\n')
                self.__clauses.append(str(-position1)+' '+str(-position2)+' '+str(-position3)+' 0\n')
                column.append(position1)
            
            column.append(self.__get_position(x, y+1))
            column.append(self.__get_position(x, y+2))
            
            # Cláusulas para balancear las columnas
            for positions in combinations(column, int(self.__size/2+1)):
                clause1 = ''
                clause2 = ''
                for position in positions:
                    clause1 += str(position)+' '
                    clause2 += str(-position)+' '
                self.__clauses.append(clause1+'0\n')
                self.__clauses.append(clause2+'0\n')
                
            # Cláusulas para no repetir columnas
            for positions in list(product(*((y, -y) for y in column))):
                sign = []
                clause1 = ''
                append = True
                aux0 = 0
                c0 = 0
                aux1 = 0
                c1 = 0
                for position in positions:
                    if position < 0:
                        c0 += 1
                        if c0 > self.__size/2 or aux1 >= 3:
                            append = False
                            break
                        else:
                            aux1 = 0
                            aux0 += 1
                    else:
                        c1 += 1
                        if c1 > self.__size/2 or aux0 >= 3:
                            append = False
                            break
                        else:
                            aux0 = 0
                            aux1 += 1
                    sign.append(numpy.sign(-position))
                    clause1 += str(-position)+' '
                if append:
                    for k in range(x+1, self.__size):
                        clause2 = ''
                        for y in range(0, self.__size):
                            clause2 += str(sign[x]*self.__get_position(k, y))+' '
                        self.__clauses.append(clause1+clause2+'0\n')

    def is_correct(self, input_file=None):
        solution_file = 'sol'+str(self.__size).zfill(2)+'.txt'
        if self.__size > 0:
            if (input_file == None):
                input_file = 'examples/'+solution_file
            try:
                with open(solution_file) as solution:
                    puzzle = []
                    for line in solution:
                        for char in line:
                            if char != '\n':
                                puzzle.append(char)
            except FileNotFoundError:
                print('Solver solution file not found: sol'+str(self.__size).zfill(2)+'.txt')
                return
            try:
                with open(input_file) as correct_solution:
                    puzzle_correct = []
                    for line in correct_solution:
                        for char in line:
                            if char != '\n':
                                puzzle_correct.append(char)
                print('Is correct: '+str(puzzle == puzzle_correct))
            except FileNotFoundError:
                print('Solution file not found:', input_file)

class AspSolver:
    def __init__(self, input_file):
        self.__size = 0
        if not os.path.exists('binairo.lp'):
            print('File not found: binairo.lp')
            return
        
        # Parsear el fichero de entrada para obtener las cláusulas iniciales
        if os.path.exists('tmp.lp'):
            os.remove('tmp.lp')
        with open('tmp.lp', 'w+') as output:
            try:
                with open(input_file) as input:
                    try:
                        self.__size = int(input.readline())
                        if self.__size % 2 != 0:
                            print('Could not solve a puzzle of size:', self.__size)
                            self.__size = 0
                            return
                        
                        output.write('#const n='+str(self.__size)+'.\n')
                        position = 0
                        for line in input:
                            for char in line:
                                if char == '.':
                                    position += 1
                                elif char == '0':
                                    output.write('dot('+str(position%self.__size)+','+str(position//self.__size)+',white).\n')
                                    position += 1
                                elif char == '1':
                                    output.write('dot('+str(position%self.__size)+','+str(position//self.__size)+',black).\n')
                                    position += 1
                        if position != self.__size*self.__size:
                            print('File contain wrong arguments')
                            self.__size = 0
                            return
                    except:
                        print('File contain wrong arguments')
                        self.__size = 0
                        return
            except:
                print('File not found:', input_file)
                self.__size = 0
                return
        
        # Llamada a clingo
        os.system('clingo --verbose=0 binairo.lp tmp.lp > solution.lp')
        os.remove('tmp.lp')

        # Construye el puzzle con la solución obtenida de clingo
        output_file = 'sol'+str(self.__size).zfill(2)+'.txt'
        if os.path.exists(output_file):
            os.remove(output_file)
        with open('solution.lp') as input:
            puzzle = {}
            for word in input.readline()[:-1].split(' '):
                word = word.split(',')
                puzzle[self.__get_position(int(word[0][4:]), int(word[1]))] = word[2][:-1]
        os.remove('solution.lp')
        if (len(puzzle) == 0):
            print('The puzzle has not solution')
            self.__size = 0
            return
        with open(output_file, 'w+') as output:
            for position in range(0, self.__size*self.__size):
                if puzzle[position+1] == 'white':
                    output.write('0')
                else:
                    output.write('1')
                if (position % self.__size == self.__size-1):
                    output.write('\n')
        print('Solution written in:', output_file)
    
    def __get_position(self, x, y):
        return x+y*self.__size+1

    def is_correct(self, input_file=None):
        solution_file = 'sol'+str(self.__size).zfill(2)+'.txt'
        if self.__size > 0:
            if (input_file == None):
                input_file = 'examples/'+solution_file
            try:
                with open(solution_file) as solution:
                    puzzle = []
                    for line in solution:
                        for char in line:
                            if char != '\n':
                                puzzle.append(char)
            except FileNotFoundError:
                print('Solver solution file not found: sol'+str(self.__size).zfill(2)+'.txt')
                return
            try:
                with open(input_file) as correct_solution:
                    puzzle_correct = []
                    for line in correct_solution:
                        for char in line:
                            if char != '\n':
                                puzzle_correct.append(char)
                print('Is correct: '+str(puzzle == puzzle_correct))
            except FileNotFoundError:
                print('Solution file not found:', input_file)

if __name__ == '__main__':
    parser = ArgumentParser(description='Binairo solver')
    parser.add_argument('input_file', metavar='I', type=str, help='route of the binairo puzzle instance')
    parser.add_argument('-a', '--asp', action='store_true', help='use asp to solve')
    parser.add_argument('-c', '--comp', help='compare the result with this file')
    args = parser.parse_args()
    if args.asp:
        solver = AspSolver(args.input_file)
    else:
        solver = SatSolver(args.input_file)
    if args.comp != None:
        solver.is_correct(args.comp)