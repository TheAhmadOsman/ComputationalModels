###########################################
#   Author: Ahmad M. Osman
#   Date: 11/17/2017
#
#   Class: CS 260
#   Instructor: Dr. Kent Lee
#
#   File name: ahmad-main.py
#   Purpose: Turing Machine Simulator
###########################################


class Tape:

    def __init__(self, inputStr):
        self.tape = [' '] * 100

        while(len(inputStr) >= (len(self.tape) / 2)):
            self.tape = self.tape * 2

        self.location = (len(self.tape) - 1) // 2

        for i in range(len(inputStr)):
            self.tape[self.location + i] = inputStr[i]

    def moveLeft(self):
        self.location = self.location - 1

    def moveRight(self):
        self.location = self.location + 1

    def read(self):
        return self.tape[self.location]

    def write(self, ch):
        self.tape[self.location] = ch

    def __str__(self):
        output = ""
        for ch in self.tape:
            if ch not in [' ', '$']:
                output += '|' + ch
        output = '|' + '$' + output + '|' + '$' + '|'
        return output


class TuringMachine:

    def __init__(self, tape, states, classes, tapeAlphabet, transitions, blank, initialState, finalStates):
        self.tape = tape
        self.states = states
        self.classes = classes
        self.tapeAlphabet = tapeAlphabet
        self.transitions = transitions
        self.blank = blank
        self.initialState = initialState
        self.finalStates = finalStates

    def step(self):
        state = self.initialState

        done = False
        while not done:
            ch = self.tape.read()

            state, write, direction = self.transitions[(state, ch)]
            self.tape.write(write)

            if direction == 'R':
                self.tape.moveRight()
            elif direction == 'L':
                self.tape.moveLeft()

            if state in self.finalStates:
                done = True


def main():

    tape = Tape("$reverse$")
    states = [0, 1]
    classes = ['r', 'e', 'v', 's']
    tapeAlphabet = classes + [' ', '$']

    transitions = {
        (0, '$'): (1, '$', 'R'),

        (1, 'r'): (1, 'r', 'R'),
        (1, 'e'): (1, 'e', 'R'),
        (1, 'v'): (1, 'v', 'R'),
        (1, 's'): (1, 's', 'R'),
        (1, '$'): (2, '$', 'L'),

        (2, 'r'): (3, '$', 'R'),
        (2, 'e'): (4, '$', 'R'),
        (2, 'v'): (5, '$', 'R'),
        (2, 's'): (6, '$', 'R'),
        (2, '$'): (8, '$', 'L'),

        (3, '$'): (3, '$', 'R'),
        (3, ' '): (7, 'r', 'L'),
        (3, 'r'): (3, 'r', 'R'),
        (3, 'e'): (3, 'e', 'R'),
        (3, 'v'): (3, 'v', 'R'),
        (3, 's'): (3, 's', 'R'),

        (4, '$'): (4, '$', 'R'),
        (4, ' '): (7, 'e', 'L'),
        (4, 'r'): (4, 'r', 'R'),
        (4, 'e'): (4, 'e', 'R'),
        (4, 'v'): (4, 'v', 'R'),
        (4, 's'): (4, 's', 'R'),

        (5, '$'): (5, '$', 'R'),
        (5, ' '): (7, 'v', 'L'),
        (5, 'r'): (5, 'r', 'R'),
        (5, 'e'): (5, 'e', 'R'),
        (5, 'v'): (5, 'v', 'R'),
        (5, 's'): (5, 's', 'R'),

        (6, '$'): (6, '$', 'R'),
        (6, ' '): (7, 's', 'L'),
        (6, 'r'): (6, 'r', 'R'),
        (6, 'e'): (6, 'e', 'R'),
        (6, 'v'): (6, 'v', 'R'),
        (6, 's'): (6, 's', 'R'),

        (7, '$'): (7, '$', 'L'),
        (7, ' '): (0, ' ', 'R'),
        (7, 'r'): (7, 'r', 'L'),
        (7, 'e'): (7, 'e', 'L'),
        (7, 'v'): (7, 'v', 'L'),
        (7, 's'): (7, 's', 'L'),

        (8, '$'): (8, '$', 'L'),
        (8, ' '): (8, ' ', 'L')
    }

    blank = '$'
    initialState = 0
    finalStates = [8]

    reverse = TuringMachine(tape, states, classes, tapeAlphabet,
                            transitions, blank, initialState, finalStates)
    reverse.step()

    print(tape)

if __name__ == "__main__":
    main()
