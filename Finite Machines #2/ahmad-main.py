###########################################
#   Author: Ahmad M. Osman
#   Date: 9/14/2017
#   File name: ahmad-main.py
#   Class: CS 260
#   Instructor: Dr. Kent Lee
#	Purpse: Ch 2 Prog Ex 2 (c)
###########################################


import state
import io
import streamreader


class FiniteStateMachine:

    def __init__(self, states, startStateId, classes):
        self.states = states
        self.startStateId = startStateId
        self.classes = classes

        for stateId in self.states:
            self.states[stateId].setClasses(classes)

    def accepts(self, strm):
        c = strm.readChar()
        while not strm.eof():
            q = self.states[self.startStateId]
            self.startStateId = self.states[self.startStateId].onGoTo(c)

            if self.startStateId == state.NoTransition:
                print("That string is not accepted.")
                return

            c = strm.readChar()

        if self.states[self.startStateId].isAccepting():
            print("This string is accepted by the Finite State Machine.")
        else:
            print("That string is not accepted.")


def main():

    q1 = state.State(1, True)
    q2 = state.State(2, True)
    q3 = state.State(3, True)
    q4 = state.State(4, True)
    q5 = state.State(5)

    classes = {}
    classes["a"] = set(["a"])
    classes["b"] = set(["b"])

    q1.addTransition("a", 2)
    q1.addTransition("b", 1)
    q2.addTransition("a", 3)
    q2.addTransition("b", 2)
    q3.addTransition("a", 4)
    q3.addTransition("b", 3)
    q4.addTransition("a", 5)
    q4.addTransition("b", 4)
    q5.addTransition("a", 5)
    q5.addTransition("b", 5)

    s = input("Please enter a string of a's and b's:")
    while s:
        dfa = FiniteStateMachine(
            {1: q1, 2: q2, 3: q3, 4: q4, 5: q5}, 1, classes)
        strm = streamreader.StreamReader(io.StringIO(s))
        dfa.accepts(strm)
        s = input("Please enter a string of a's and b's:")

    print('Program Completed.')

if __name__ == "__main__":
    main()
