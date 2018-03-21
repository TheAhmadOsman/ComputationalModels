###########################################
#   Author: Ahmad M. Osman
#   Date: 12/8/2017
#
#   Class: CS 260
#   Instructor: Dr. Kent Lee
#
#   File name: ahmad-main.py
#   Purpose: Solving Sudoku
###########################################


def getSValue(x, y, z):
    s = 81 * (x - 1) + 9 * (y - 1) + z
    return s


def main():
    inputFile = open('sudoku.puzzle', 'r')
    row = 1
    column = 0
    count = 0
    values = []

    for i in range(1, 10):
        line = inputFile.readline()
        lineSplitted = line.split()
        column = 0
        for val in lineSplitted:
            column += 1
            if val != "x":
                values.append(getSValue(row, column, int(val)))
                count += 1
        row += 1

    print("p cnf", 729, (8829 + count))

    for val in values:
        print(val, 0)

    for x in range(1, 10):
        for y in range(1, 10):
            for z in range(1, 10):
                s = getSValue(x, y, z)
                print(s, end=" ")
            print(0)

    for y in range(1, 10):
        for z in range(1, 10):
            for x in range(1, 9):
                for i in range(x + 1, 10):
                    s1 = getSValue(x, y, z)
                    s2 = getSValue(i, y, z)
                    print(s1 * (-1), s2 * (-1), 0)

    for x in range(1, 10):
        for z in range(1, 10):
            for y in range(1, 9):
                for i in range(y + 1, 10):
                    s1 = getSValue(x, y, z)
                    s2 = getSValue(x, i, z)
                    print(s1 * (-1), end=" ")
                    print(s2 * (-1), 0)

    for z in range(1, 10):
        for i in range(0, 3):
            for j in range(0, 3):
                for x in range(1, 4):
                    for y in range(1, 4):
                        for k in range(y + 1, 4):
                            s1 = getSValue(3 * i + x, 3 * j + y, z)
                            s2 = getSValue(3 * i + x, 3 * j + k, z)
                            print(s1 * (-1), end=" ")
                            print(s2 * (-1), 0)

    for z in range(1, 10):
        for i in range(0, 3):
            for j in range(0, 3):
                for x in range(1, 4):
                    for y in range(1, 4):
                        for k in range(x + 1, 4):
                            for l in range(1, 4):
                                s1 = getSValue(3 * i + x, 3 * j + y, z)
                                s2 = getSValue(3 * i + k, 3 * j + l, z)
                                print(s1 * (-1), end=" ")
                                print(s2 * (-1), 0)


if __name__ == "__main__":
    main()
