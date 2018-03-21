###########################################
#   Author: Ahmad M. Osman
#   Date: 9/15/2017
#   File name: ahmad-main.py
#   Class: CS 260
#   Instructor: Dr. Kent Lee
#   Purpse: Ch 2 Prog Ex 4 (d)
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

    q1 = state.State(1)
    q2 = state.State(2)
    q3 = state.State(3)
    q4 = state.State(4)
    q5 = state.State(5)
    q6 = state.State(6)
    q7 = state.State(7, True)
    q8 = state.State(8, True)
    q9 = state.State(9, True)
    q10 = state.State(10)

    classes = {}
    classes["a"] = set(["a"])
    classes["b"] = set(["b"])

    q1.addTransition("a", 2)
    q1.addTransition("b", 1)
    q2.addTransition("a", 3)
    q2.addTransition("b", 1)
    q3.addTransition("a", 4)
    q3.addTransition("b", 1)
    q4.addTransition("a", 5)
    q4.addTransition("b", 4)
    q5.addTransition("a", 6)
    q5.addTransition("b", 4)
    q6.addTransition("a", 7)
    q6.addTransition("b", 4)
    q7.addTransition("a", 10)
    q7.addTransition("b", 8)
    q8.addTransition("a", 9)
    q8.addTransition("b", 8)
    q9.addTransition("a", 7)
    q9.addTransition("b", 8)
    q10.addTransition("a", 10)
    q10.addTransition("b", 10)

    s = input("Please enter a string of a's and b's:")
    while s:
        dfa = FiniteStateMachine(
            {1: q1, 2: q2, 3: q3, 4: q4, 5: q5, 6: q6, 7: q7, 8: q8, 9: q9, 10: q10}, 1, classes)
        strm = streamreader.StreamReader(io.StringIO(s))
        dfa.accepts(strm)
        s = input("Please enter a string of a's and b's:")

    print('Program Completed.')

if __name__ == "__main__":
    main()
